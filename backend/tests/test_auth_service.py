#!/usr/bin/env python3
"""
Test script for AuthService
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from config import Config

# Try to import auth_service, handle import error gracefully
try:
    from services.auth_service import auth_service
    AUTH_SERVICE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  AuthService import failed: {e}")
    print("This is likely because the supabase package is not installed in the current environment")
    AUTH_SERVICE_AVAILABLE = False
    auth_service = None

def test_auth_service_initialization():
    """Test that AuthService initializes correctly"""
    print("Testing AuthService initialization...")
    
    if not AUTH_SERVICE_AVAILABLE:
        print("❌ AuthService not available - supabase package not installed")
        return False
    
    # Check Supabase config
    print(f"Supabase URL: {Config.SUPABASE_URL}")
    print(f"Supabase Key: {'SET' if Config.SUPABASE_KEY else 'NOT SET'}")
    
    # Test service creation
    try:
        service = auth_service
        print("✅ AuthService initialized successfully")
        return True
    except Exception as e:
        print(f"❌ AuthService initialization failed: {e}")
        return False

def test_user_registration():
    """Test user registration (will fail if user already exists)"""
    print("\nTesting user registration...")
    
    test_email = "test@example.com"
    test_password = "testpassword123"
    test_username = "testuser"
    
    try:
        result = auth_service.sign_up(test_email, test_password, test_username)
        
        if result.get("success"):
            print("✅ User registration successful")
            print(f"   User ID: {result['user'].id}")
            print(f"   Username: {result['profile']['username']}")
            return True
        else:
            print(f"❌ User registration failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_user_sign_in():
    """Test user sign in"""
    print("\nTesting user sign in...")
    
    test_email = "test@example.com"
    test_password = "testpassword123"
    
    try:
        result = auth_service.sign_in(test_email, test_password)
        
        if result.get("success"):
            print("✅ User sign in successful")
            print(f"   User ID: {result['user'].id}")
            print(f"   Username: {result['profile']['username']}")
            print(f"   Access Token: {result['session'].access_token[:20]}...")
            return result['session'].access_token
        else:
            print(f"❌ User sign in failed: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Sign in error: {e}")
        return None

def test_token_validation():
    """Test token validation"""
    print("\nTesting token validation...")
    
    if not AUTH_SERVICE_AVAILABLE:
        print("❌ AuthService not available - cannot test token validation")
        return
    
    # First sign in to get a token
    test_email = "test@example.com"
    test_password = "testpassword123"
    
    try:
        # Sign in to get token
        sign_in_result = auth_service.sign_in(test_email, test_password)
        
        if not sign_in_result.get("success"):
            print("❌ Token validation failed - could not sign in")
            return
        
        token = sign_in_result['session'].access_token
        
        # Now test token validation
        result = auth_service.get_user_from_token(token)
        
        if result:
            print("✅ Token validation successful")
            print(f"   User ID: {result['user'].id}")
            print(f"   Username: {result['profile']['username']}")
        else:
            print("❌ Token validation failed")
            
    except Exception as e:
        print(f"❌ Token validation error: {e}")

def main():
    """Run all auth service tests"""
    print("🔐 AuthService Test Suite")
    print("=" * 40)
    
    if not AUTH_SERVICE_AVAILABLE:
        print("❌ AuthService not available - cannot run tests")
        print("Please install supabase package: pip install supabase==2.3.4")
        return
    
    # Test 1: Initialization
    if not test_auth_service_initialization():
        print("\n❌ AuthService initialization failed - stopping tests")
        return
    
    # Test 2: Registration (may fail if user exists)
    test_user_registration()
    
    # Test 3: Sign in
    token = test_user_sign_in()
    if not token:
        print("\n❌ Sign in failed - stopping tests")
        return
    
    # Test 4: Token validation
    test_token_validation(token)
    
    print("\n🎉 AuthService tests completed!")

if __name__ == "__main__":
    main()
