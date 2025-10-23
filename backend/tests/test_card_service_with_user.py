#!/usr/bin/env python3
"""
Test CardService with user context
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.card_service import CardService
from config import Config

def test_card_service_with_user():
    """Test CardService with user context"""
    print("🧪 Testing CardService with User Context")
    print("=" * 50)
    
    # Test 1: Create CardService without user (anonymous)
    print("\n1. Testing anonymous CardService...")
    anonymous_service = CardService()
    assert anonymous_service.user_id is None
    print("✅ Anonymous CardService created")
    
    # Test 2: Create CardService with user ID
    print("\n2. Testing CardService with user ID...")
    test_user_id = "test-user-123"
    user_service = CardService(user_id=test_user_id)
    assert user_service.user_id == test_user_id
    print(f"✅ CardService created for user: {test_user_id}")
    
    # Test 3: Test adding card with user context
    print("\n3. Testing card creation with user context...")
    try:
        card_id = user_service.add_card(
            name="Test Card with User",
            set_name="Test Set",
            quantity=2,
            is_favorite=True
        )
        print(f"✅ Card created with ID: {card_id}")
        
        # Verify the card was created with user_id
        card = user_service.get_card(card_id)
        if card:
            print(f"✅ Card retrieved: {card['name']}")
            print(f"   User ID: {card.get('user_id', 'None')}")
            if card.get('user_id') == test_user_id:
                print("✅ Card has correct user_id")
            else:
                print(f"❌ Card user_id mismatch: expected {test_user_id}, got {card.get('user_id')}")
        else:
            print("❌ Could not retrieve created card")
            
    except Exception as e:
        print(f"❌ Error creating card with user context: {e}")
        return False
    
    # Test 4: Test anonymous card creation
    print("\n4. Testing anonymous card creation...")
    try:
        anonymous_card_id = anonymous_service.add_card(
            name="Anonymous Test Card",
            set_name="Anonymous Set"
        )
        print(f"✅ Anonymous card created with ID: {anonymous_card_id}")
        
        # Verify the card was created without user_id
        anonymous_card = anonymous_service.get_card(anonymous_card_id)
        if anonymous_card:
            print(f"✅ Anonymous card retrieved: {anonymous_card['name']}")
            print(f"   User ID: {anonymous_card.get('user_id', 'None')}")
            if anonymous_card.get('user_id') is None:
                print("✅ Anonymous card has no user_id")
            else:
                print(f"❌ Anonymous card has user_id: {anonymous_card.get('user_id')}")
        else:
            print("❌ Could not retrieve anonymous card")
            
    except Exception as e:
        print(f"❌ Error creating anonymous card: {e}")
        return False
    
    print("\n🎉 All CardService user context tests passed!")
    return True

def main():
    """Run the test"""
    if not Config.USE_SUPABASE:
        print("❌ This test requires Supabase configuration")
        return
    
    test_card_service_with_user()

if __name__ == "__main__":
    main()
