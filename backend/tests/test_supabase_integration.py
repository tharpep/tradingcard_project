# Comprehensive Supabase integration tests
import pytest
import sys
import os
from pathlib import Path
from datetime import datetime

# Add backend to path so we can import from it
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from config import Config
from repositories.repository_factory import get_card_repository
from services.card_service import CardService

def test_supabase_configuration():
    """Test that Supabase configuration is properly set"""
    print(f"Database Type: {Config.get_database_type()}")
    print(f"USE_SUPABASE: {Config.USE_SUPABASE}")
    print(f"SUPABASE_URL: {Config.SUPABASE_URL}")
    print(f"SUPABASE_KEY: {'SET' if Config.SUPABASE_KEY else 'NOT SET'}")
    
    # Should be using Supabase
    assert Config.USE_SUPABASE is True
    assert Config.get_database_type() == "supabase"
    assert Config.SUPABASE_URL is not None
    assert Config.SUPABASE_KEY is not None
    
    # Validate configuration
    assert Config.validate_supabase_config() is True

def test_supabase_connection_detailed():
    """Test Supabase connection with detailed error reporting"""
    print("🔍 Testing Supabase Configuration...")
    print("=" * 50)
    
    # Check configuration
    print(f"Database Type: {Config.get_database_type()}")
    print(f"USE_SUPABASE: {Config.USE_SUPABASE}")
    print(f"SUPABASE_URL: {Config.SUPABASE_URL}")
    print(f"SUPABASE_KEY: {'SET' if Config.SUPABASE_KEY else 'NOT SET'}")
    
    if not Config.SUPABASE_URL:
        pytest.fail("❌ SUPABASE_URL not set")
        
    if not Config.SUPABASE_KEY:
        pytest.fail("❌ SUPABASE_KEY not set")
    
    # Validate URL format
    if not Config.SUPABASE_URL.startswith('https://') or '.supabase.co' not in Config.SUPABASE_URL:
        pytest.fail("❌ SUPABASE_URL format appears invalid")
    
    # Check key format
    if not Config.SUPABASE_KEY.startswith('eyJ'):
        pytest.fail("❌ SUPABASE_KEY format appears invalid (should start with 'eyJ')")
    
    print("✅ Configuration looks valid")
    
    # Test actual connection
    try:
        from supabase import create_client, Client

        print("\n🔗 Testing Supabase Connection...")
        print(f"URL: {Config.SUPABASE_URL}")
        print(f"Key: {'SET' if Config.SUPABASE_KEY else 'NOT SET'}")

        client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

        # Try a simple query
        result = client.table('cards').select('*').limit(1).execute()
        print("✅ Supabase connection successful!")
        print(f"Found {len(result.data)} cards in database")

    except ImportError as e:
        print(f"❌ Supabase module not available: {e}")
        print("💡 This is expected if supabase package is not installed")
        print("✅ Configuration is valid, but cannot test actual connection")
        return  # Skip the test gracefully
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Provide specific guidance based on error
        if "Invalid API key" in str(e):
            print("\n💡 Troubleshooting 'Invalid API key':")
            print("1. Make sure you're using the 'anon' key, not 'service_role'")
            print("2. Check that the key is copied correctly (no extra spaces)")
            print("3. Verify the key is from the correct project")
            print("4. Try regenerating the key in Supabase dashboard")
        elif "Connection" in str(e) or "Network" in str(e):
            print("\n💡 Troubleshooting connection issues:")
            print("1. Check your internet connection")
            print("2. Verify the SUPABASE_URL is correct")
            print("3. Make sure the project is active (not paused)")
        
        pytest.fail(f"Supabase connection failed: {e}")

def test_supabase_repository_creation():
    """Test that Supabase repository can be created"""
    repo = get_card_repository()
    assert repo is not None
    assert hasattr(repo, 'create')
    assert hasattr(repo, 'find_by_id')
    assert hasattr(repo, 'find_all')
    assert hasattr(repo, 'update')
    assert hasattr(repo, 'delete')
    
    # Should be Supabase repository, not SQLite
    from repositories.supabase_card_repository import SupabaseCardRepository
    assert isinstance(repo, SupabaseCardRepository)

def test_supabase_connection():
    """Test basic Supabase connection"""
    repo = get_card_repository()
    
    # Try to get all cards (this tests the connection)
    try:
        cards = repo.find_all()
        assert isinstance(cards, list)
        print(f"✅ Supabase connection successful. Found {len(cards)} existing cards.")
    except Exception as e:
        pytest.fail(f"Supabase connection failed: {e}")

def test_supabase_create_card():
    """Test creating a card in Supabase"""
    repo = get_card_repository()
    
    card_data = {
        'name': 'Supabase Test Card',
        'set_name': 'Test Set',
        'card_number': 'TEST-001',
        'rarity': 'Common',
        'quantity': 1,
        'is_favorite': False,
        'date_added': datetime.now().isoformat()
    }
    
    try:
        card_id = repo.create(card_data)
        assert card_id is not None
        assert isinstance(card_id, str)  # Supabase uses UUID strings
        print(f"✅ Card created with ID: {card_id}")
        return card_id
    except Exception as e:
        pytest.fail(f"Failed to create card in Supabase: {e}")

def test_supabase_find_card():
    """Test finding a card in Supabase"""
    repo = get_card_repository()
    
    # First create a card
    card_data = {
        'name': 'Find Test Card',
        'set_name': 'Find Set',
        'quantity': 2,
        'date_added': datetime.now().isoformat()
    }
    card_id = repo.create(card_data)
    
    # Then find it
    try:
        found_card = repo.find_by_id(card_id)
        assert found_card is not None
        assert found_card['name'] == 'Find Test Card'
        assert found_card['quantity'] == 2
        print(f"✅ Card found: {found_card['name']}")
        return card_id
    except Exception as e:
        pytest.fail(f"Failed to find card in Supabase: {e}")

