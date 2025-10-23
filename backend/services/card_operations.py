"""
Shared card business logic operations
Pure functions that can be used by both CLI and API
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from models.card import CardCreate, CardUpdate
import logging

logger = logging.getLogger(__name__)

def validate_card_name(name: str) -> str:
    """Validate and clean card name"""
    if not name or not name.strip():
        raise ValueError("Card name cannot be empty")
    
    cleaned_name = name.strip()
    if len(cleaned_name) > 100:
        raise ValueError("Card name cannot exceed 100 characters")
    
    return cleaned_name

def validate_card_set(set_name: str) -> str:
    """Validate and clean card set name"""
    if not set_name:
        return "Unknown"
    
    cleaned_set = set_name.strip()
    if len(cleaned_set) > 100:
        raise ValueError("Set name cannot exceed 100 characters")
    
    return cleaned_set

def validate_card_quantity(quantity: int) -> int:
    """Validate card quantity"""
    if not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer")
    
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    
    if quantity > 999:
        raise ValueError("Quantity cannot exceed 999")
    
    return quantity

def validate_card_number(card_number: Optional[str]) -> Optional[str]:
    """Validate card number"""
    if not card_number:
        return None
    
    cleaned_number = card_number.strip()
    if len(cleaned_number) > 20:
        raise ValueError("Card number cannot exceed 20 characters")
    
    return cleaned_number

def validate_card_rarity(rarity: Optional[str]) -> Optional[str]:
    """Validate card rarity"""
    if not rarity:
        return None
    
    cleaned_rarity = rarity.strip()
    if len(cleaned_rarity) > 50:
        raise ValueError("Rarity cannot exceed 50 characters")
    
    return cleaned_rarity

def create_card_data(
    name: str,
    set_name: str = "Unknown",
    card_number: Optional[str] = None,
    rarity: Optional[str] = None,
    quantity: int = 1,
    is_favorite: bool = False,
    user_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create validated card data with business logic
    
    Args:
        name: Card name (required)
        set_name: Set name (default: "Unknown")
        card_number: Card number (optional)
        rarity: Card rarity (optional)
        quantity: Quantity (default: 1)
        is_favorite: Is favorite (default: False)
        user_id: User ID for multi-user support (optional)
        **kwargs: Additional fields
    
    Returns:
        Validated card data dictionary
    """
    logger.info(f"Creating card data for: {name}")
    
    # Validate and clean all fields
    validated_name = validate_card_name(name)
    validated_set = validate_card_set(set_name)
    validated_quantity = validate_card_quantity(quantity)
    validated_number = validate_card_number(card_number)
    validated_rarity = validate_card_rarity(rarity)
    
    # Create card data with defaults
    card_data = {
        'name': validated_name,
        'set_name': validated_set,
        'card_number': validated_number,
        'rarity': validated_rarity,
        'quantity': validated_quantity,
        'is_favorite': bool(is_favorite),
        'date_added': datetime.now().isoformat(),
        'user_id': user_id
    }
    
    # Add any additional fields
    card_data.update(kwargs)
    
    # Validate using Pydantic model
    try:
        card_create = CardCreate(**card_data)
        validated_data = card_create.model_dump()
        logger.info(f"Validated card data: {validated_data}")
        return validated_data
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise ValueError(f"Invalid card data: {e}")

def update_card_data(
    existing_card: Dict[str, Any],
    **updates
) -> Dict[str, Any]:
    """
    Update card data with validation
    
    Args:
        existing_card: Current card data
        **updates: Fields to update
    
    Returns:
        Updated and validated card data
    """
    logger.info(f"Updating card data for: {existing_card.get('name', 'Unknown')}")
    
    # Prepare update data (only include provided fields)
    update_data = {}
    for key, value in updates.items():
        if value is not None:
            update_data[key] = value
    
    if not update_data:
        logger.warning("No fields to update")
        return existing_card
    
    # Validate specific fields if they're being updated
    if 'name' in update_data:
        update_data['name'] = validate_card_name(update_data['name'])
    
    if 'set_name' in update_data:
        update_data['set_name'] = validate_card_set(update_data['set_name'])
    
    if 'quantity' in update_data:
        update_data['quantity'] = validate_card_quantity(update_data['quantity'])
    
    if 'card_number' in update_data:
        update_data['card_number'] = validate_card_number(update_data['card_number'])
    
    if 'rarity' in update_data:
        update_data['rarity'] = validate_card_rarity(update_data['rarity'])
    
    # Merge with existing data for validation
    full_data = {**existing_card, **update_data}
    
    # Validate using Pydantic model
    try:
        card_update = CardUpdate(**full_data)
        validated_data = card_update.model_dump(exclude_unset=True)
        logger.info(f"Validated update data: {validated_data}")
        return validated_data
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise ValueError(f"Invalid update data: {e}")

def format_card_display(card: Dict[str, Any]) -> str:
    """Format card for display"""
    name = card.get('name', 'Unknown')
    set_name = card.get('set_name', 'Unknown')
    quantity = card.get('quantity', 1)
    favorite = "⭐" if card.get('is_favorite') else ""
    
    return f"{name} ({set_name}) x{quantity} {favorite}".strip()

def calculate_collection_stats(cards: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate collection statistics from card list
    
    Args:
        cards: List of card dictionaries
    
    Returns:
        Statistics dictionary
    """
    if not cards:
        return {
            'total_cards': 0,
            'total_quantity': 0,
            'favorites': 0,
            'most_common_set': 'None',
            'unique_sets': 0
        }
    
    total_cards = len(cards)
    total_quantity = sum(card.get('quantity', 1) for card in cards)
    favorites = sum(1 for card in cards if card.get('is_favorite'))
    
    # Calculate most common set
    set_counts = {}
    for card in cards:
        set_name = card.get('set_name', 'Unknown')
        set_counts[set_name] = set_counts.get(set_name, 0) + 1
    
    most_common_set = max(set_counts.items(), key=lambda x: x[1])[0] if set_counts else 'None'
    unique_sets = len(set_counts)
    
    return {
        'total_cards': total_cards,
        'total_quantity': total_quantity,
        'favorites': favorites,
        'most_common_set': most_common_set,
        'unique_sets': unique_sets
    }

def search_cards_by_name(cards: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """
    Search cards by name (case-insensitive)
    
    Args:
        cards: List of card dictionaries
        search_term: Search term
    
    Returns:
        Filtered list of cards
    """
    if not search_term or not search_term.strip():
        return cards
    
    search_lower = search_term.lower().strip()
    
    return [
        card for card in cards
        if search_lower in card.get('name', '').lower()
    ]

def filter_favorite_cards(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter cards to only favorites
    
    Args:
        cards: List of card dictionaries
    
    Returns:
        List of favorite cards
    """
    return [card for card in cards if card.get('is_favorite', False)]

def sort_cards_by_name(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort cards alphabetically by name
    
    Args:
        cards: List of card dictionaries
    
    Returns:
        Sorted list of cards
    """
    return sorted(cards, key=lambda card: card.get('name', '').lower())

def sort_cards_by_date_added(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort cards by date added (newest first)
    
    Args:
        cards: List of card dictionaries
    
    Returns:
        Sorted list of cards
    """
    return sorted(
        cards, 
        key=lambda card: card.get('date_added', ''), 
        reverse=True
    )
