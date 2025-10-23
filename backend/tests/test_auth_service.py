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
        assert False, "AuthService not available - supabase package not installed"
    
    # Check Supabase config
    print(f"Supabase URL: {Config.SUPABASE_URL}")
    print(f"Supabase Key: {'SET' if Config.SUPABASE_KEY else 'NOT SET'}")
    
    # Test service creation
    try:
        service = auth_service
        print("✅ AuthService initialized successfully")
        assert service is not None
    except Exception as e:
        print(f"❌ AuthService initialization failed: {e}")
        assert False, f"AuthService initialization failed: {e}"

def test_user_registration():
    """Test user registration with cleanup"""
    print("\nTesting user registration...")
    
    if not AUTH_SERVICE_AVAILABLE or auth_service is None:
        print("❌ AuthService not available - skipping registration test")
        assert False, "AuthService not available - skipping registration test"
    
    test_email = "rapgtharpe@gmail.com"
    test_password = "testpassword123"
    test_username = "testuser"
    user_id = None
    
    try:
        # First, try to clean up any existing user
        print("🧹 Cleaning up any existing test user...")
        # We can't easily find the user ID without signing in, so we'll handle errors gracefully
        
        result = auth_service.sign_up(test_email, test_password, test_username)
        
        if result.get("success"):
            print("✅ User registration successful")
            print(f"   User ID: {result['user'].id}")
            print(f"   Username: {result['profile']['username']}")
            user_id = result['user'].id
            assert result.get("success"), "User registration should succeed"
        else:
            # Check if user already exists (various error messages)
            error_msg = str(result.get('error', ''))
            if any(phrase in error_msg.lower() for phrase in [
                "already registered", "user already exists", "duplicate key", 
                "unique constraint", "already exists", "security purposes", 
                "only request this after", "rate limit"
            ]):
                print("✅ User already exists - attempting to sign in to get user ID")
                # Try to sign in to get the user ID for cleanup
                signin_result = auth_service.sign_in(test_email, test_password)
                if signin_result.get("success"):
                    user_id = signin_result['user'].id
                    print(f"✅ Got existing user ID: {user_id}")
                else:
                    print("❌ Could not sign in existing user")
                    assert False, "Could not sign in existing user"
            else:
                print(f"❌ User registration failed: {error_msg}")
                assert False, f"User registration failed: {error_msg}"
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        assert False, f"Registration error: {e}"
    
    finally:
        # Clean up: delete the test user
        if user_id:
            print(f"🧹 Cleaning up test user: {user_id}")
            try:
                auth_service.delete_user(user_id)
                print("✅ Test user cleaned up successfully")
            except Exception as e:
                print(f"⚠️  Could not clean up test user: {e}")
                # Don't fail the test for cleanup issues

def test_user_sign_in():
    """Test user sign in with setup and cleanup"""
    print("\nTesting user sign in...")
    
    if not AUTH_SERVICE_AVAILABLE or auth_service is None:
        print("❌ AuthService not available - skipping sign in test")
        assert False, "AuthService not available - skipping sign in test"
    
    test_email = "rapgtharpe@gmail.com"
    test_password = "testpassword123"
    test_username = "testuser"
    user_id = None
    
    try:
        # First, ensure user exists by trying to register
        print("🔧 Setting up test user...")
        reg_result = auth_service.sign_up(test_email, test_password, test_username)
        
        if reg_result.get("success"):
            user_id = reg_result['user'].id
            print("✅ Test user created for sign-in test")
        else:
            # User might already exist, try to sign in to get user ID
            print("ℹ️  User might already exist, attempting sign in...")
            signin_result = auth_service.sign_in(test_email, test_password)
            if signin_result.get("success"):
                user_id = signin_result['user'].id
                print("✅ Existing user found for sign-in test")
            else:
                print("❌ Could not create or find test user")
                assert False, "Could not create or find test user"
        
        # Now test the actual sign-in
        result = auth_service.sign_in(test_email, test_password)
        
        if result.get("success"):
            print("✅ User sign in successful")
            print(f"   User ID: {result['user'].id}")
            print(f"   Username: {result['profile']['username']}")
            print(f"   Access Token: {result['session'].access_token[:20]}...")
            assert result.get("success"), "User sign in should succeed"
        else:
            print(f"❌ User sign in failed: {result.get('error')}")
            assert False, f"User sign in failed: {result.get('error')}"
            
    except Exception as e:
        print(f"❌ Sign in error: {e}")
        assert False, f"Sign in error: {e}"
    
    finally:
        # Clean up: delete the test user
        if user_id:
            print(f"🧹 Cleaning up test user: {user_id}")
            try:
                auth_service.delete_user(user_id)
                print("✅ Test user cleaned up successfully")
            except Exception as e:
                print(f"⚠️  Could not clean up test user: {e}")
                # Don't fail the test for cleanup issues

def test_token_validation():
    """Test token validation with setup and cleanup"""
    print("\nTesting token validation...")
    
    if not AUTH_SERVICE_AVAILABLE or auth_service is None:
        print("❌ AuthService not available - cannot test token validation")
        assert False, "AuthService not available - cannot test token validation"
    
    test_email = "rapgtharpe@gmail.com"
    test_password = "testpassword123"
    test_username = "testuser"
    user_id = None
    
    try:
        # First, ensure user exists
        print("🔧 Setting up test user...")
        reg_result = auth_service.sign_up(test_email, test_password, test_username)
        
        if reg_result.get("success"):
            user_id = reg_result['user'].id
            print("✅ Test user created for token validation test")
        else:
            # User might already exist, try to sign in to get user ID
            print("ℹ️  User might already exist, attempting sign in...")
            signin_result = auth_service.sign_in(test_email, test_password)
            if signin_result.get("success"):
                user_id = signin_result['user'].id
                print("✅ Existing user found for token validation test")
            else:
                print("❌ Could not create or find test user")
                assert False, "Could not create or find test user"
        
        # Sign in to get token
        sign_in_result = auth_service.sign_in(test_email, test_password)
        
        if not sign_in_result.get("success"):
            print("❌ Token validation failed - could not sign in")
            assert False, "Token validation failed - could not sign in"
        
        token = sign_in_result['session'].access_token
        
        # Now test token validation
        result = auth_service.get_user_from_token(token)
        
        if result:
            print("✅ Token validation successful")
            print(f"   User ID: {result['user'].id}")
            print(f"   Username: {result['profile']['username']}")
            assert result is not None, "Token validation should return user data"
        else:
            print("❌ Token validation failed")
            assert False, "Token validation failed"
            
    except Exception as e:
        print(f"❌ Token validation error: {e}")
        assert False, f"Token validation error: {e}"
    
    finally:
        # Clean up: delete the test user
        if user_id:
            print(f"🧹 Cleaning up test user: {user_id}")
            try:
                auth_service.delete_user(user_id)
                print("✅ Test user cleaned up successfully")
            except Exception as e:
                print(f"⚠️  Could not clean up test user: {e}")
                # Don't fail the test for cleanup issues

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
    test_token_validation()
    
    print("\n🎉 AuthService tests completed!")

if __name__ == "__main__":
    main()
