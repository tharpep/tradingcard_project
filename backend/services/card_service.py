from typing import List, Dict, Any, Optional, Tuple, Union
import logging
from datetime import datetime
from .base_service import BaseService
from .pokemon_api_service import pokemon_api_service
from repositories.repository_factory import get_card_repository
from models.card import Card, CardCreate, CardUpdate

logger = logging.getLogger(__name__)

class CardService(BaseService):
    """Service for card business logic"""
    
    def __init__(self, user_id: Optional[str] = None, admin: bool = False):
        super().__init__()
        self.repository = get_card_repository()
        self.user_id = user_id
        self.admin = admin
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
        self.logger.info(f"Adding card: {name}")
        
        # Pokemon validation removed - focus on collection management
        # Users can add any card name they want
        
        # Create card data with defaults
        card_data = {
            'name': name.strip(),
            'set_name': set_name.strip() if set_name else "Unknown",
            'card_number': kwargs.get('card_number'),
            'rarity': kwargs.get('rarity'),
            'quantity': kwargs.get('quantity', 1),
            'is_favorite': kwargs.get('is_favorite', False),
            'date_added': datetime.now().isoformat(),
            'user_id': self.user_id if not self.admin else kwargs.get('user_id')  # Admin can specify user_id
        }
        
        # Validate using Pydantic model
        try:
            card_create = CardCreate(**card_data)
            validated_data = card_create.model_dump()
            self.logger.info(f"Validated card data: {validated_data}")
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            raise ValueError(f"Invalid card data: {e}")
        
        # Create the card
        card_id = self.repository.create(validated_data)
        self.logger.info(f"Card added successfully with ID: {card_id}")
        return card_id
    
    def get_card(self, card_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a card by ID"""
        self.logger.info(f"Getting card ID: {card_id}")
        return self.repository.find_by_id(card_id)
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """Get all cards"""
        self.logger.info("Getting all cards")
        return self.repository.find_all()
    
    def search_cards(self, name: str) -> List[Dict[str, Any]]:
        """Search cards by name"""
        self.logger.info(f"Searching cards by name: {name}")
        return self.repository.find_by_name(name)
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite cards"""
        self.logger.info("Getting favorite cards")
        return self.repository.find_favorites()
    
    def update_card(self, card_id: Union[int, str], **kwargs) -> bool:
        """Update a card with validation"""
        self.logger.info(f"Updating card ID: {card_id}")
        
        # Check if card exists
        existing_card = self.repository.find_by_id(card_id)
        if not existing_card:
            self.logger.error(f"Card ID {card_id} not found")
            return False
        
        # Prepare update data (only include provided fields)
        update_data = {}
        for key, value in kwargs.items():
            if value is not None:
                update_data[key] = value
        
        if not update_data:
            self.logger.warning("No fields to update")
            return False
        
        # Validate using Pydantic model
        try:
            # Merge with existing data for validation
            full_data = {**existing_card, **update_data}
            card_update = CardUpdate(**full_data)
            validated_data = card_update.model_dump(exclude_unset=True)
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            raise ValueError(f"Invalid update data: {e}")
        
        # Update the card
        success = self.repository.update(card_id, validated_data)
        if success:
            self.logger.info(f"Card {card_id} updated successfully")
        else:
            self.logger.error(f"Failed to update card {card_id}")
        
        return success
    
    def delete_card(self, card_id: Union[int, str]) -> bool:
        """Delete a card"""
        self.logger.info(f"Deleting card ID: {card_id}")
        
        # Check if card exists
        if not self.repository.find_by_id(card_id):
            self.logger.error(f"Card ID {card_id} not found")
            return False
        
        success = self.repository.delete(card_id)
        if success:
            self.logger.info(f"Card {card_id} deleted successfully")
        else:
            self.logger.error(f"Failed to delete card {card_id}")
        
        return success
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        self.logger.info("Getting collection statistics")
        return self.repository.get_stats()
    
    def toggle_favorite(self, card_id: Union[int, str]) -> bool:
        """Toggle favorite status of a card"""
        self.logger.info(f"Toggling favorite status for card ID: {card_id}")
        
        card = self.repository.find_by_id(card_id)
        if not card:
            self.logger.error(f"Card ID {card_id} not found")
            return False
        
        new_favorite_status = not card['is_favorite']
        return self.update_card(card_id, is_favorite=new_favorite_status)
    
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
        self.logger.info("Deleting all cards from collection")
        return self.repository.delete_all()
    
    def is_pokemon_api_available(self) -> bool:
        """Check if Pokemon TCG API is available"""
        return pokemon_api_service.is_api_available()
    
    # Type annotations updated to support both SQLite (int) and Supabase (str) IDs
