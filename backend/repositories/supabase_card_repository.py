from typing import List, Dict, Any, Optional, Union
import logging
import requests
from .base_repository import BaseRepository
from config import Config

logger = logging.getLogger(__name__)

class SupabaseCardRepository(BaseRepository):
    """Repository for card database operations using Supabase REST API"""
    
    def __init__(self, user_jwt_token: Optional[str] = None):
        super().__init__("cards")
        self.supabase_url = Config.SUPABASE_URL
        self.supabase_key = Config.SUPABASE_KEY
        self.user_jwt_token = user_jwt_token
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        
        # Supabase REST API endpoint
        self.api_url = f"{self.supabase_url}/rest/v1/{self.table_name}"
        
        # Headers for all requests - use user JWT if available, otherwise service key
        if self.user_jwt_token:
            self.headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.user_jwt_token}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
        else:
            # Fallback to service key for admin operations
            self.headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
        
        logger.info("Initialized Supabase REST API client")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"API Key: {'SET' if self.supabase_key else 'NOT SET'}")
    
    def create(self, data: Dict[str, Any]) -> str:
        """Create a new card and return its ID"""
        logger.info(f"Creating card via REST API: {data.get('name', 'Unknown')}")
        
        try:
            # Use direct table insert instead of stored procedure
            # This will respect RLS policies with user JWT context
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            
            # Extract the ID from the response
            result = response.json()
            if result and len(result) > 0:
                card_id = result[0]['id']
                logger.info(f"Card created with ID: {card_id}")
                return card_id
            else:
                raise Exception("No card ID returned from create operation")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create card via REST API: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def find_by_id(self, record_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Find a card by ID"""
        try:
            url = f"{self.api_url}?id=eq.{record_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return data[0]
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to find card by ID {record_id}: {e}")
            return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all cards"""
        try:
            url = f"{self.api_url}?order=date_added.desc"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to find all cards: {e}")
            return []
    
    def update(self, record_id: Union[int, str], data: Dict[str, Any]) -> bool:
        """Update a card by ID"""
        logger.info(f"Updating card ID {record_id}: {list(data.keys())}")
        
        try:
            url = f"{self.api_url}?id=eq.{record_id}"
            response = requests.patch(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return len(result) > 0
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update card {record_id}: {e}")
            return False
    
    def delete(self, record_id: Union[int, str]) -> bool:
        """Delete a card by ID"""
        logger.info(f"Deleting card ID: {record_id}")
        
        try:
            url = f"{self.api_url}?id=eq.{record_id}"
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete card {record_id}: {e}")
            return False
    
    def delete_all(self) -> int:
        """Delete all cards from the database"""
        logger.info("Deleting all cards from database")
        
        try:
            # Get all cards first to count them
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
            
            cards = response.json()
            total_cards = len(cards)
            
            if total_cards == 0:
                logger.info("No cards to delete")
                return 0
            
            # Delete all cards using Supabase's batch delete with a filter
            # Use a filter that matches all records (id is not null)
            delete_response = requests.delete(
                f"{self.api_url}?id=not.is.null",
                headers=self.headers
            )
            delete_response.raise_for_status()
            
            logger.info(f"Successfully deleted {total_cards} cards")
            return total_cards
            
        except Exception as e:
            logger.error(f"Failed to delete all cards: {e}")
            return 0
    
    def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search cards by name"""
        try:
            url = f"{self.api_url}?name=ilike.*{name}*"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search cards by name '{name}': {e}")
            return []
    
    def find_favorites(self) -> List[Dict[str, Any]]:
        """Find all favorite cards"""
        try:
            url = f"{self.api_url}?is_favorite=eq.true"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to find favorite cards: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            # Get all cards to calculate stats
            cards = self.find_all()
            
            total_cards = len(cards)
            total_quantity = sum(card.get('quantity', 0) for card in cards)
            favorites = sum(1 for card in cards if card.get('is_favorite'))
            
            # Find most common set
            sets = {}
            for card in cards:
                set_name = card.get('set_name', 'Unknown')
                sets[set_name] = sets.get(set_name, 0) + 1
            
            most_common_set = max(sets.items(), key=lambda x: x[1])[0] if sets else 'None'
            
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
