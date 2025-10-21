# Tests for Card Service functionality
import pytest
import sys
from pathlib import Path

# Add backend to path so we can import from it
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.card_service import CardService

def test_card_service_creation():
    """Test that CardService can be created"""
    service = CardService()
    assert service is not None
    assert hasattr(service, 'repository')

def test_add_card_basic():
    """Test adding a basic card"""
    service = CardService()
    
    # Add a simple card
    card_id = service.add_card(
        name="Test Charizard",
        set_name="Base Set",
        quantity=1
    )
    
    assert card_id is not None
    assert isinstance(card_id, (int, str))  # Could be int (SQLite) or str (Supabase)

def test_add_card_with_details():
    """Test adding a card with all details"""
    service = CardService()
    
    card_id = service.add_card(
        name="Pikachu",
        set_name="Base Set",
        card_number="58",
        rarity="Common",
        quantity=3,
        is_favorite=True
    )
    
    assert card_id is not None

def test_get_card():
    """Test retrieving a card"""
    service = CardService()
    
    # First add a card
    card_id = service.add_card(name="Test Card")
    
    # Then retrieve it
    card = service.get_card(card_id)
    assert card is not None
    assert card['name'] == "Test Card"

def test_get_all_cards():
    """Test getting all cards"""
    service = CardService()
    
    # Add a test card
    service.add_card(name="Test Card 1")
    service.add_card(name="Test Card 2")
    
    # Get all cards
    cards = service.get_all_cards()
    assert isinstance(cards, list)
    assert len(cards) >= 2

def test_search_cards():
    """Test searching cards by name"""
    service = CardService()
    
    # Add a card with specific name
    service.add_card(name="Charizard")
    
    # Search for it
    results = service.search_cards("Char")
    assert len(results) >= 1
    assert any(card['name'] == "Charizard" for card in results)

def test_update_card():
    """Test updating a card"""
    service = CardService()
    
    # Add a card
    card_id = service.add_card(name="Original Name")
    
    # Update it
    success = service.update_card(card_id, name="Updated Name", quantity=5)
    assert success is True
    
    # Verify the update
    updated_card = service.get_card(card_id)
    assert updated_card['name'] == "Updated Name"
    assert updated_card['quantity'] == 5

def test_toggle_favorite():
    """Test toggling favorite status"""
    service = CardService()
    
    # Add a card
    card_id = service.add_card(name="Test Card")
    
    # Toggle favorite
    success = service.toggle_favorite(card_id)
    assert success is True
    
    # Verify it's now favorite (SQLite stores booleans as integers)
    card = service.get_card(card_id)
    assert card['is_favorite'] in [True, 1]

def test_delete_card():
    """Test deleting a card"""
    service = CardService()
    
    # Add a card
    card_id = service.add_card(name="To Delete")
    
    # Delete it
    success = service.delete_card(card_id)
    assert success is True
    
    # Verify it's gone
    deleted_card = service.get_card(card_id)
    assert deleted_card is None

def test_get_stats():
    """Test getting collection statistics"""
    service = CardService()
    
    # Add some test cards
    service.add_card(name="Card 1", quantity=2)
    service.add_card(name="Card 2", quantity=1)
    
    # Get stats
    stats = service.get_collection_stats()
    assert 'total_cards' in stats
    assert 'total_quantity' in stats
    assert 'favorites' in stats
    assert stats['total_cards'] >= 2
    assert stats['total_quantity'] >= 3
