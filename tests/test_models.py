# Tests for Pydantic models
import pytest
from datetime import datetime
from backend.models.card import CardCreate, CardUpdate, Card

def test_card_create_defaults():
    """Test CardCreate with minimal data"""
    card = CardCreate(name="Test Card")
    
    assert card.name == "Test Card"
    assert card.set_name == "Unknown"
    assert card.quantity == 1
    assert card.is_favorite == False
    assert card.date_added is not None

def test_card_create_full_data():
    """Test CardCreate with all data"""
    card = CardCreate(
        name="Charizard",
        set_name="Base Set",
        card_number="4",
        rarity="Rare Holo",
        quantity=2,
        is_favorite=True
    )
    
    assert card.name == "Charizard"
    assert card.set_name == "Base Set"
    assert card.card_number == "4"
    assert card.rarity == "Rare Holo"
    assert card.quantity == 2
    assert card.is_favorite == True

def test_card_update_partial():
    """Test CardUpdate with partial data"""
    update = CardUpdate(name="Updated Name", quantity=5)
    
    assert update.name == "Updated Name"
    assert update.quantity == 5
    assert update.set_name is None
    assert update.is_favorite is None

def test_card_model():
    """Test complete Card model"""
    card = Card(
        id=1,
        name="Pikachu",
        set_name="Base Set",
        card_number="58",
        rarity="Common",
        quantity=3,
        is_favorite=True,
        date_added="2024-01-01T12:00:00"
    )
    
    assert card.id == 1
    assert card.name == "Pikachu"
    assert card.quantity == 3
    assert card.is_favorite == True
