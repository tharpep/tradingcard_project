# Tests for database operations
import pytest
import sys
from pathlib import Path

# Add backend to path so we can import from it
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from repositories.repository_factory import get_card_repository
from config import Config

def test_repository_creation():
    """Test that repository can be created"""
    repo = get_card_repository()
    assert repo is not None
    assert hasattr(repo, 'create')
    assert hasattr(repo, 'find_by_id')
    assert hasattr(repo, 'find_all')

def test_database_type():
    """Test that we're using the correct database type"""
    db_type = Config.get_database_type()
    assert db_type in ['sqlite', 'supabase']
    
    # Should default to SQLite if no Supabase config
    if not Config.USE_SUPABASE:
        assert db_type == 'sqlite'

def test_create_card():
    """Test creating a card in the database"""
    repo = get_card_repository()
    
    card_data = {
        'name': 'Test Card',
        'set_name': 'Test Set',
        'quantity': 1,
        'is_favorite': False,
        'date_added': '2024-01-01T12:00:00'
    }
    
    card_id = repo.create(card_data)
    assert card_id is not None
    assert isinstance(card_id, (int, str))

def test_find_card_by_id():
    """Test finding a card by ID"""
    repo = get_card_repository()
    
    # Create a card
    card_data = {
        'name': 'Find Test Card',
        'set_name': 'Test Set',
        'quantity': 1,
        'date_added': '2024-01-01T12:00:00'
    }
    card_id = repo.create(card_data)
    
    # Find it
    found_card = repo.find_by_id(card_id)
    assert found_card is not None
    assert found_card['name'] == 'Find Test Card'

def test_find_all_cards():
    """Test finding all cards"""
    repo = get_card_repository()
    
    # Create some test cards
    repo.create({'name': 'Card 1', 'set_name': 'Set 1', 'date_added': '2024-01-01T12:00:00'})
    repo.create({'name': 'Card 2', 'set_name': 'Set 2', 'date_added': '2024-01-01T12:00:00'})
    
    # Get all cards
    all_cards = repo.find_all()
    assert isinstance(all_cards, list)
    assert len(all_cards) >= 2

def test_update_card():
    """Test updating a card"""
    repo = get_card_repository()
    
    # Create a card
    card_data = {'name': 'Original Name', 'set_name': 'Original Set', 'date_added': '2024-01-01T12:00:00'}
    card_id = repo.create(card_data)
    
    # Update it
    update_data = {'name': 'Updated Name', 'quantity': 5}
    success = repo.update(card_id, update_data)
    assert success is True
    
    # Verify the update
    updated_card = repo.find_by_id(card_id)
    assert updated_card['name'] == 'Updated Name'
    assert updated_card['quantity'] == 5

def test_delete_card():
    """Test deleting a card"""
    repo = get_card_repository()
    
    # Create a card
    card_data = {'name': 'To Delete', 'set_name': 'Test Set', 'date_added': '2024-01-01T12:00:00'}
    card_id = repo.create(card_data)
    
    # Delete it
    success = repo.delete(card_id)
    assert success is True
    
    # Verify it's gone
    deleted_card = repo.find_by_id(card_id)
    assert deleted_card is None

def test_get_stats():
    """Test getting database statistics"""
    repo = get_card_repository()
    
    # Create some test data
    repo.create({'name': 'Stats Card 1', 'quantity': 2, 'date_added': '2024-01-01T12:00:00'})
    repo.create({'name': 'Stats Card 2', 'quantity': 1, 'date_added': '2024-01-01T12:00:00'})
    
    # Get stats
    stats = repo.get_stats()
    assert 'total_cards' in stats
    assert 'total_quantity' in stats
    assert 'favorites' in stats
    assert stats['total_cards'] >= 2
    assert stats['total_quantity'] >= 3