def test_supabase_update_card():
    """Test updating a card in Supabase"""
    repo = get_card_repository()
    
    # Create a card
    card_data = {
        'name': 'Update Test Card',
        'set_name': 'Update Set',
        'quantity': 1,
        'date_added': datetime.now().isoformat()
    }
    card_id = repo.create(card_data)
    
    # Update it
    update_data = {
        'name': 'Updated Card Name',
        'quantity': 5,
        'is_favorite': True
    }
    
    try:
        success = repo.update(card_id, update_data)
        assert success is True
        
        # Verify the update
        updated_card = repo.find_by_id(card_id)
        assert updated_card['name'] == 'Updated Card Name'
        assert updated_card['quantity'] == 5
        assert updated_card['is_favorite'] is True
        print(f"✅ Card updated successfully: {updated_card['name']}")
        return card_id
    except Exception as e:
        pytest.fail(f"Failed to update card in Supabase: {e}")

def test_supabase_delete_card():
    """Test deleting a card in Supabase"""
    repo = get_card_repository()
    
    # Create a card
    card_data = {
        'name': 'Delete Test Card',
        'set_name': 'Delete Set',
        'quantity': 1,
        'date_added': datetime.now().isoformat()
    }
    card_id = repo.create(card_data)
    
    # Delete it
    try:
        success = repo.delete(card_id)
        assert success is True
        
        # Verify it's gone
        deleted_card = repo.find_by_id(card_id)
        assert deleted_card is None
        print(f"✅ Card deleted successfully")
    except Exception as e:
        pytest.fail(f"Failed to delete card in Supabase: {e}")

def test_supabase_get_all_cards():
    """Test getting all cards from Supabase"""
    repo = get_card_repository()
    
    # Create some test cards
    test_cards = [
        {'name': 'All Cards Test 1', 'set_name': 'Set 1', 'date_added': datetime.now().isoformat()},
        {'name': 'All Cards Test 2', 'set_name': 'Set 2', 'date_added': datetime.now().isoformat()}
    ]
    
    created_ids = []
    for card_data in test_cards:
        card_id = repo.create(card_data)
        created_ids.append(card_id)
    
    try:
        all_cards = repo.find_all()
        assert isinstance(all_cards, list)
        assert len(all_cards) >= 2
        
        # Check that our test cards are in the results
        test_card_names = [card['name'] for card in all_cards if 'All Cards Test' in card['name']]
        assert len(test_card_names) >= 2
        print(f"✅ Found {len(all_cards)} total cards, including test cards")
        
        return created_ids
    except Exception as e:
        pytest.fail(f"Failed to get all cards from Supabase: {e}")

def test_supabase_card_service():
    """Test card service with Supabase backend"""
    service = CardService()
    
    try:
        # Test adding a card through service
        card_id = service.add_card(
            name="Service Test Card",
            set_name="Service Set",
            quantity=3,
            is_favorite=True
        )
        assert card_id is not None
        assert isinstance(card_id, str)  # Supabase returns UUID strings
        
        # Test getting the card
        card = service.get_card(card_id)
        assert card is not None
        assert card['name'] == "Service Test Card"
        assert card['quantity'] == 3
        assert card['is_favorite'] is True
        
        # Test updating the card
        success = service.update_card(card_id, name="Updated Service Card", quantity=5)
        assert success is True
        
        # Verify update
        updated_card = service.get_card(card_id)
        assert updated_card['name'] == "Updated Service Card"
        assert updated_card['quantity'] == 5
        
        # Test deleting the card
        delete_success = service.delete_card(card_id)
        assert delete_success is True
        
        # Verify deletion
        deleted_card = service.get_card(card_id)
        assert deleted_card is None
        
        print(f"✅ Card service works with Supabase backend")
        return card_id
    except Exception as e:
        pytest.fail(f"Card service failed with Supabase: {e}")

def test_supabase_search_cards():
    """Test searching cards in Supabase"""
    service = CardService()
    
    try:
        # Add a card with specific name
        card_id = service.add_card(name="Search Test Charizard", set_name="Search Set")
        
        # Search for it
        results = service.search_cards("Char")
        assert len(results) >= 1
        assert any(card['name'] == "Search Test Charizard" for card in results)
        
        # Clean up
        service.delete_card(card_id)
        print(f"✅ Card search works with Supabase")
    except Exception as e:
        pytest.fail(f"Card search failed with Supabase: {e}")

def test_supabase_get_stats():
    """Test getting statistics from Supabase"""
    service = CardService()
    
    try:
        # Add some test cards
        service.add_card(name="Stats Test 1", quantity=2)
        service.add_card(name="Stats Test 2", quantity=1)
        
        # Get stats
        stats = service.get_collection_stats()
        assert 'total_cards' in stats
        assert 'total_quantity' in stats
        assert 'favorites' in stats
        assert stats['total_cards'] >= 2
        assert stats['total_quantity'] >= 3
        
        print(f"✅ Statistics work with Supabase: {stats}")
    except Exception as e:
        pytest.fail(f"Statistics failed with Supabase: {e}")

def test_supabase_cleanup():
    """Clean up test data from Supabase"""
    service = CardService()
    
    try:
        # Get all cards and delete test cards
        all_cards = service.get_all_cards()
        test_cards = [card for card in all_cards if 'Test' in card['name'] or 'test' in card['name']]
        
        for card in test_cards:
            service.delete_card(card['id'])
        
        print(f"✅ Cleaned up {len(test_cards)} test cards from Supabase")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

# Run cleanup after all tests
def test_supabase_final_cleanup():
    """Final cleanup of all test data"""
    test_supabase_cleanup()
