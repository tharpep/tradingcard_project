from typing import List, Dict, Any, Optional, Tuple, Union
import logging
from datetime import datetime
from .base_service import BaseService
from .pokemon_api_service import pokemon_api_service
from .shared_card_service import SharedCardService
from repositories.repository_factory import get_card_repository
from models.card import Card, CardCreate, CardUpdate

logger = logging.getLogger(__name__)

class CardService(BaseService):
    """Service for card business logic - now uses shared service"""
    
    def __init__(self, user_id: Optional[str] = None, admin: bool = False):
        super().__init__()
        # Use shared service for common operations
        self.shared_service = SharedCardService(user_id=user_id, admin=admin)
        self.user_id = user_id
        self.admin = admin
        # Expose repository for backward compatibility with tests
        self.repository = self.shared_service.repository
        if admin:
            self.logger.info("CardService initialized in ADMIN mode - full system access")
        elif user_id:
            self.logger.info(f"CardService initialized for user: {user_id}")
        else:
            self.logger.info("CardService initialized without user context (anonymous)")
    
    def get_pokemon_card_data(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get Pokemon card data for autofill functionality
        
        Args:
            name: Card name to get data for
            
        Returns:
            Dictionary with card data or None if not found
        """
        self.logger.info(f"Getting Pokemon card data for: {name}")
        
        try:
            # Try to get card data from Pokemon TCG API
            card_data = pokemon_api_service.get_card_details(name)
            if card_data:
                self.logger.info(f"Found Pokemon card data for: {name}")
                return card_data
            else:
                self.logger.info(f"No Pokemon card data found for: {name}")
                return None
                
        except Exception as e:
            self.logger.warning(f"Error getting Pokemon card data for '{name}': {e}")
            return None
    
    def add_card(self, name: str, set_name: str = "Unknown", **kwargs) -> Union[int, str]:
        """Add a new card with business logic validation"""
        return self.shared_service.add_card(name=name, set_name=set_name, **kwargs)
    
    def get_card(self, card_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a card by ID"""
        return self.shared_service.get_card(card_id)
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """Get all cards"""
        return self.shared_service.get_all_cards()
    
    def search_cards(self, name: str) -> List[Dict[str, Any]]:
        """Search cards by name"""
        return self.shared_service.search_cards(name)
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite cards"""
        return self.shared_service.get_favorites()
    
    def update_card(self, card_id: Union[int, str], **kwargs) -> bool:
        """Update a card with validation"""
        return self.shared_service.update_card(card_id, **kwargs)
    
    def delete_card(self, card_id: Union[int, str]) -> bool:
        """Delete a card"""
        return self.shared_service.delete_card(card_id)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        return self.shared_service.get_collection_stats()
    
    def toggle_favorite(self, card_id: Union[int, str]) -> bool:
        """Toggle favorite status of a card"""
        return self.shared_service.toggle_favorite(card_id)
    
    # Implement abstract methods from BaseService
    def create(self, data: Dict[str, Any]) -> Union[int, str]:
        """Create a new card (implements BaseService)"""
        return self.add_card(**data)
    
    def get_by_id(self, record_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a card by ID (implements BaseService)"""
        return self.get_card(record_id)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all cards (implements BaseService)"""
        return self.get_all_cards()
    
    def update(self, record_id: Union[int, str], data: Dict[str, Any]) -> bool:
        """Update a card (implements BaseService)"""
        return self.update_card(record_id, **data)
    
    def delete(self, record_id: Union[int, str]) -> bool:
        """Delete a card (implements BaseService)"""
        return self.delete_card(record_id)
    
    def delete_all_cards(self) -> int:
        """Delete all cards from the collection"""
        return self.shared_service.delete_all_cards()
    
    def is_pokemon_api_available(self) -> bool:
        """Check if Pokemon TCG API is available"""
        return pokemon_api_service.is_api_available()
    
    # Type annotations updated to support both SQLite (int) and Supabase (str) IDs
