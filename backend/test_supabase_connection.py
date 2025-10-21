#!/usr/bin/env python3
"""
Simple script to test Supabase connection
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from config import Config

def test_supabase_connection():
    """Test Supabase connection with detailed error reporting"""
    print("🔍 Testing Supabase Configuration...")
    print("=" * 50)
    
    # Check configuration
    print(f"Database Type: {Config.get_database_type()}")
    print(f"USE_SUPABASE: {Config.USE_SUPABASE}")
    print(f"SUPABASE_URL: {Config.SUPABASE_URL}")
    print(f"SUPABASE_KEY: {'SET' if Config.SUPABASE_KEY else 'NOT SET'}")
    
    if not Config.SUPABASE_URL:
        print("❌ SUPABASE_URL not set")
        return False
        
    if not Config.SUPABASE_KEY:
        print("❌ SUPABASE_KEY not set")
        return False
    
    # Validate URL format
    if not Config.SUPABASE_URL.startswith('https://') or '.supabase.co' not in Config.SUPABASE_URL:
        print("❌ SUPABASE_URL format appears invalid")
        return False
    
    # Check key format
    if not Config.SUPABASE_KEY.startswith('eyJ'):
        print("❌ SUPABASE_KEY format appears invalid (should start with 'eyJ')")
        return False
    
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
        
        return True
        
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
        
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    sys.exit(0 if success else 1)
