#!/usr/bin/env python3
"""
Test CLI authentication functionality
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from config import Config

def test_cli_auth_imports():
    """Test that CLI authentication functions can be imported"""
    print("🧪 Testing CLI Authentication Imports")
    print("=" * 40)
    
    try:
        # Test importing the CLI functions
        from run import authenticate_user, logout_user, get_card_service
        print("✅ CLI authentication functions imported successfully")
        
        # Test CardService initialization
        from services.card_service import CardService
        
        # Test anonymous CardService
        anonymous_service = CardService()
        assert anonymous_service.user_id is None
        print("✅ Anonymous CardService works")
        
        # Test user CardService
        user_service = CardService(user_id="test-user-123")
        assert user_service.user_id == "test-user-123"
        print("✅ User CardService works")
        
        print("\n🎉 CLI authentication imports test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cli_auth_functions():
    """Test CLI authentication function logic"""
    print("\n🧪 Testing CLI Authentication Functions")
    print("=" * 40)
    
    try:
        from run import get_card_service
        
        # Test get_card_service function
        service = get_card_service()
        assert service is not None
        print("✅ get_card_service() works")
        
        # Test that it returns a CardService instance
        from services.card_service import CardService
        assert isinstance(service, CardService)
        print("✅ get_card_service() returns CardService instance")
        
        print("\n🎉 CLI authentication functions test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing CLI functions: {e}")
        return False

def main():
    """Run all CLI authentication tests"""
    print("🔐 CLI Authentication Test Suite")
    print("=" * 50)
    
    if not Config.USE_SUPABASE:
        print("ℹ️  Supabase not configured - testing basic functionality only")
    
    # Test 1: Import functionality
    if not test_cli_auth_imports():
        print("\n❌ Import tests failed")
        return
    
    # Test 2: Function logic
    if not test_cli_auth_functions():
        print("\n❌ Function tests failed")
        return
    
    print("\n🎉 All CLI authentication tests passed!")

if __name__ == "__main__":
    main()
