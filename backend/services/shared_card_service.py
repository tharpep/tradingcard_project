"""
Shared card service interface
Common interface for both CLI and API to use
"""

from typing import List, Dict, Any, Optional, Union
import logging
from .card_operations import (
    create_card_data,
    update_card_data,
    calculate_collection_stats,
    search_cards_by_name,
    filter_favorite_cards,
    sort_cards_by_name,
    sort_cards_by_date_added
)
from repositories.repository_factory import get_card_repository

logger = logging.getLogger(__name__)

class SharedCardService:
    """
    Shared card service that provides common business logic
    for both CLI and API interfaces
    """
    
    def __init__(self, user_id: Optional[str] = None, admin: bool = False):
        """
        Initialize shared card service
        
        Args:
            user_id: User ID for multi-user support
            admin: Whether to run in admin mode (bypasses user restrictions)
        """
        self.repository = get_card_repository()
        self.user_id = user_id
        self.admin = admin
        
        if admin:
            logger.info("SharedCardService initialized in ADMIN mode - full system access")
        elif user_id:
            logger.info(f"SharedCardService initialized for user: {user_id}")
        else:
            logger.info("SharedCardService initialized without user context (anonymous)")
    
    def add_card(
        self,
        name: str,
        set_name: str = "Unknown",
        card_number: Optional[str] = None,
        rarity: Optional[str] = None,
        quantity: int = 1,
        is_favorite: bool = False,
        **kwargs
    ) -> Union[int, str]:
        """
        Add a new card with business logic validation
        
        Args:
            name: Card name (required)
            set_name: Set name (default: "Unknown")
            card_number: Card number (optional)
            rarity: Card rarity (optional)
            quantity: Quantity (default: 1)
            is_favorite: Is favorite (default: False)
            **kwargs: Additional fields
        
        Returns:
            Card ID
        """
        logger.info(f"Adding card: {name}")
        
        # Create validated card data
        card_data = create_card_data(
            name=name,
            set_name=set_name,
            card_number=card_number,
            rarity=rarity,
            quantity=quantity,
            is_favorite=is_favorite,
            user_id=self.user_id if not self.admin else kwargs.get('user_id'),
            **kwargs
        )
        
        # Create the card
        card_id = self.repository.create(card_data)
        logger.info(f"Card added successfully with ID: {card_id}")
        return card_id
    
    def get_card(self, card_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a card by ID"""
        logger.info(f"Getting card ID: {card_id}")
        return self.repository.find_by_id(card_id)
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """Get all cards"""
        logger.info("Getting all cards")
        return self.repository.find_all()
    
    def search_cards(self, name: str) -> List[Dict[str, Any]]:
        """Search cards by name"""
        logger.info(f"Searching cards by name: {name}")
        return self.repository.find_by_name(name)
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite cards"""
        logger.info("Getting favorite cards")
        return self.repository.find_favorites()
    
    def update_card(self, card_id: Union[int, str], **kwargs) -> bool:
        """
        Update a card with validation
        
        Args:
            card_id: Card ID to update
            **kwargs: Fields to update
        
        Returns:
            Success status
        """
        logger.info(f"Updating card ID: {card_id}")
        
        # Check if card exists
        existing_card = self.repository.find_by_id(card_id)
        if not existing_card:
            logger.error(f"Card ID {card_id} not found")
            return False
        
        # Prepare update data (only include provided fields)
        update_data = {}
        for key, value in kwargs.items():
            if value is not None:
                update_data[key] = value
        
        if not update_data:
            logger.warning("No fields to update")
            return False
        
        # Validate and prepare update data
        validated_data = update_card_data(existing_card, **update_data)
        
        # Update the card
        success = self.repository.update(card_id, validated_data)
        if success:
            logger.info(f"Card {card_id} updated successfully")
        else:
            logger.error(f"Failed to update card {card_id}")
        
        return success
    
    def delete_card(self, card_id: Union[int, str]) -> bool:
        """Delete a card"""
        logger.info(f"Deleting card ID: {card_id}")
        
        # Check if card exists
        if not self.repository.find_by_id(card_id):
            logger.error(f"Card ID {card_id} not found")
            return False
        
        success = self.repository.delete(card_id)
        if success:
            logger.info(f"Card {card_id} deleted successfully")
        else:
            logger.error(f"Failed to delete card {card_id}")
        
        return success
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        logger.info("Getting collection statistics")
        return self.repository.get_stats()
    
    def toggle_favorite(self, card_id: Union[int, str]) -> bool:
        """Toggle favorite status of a card"""
        logger.info(f"Toggling favorite status for card ID: {card_id}")
        
        card = self.repository.find_by_id(card_id)
        if not card:
            logger.error(f"Card ID {card_id} not found")
            return False
        
        new_favorite_status = not card['is_favorite']
        return self.update_card(card_id, is_favorite=new_favorite_status)
    
    def delete_all_cards(self) -> int:
        """Delete all cards from the collection"""
        logger.info("Deleting all cards from collection")
        return self.repository.delete_all()
    
    # Utility methods for display and formatting
    def get_cards_for_display(
        self,
        search_term: Optional[str] = None,
        favorites_only: bool = False,
        sort_by: str = "name"
    ) -> List[Dict[str, Any]]:
        """
        Get cards formatted for display with filtering and sorting
        
        Args:
            search_term: Optional search term
            favorites_only: Show only favorites
            sort_by: Sort by 'name' or 'date_added'
        
        Returns:
            Formatted list of cards
        """
        # Get all cards
        cards = self.get_all_cards()
        
        # Apply filters
        if favorites_only:
            cards = filter_favorite_cards(cards)
        
        if search_term:
            cards = search_cards_by_name(cards, search_term)
        
        # Apply sorting
        if sort_by == "name":
            cards = sort_cards_by_name(cards)
        elif sort_by == "date_added":
            cards = sort_cards_by_date_added(cards)
        
        return cards
    
    def get_formatted_stats(self) -> Dict[str, Any]:
        """Get formatted collection statistics"""
        stats = self.get_collection_stats()
        
        # Add additional calculated stats
        cards = self.get_all_cards()
        additional_stats = calculate_collection_stats(cards)
        
        # Merge stats
        formatted_stats = {**stats, **additional_stats}
        
        return formatted_stats
