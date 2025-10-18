#!/usr/bin/env python3
"""
Test script for Pokemon TCG API integration
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.pokemon_api_service import pokemon_api_service
from services.card_service import CardService

def test_pokemon_api():
    """Test the Pokemon TCG API integration"""
    print("Testing Pokemon TCG API Integration")
    print("=" * 50)
    
    # Test API availability
    print("1. Testing API availability...")
    is_available = pokemon_api_service.is_api_available()
    print(f"   API Available: {is_available}")
    
    if not is_available:
        print("   Warning: Pokemon TCG API is not available. Tests will be limited.")
        return
    
    # Test valid Pokemon card
    print("\n2. Testing valid Pokemon card (Charizard)...")
    is_valid, error = pokemon_api_service.validate_card_name("Charizard")
    print(f"   Valid: {is_valid}")
    if error:
        print(f"   Error: {error}")
    
    # Test invalid card
    print("\n3. Testing invalid card (DoodleBob)...")
    is_valid, error = pokemon_api_service.validate_card_name("DoodleBob")
    print(f"   Valid: {is_valid}")
    if error:
        print(f"   Error: {error}")
    
    # Test card service integration
    print("\n4. Testing CardService integration...")
    card_service = CardService()
    
    # Test valid card
    print("   Testing valid card (Pikachu)...")
    try:
        is_valid, error = card_service.validate_pokemon_card("Pikachu")
        print(f"   Valid: {is_valid}")
        if error:
            print(f"   Error: {error}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test invalid card
    print("   Testing invalid card (SpongeBob)...")
    try:
        is_valid, error = card_service.validate_pokemon_card("SpongeBob")
        print(f"   Valid: {is_valid}")
        if error:
            print(f"   Error: {error}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("\n" + "=" * 50)
    print("Pokemon API integration test completed!")

if __name__ == "__main__":
    test_pokemon_api()
