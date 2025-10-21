from typing import List, Dict, Any, Optional, Union
import logging
import os
from supabase import create_client, Client
from .base_repository import BaseRepository

logger = logging.getLogger(__name__)

class SupabaseCardRepository(BaseRepository):
    """Repository for card database operations using Supabase"""
    
    def __init__(self):
        super().__init__("cards")
        # Initialize Supabase client
        self.client = self._get_supabase_client()
    
    def _get_supabase_client(self) -> Client:
        """Initialize and return Supabase client"""
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        
        logger.info("Initializing Supabase client")
        return create_client(url, key)
    
    def create(self, data: Dict[str, Any]) -> str:
        """Create a new card and return its ID"""
        logger.info(f"Creating card: {data.get('name', 'Unknown')}")
        
        try:
            # Use the helper function for duplicate handling
            result = self.client.rpc('add_or_increment_card', {
                'p_name': data.get('name'),
                'p_set_name': data.get('set_name', 'Unknown'),
                'p_card_number': data.get('card_number'),
                'p_rarity': data.get('rarity'),
                'p_quantity': data.get('quantity', 1),
                'p_is_favorite': data.get('is_favorite', False),
                'p_card_grade': data.get('card_grade', 5.0),
                'p_card_price': data.get('card_price', 0.0),
                'p_card_type': data.get('card_type', 'Unknown'),
                'p_notes': data.get('notes'),
                'p_image_url': data.get('image_url'),
                'p_last_updated_price': data.get('last_updated_price'),
                'p_tags': data.get('tags', []),
                'p_user_id': data.get('user_id')
            }).execute()
            
            card_id = result.data
            logger.info(f"Card created with ID: {card_id}")
            return card_id
            
        except Exception as e:
            logger.error(f"Failed to create card: {e}")
            raise
    
    def find_by_id(self, record_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Find a card by ID"""
        try:
            result = self.client.table(self.table_name).select("*").eq("id", record_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Failed to find card by ID {record_id}: {e}")
            return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all cards"""
        try:
            result = self.client.table(self.table_name).select("*").order("date_added", desc=True).execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Failed to find all cards: {e}")
            return []
    
    def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search cards by name (partial match)"""
        try:
            result = self.client.table(self.table_name).select("*").ilike("name", f"%{name}%").order("name").execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Failed to search cards by name '{name}': {e}")
            return []
    
    def find_favorites(self) -> List[Dict[str, Any]]:
        """Find all favorite cards"""
        try:
            result = self.client.table(self.table_name).select("*").eq("is_favorite", True).order("name").execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Failed to find favorite cards: {e}")
            return []
    
    def update(self, record_id: Union[int, str], data: Dict[str, Any]) -> bool:
        """Update a card by ID"""
        logger.info(f"Updating card ID {record_id}: {list(data.keys())}")
        
        try:
            result = self.client.table(self.table_name).update(data).eq("id", record_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Failed to update card {record_id}: {e}")
            return False
    
    def delete(self, record_id: Union[int, str]) -> bool:
        """Delete a card by ID"""
        logger.info(f"Deleting card ID: {record_id}")
        
        try:
            result = self.client.table(self.table_name).delete().eq("id", record_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Failed to delete card {record_id}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            # Get all cards for stats calculation
            result = self.client.table(self.table_name).select("*").execute()
            cards = result.data
            
            if not cards:
                return {
                    'total_cards': 0,
                    'total_quantity': 0,
                    'favorites': 0,
                    'most_common_set': 'None'
                }
            
            # Calculate stats
            total_cards = len(cards)
            total_quantity = sum(card.get('quantity', 0) for card in cards)
            favorites = sum(1 for card in cards if card.get('is_favorite', False))
            
            # Most common set
            set_counts = {}
            for card in cards:
                set_name = card.get('set_name', 'Unknown')
                set_counts[set_name] = set_counts.get(set_name, 0) + 1
            
            most_common_set = max(set_counts.items(), key=lambda x: x[1])[0] if set_counts else 'None'
            
            return {
                'total_cards': total_cards,
                'total_quantity': total_quantity,
                'favorites': favorites,
                'most_common_set': most_common_set
            }
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                'total_cards': 0,
                'total_quantity': 0,
                'favorites': 0,
                'most_common_set': 'None'
            }
    
    def find_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Find cards by tags (Supabase-specific feature)"""
        try:
            result = self.client.table(self.table_name).select("*").overlaps("tags", tags).execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Failed to find cards by tags {tags}: {e}")
            return []
    
    def find_by_type(self, card_type: str) -> List[Dict[str, Any]]:
        """Find cards by type"""
        try:
            result = self.client.table(self.table_name).select("*").eq("card_type", card_type).order("name").execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Failed to find cards by type '{card_type}': {e}")
            return []
