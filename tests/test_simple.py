# Simple, focused tests that actually work
import pytest
from backend.models.card import CardCreate, CardUpdate, Card

def test_card_create_model():
    """Test CardCreate model with defaults"""
    card = CardCreate(name="Test Card")
    
    assert card.name == "Test Card"
    assert card.set_name == "Unknown"
    assert card.quantity == 1
    assert card.is_favorite == False
    assert card.date_added is not None

def test_card_update_model():
    """Test CardUpdate model"""
    update = CardUpdate(name="Updated Name", quantity=5)
    
    assert update.name == "Updated Name"
    assert update.quantity == 5
    assert update.set_name is None

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
