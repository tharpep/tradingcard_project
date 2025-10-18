from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
from .base_service import BaseService
from .pokemon_api_service import pokemon_api_service
from repositories.card_repository import CardRepository
from models.card import Card, CardCreate, CardUpdate

logger = logging.getLogger(__name__)

class CardService(BaseService):
    """Service for card business logic"""
    
    def __init__(self):
        super().__init__()
        self.repository = CardRepository()
    
    def validate_pokemon_card(self, name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if a card name is a valid Pokemon card using the Pokemon TCG API
        
        Args:
            name: Card name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        self.logger.info(f"Validating Pokemon card: {name}")
        
        try:
            # Quick health check first to avoid long timeouts
            if not pokemon_api_service.is_api_available():
                self.logger.warning(f"Pokemon API unavailable, allowing card '{name}' without validation")
                return True, None
            
            is_valid, error_message = pokemon_api_service.validate_card_name(name)
            
            if is_valid:
                self.logger.info(f"Successfully validated Pokemon card: {name}")
                return True, None
            else:
                # Check if the error is due to API unavailability
                if error_message and "not responding" in error_message.lower():
                    self.logger.warning(f"Pokemon API unavailable, allowing card '{name}' without validation")
                    return True, None
                else:
                    self.logger.warning(f"Invalid Pokemon card: {name} - {error_message}")
                    return False, error_message
            
        except Exception as e:
            self.logger.error(f"Error validating Pokemon card '{name}': {e}")
            # If API is completely unavailable, allow the card but warn
            self.logger.warning(f"Pokemon API unavailable, allowing card '{name}' without validation")
            return True, None
    
    def add_card(self, name: str, set_name: str = "Unknown", validate_pokemon: bool = True, **kwargs) -> int:
        """Add a new card with business logic validation"""
        self.logger.info(f"Adding card: {name}")
        
        # Pokemon validation temporarily disabled - API reliability issues
        # TODO: Re-enable Pokemon validation when API is stable
        if validate_pokemon:
            self.logger.info(f"Pokemon validation skipped for '{name}' - API validation disabled")
        
        # Create card data with defaults
        card_data = {
            'name': name.strip(),
            'set_name': set_name.strip() if set_name else "Unknown",
            'card_number': kwargs.get('card_number'),
            'rarity': kwargs.get('rarity'),
            'quantity': kwargs.get('quantity', 1),
            'is_favorite': kwargs.get('is_favorite', False),
            'date_added': datetime.now().isoformat()
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
    
    def get_card(self, card_id: int) -> Optional[Dict[str, Any]]:
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
    
    def update_card(self, card_id: int, **kwargs) -> bool:
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
    
    def delete_card(self, card_id: int) -> bool:
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
    
    def toggle_favorite(self, card_id: int) -> bool:
        """Toggle favorite status of a card"""
        self.logger.info(f"Toggling favorite status for card ID: {card_id}")
        
        card = self.repository.find_by_id(card_id)
        if not card:
            self.logger.error(f"Card ID {card_id} not found")
            return False
        
        new_favorite_status = not card['is_favorite']
        return self.update_card(card_id, is_favorite=new_favorite_status)
    
    # Implement abstract methods from BaseService
    def create(self, data: Dict[str, Any]) -> int:
        """Create a new card (implements BaseService)"""
        return self.add_card(**data)
    
    def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a card by ID (implements BaseService)"""
        return self.get_card(record_id)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all cards (implements BaseService)"""
        return self.get_all_cards()
    
    def update(self, record_id: int, data: Dict[str, Any]) -> bool:
        """Update a card (implements BaseService)"""
        return self.update_card(record_id, **data)
    
    def delete(self, record_id: int) -> bool:
        """Delete a card (implements BaseService)"""
        return self.delete_card(record_id)
    
    def is_pokemon_api_available(self) -> bool:
        """Check if Pokemon TCG API is available"""
        return pokemon_api_service.is_api_available()
