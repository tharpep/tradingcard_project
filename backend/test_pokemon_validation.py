#!/usr/bin/env python3
"""
Test Pokemon validation with debug output
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.pokemon_api_service import pokemon_api_service
from services.card_service import CardService

def test_validation():
    """Test Pokemon card validation with debug output"""
    print("Testing Pokemon Card Validation")
    print("=" * 50)
    
    card_service = CardService()
    
    # Test cases
    test_cases = [
        ("Pikachu", "Should be valid"),
        ("Charizard", "Should be valid"), 
        ("stupidguy", "Should be invalid"),
        ("DoodleBob", "Should be invalid")
    ]
    
    for card_name, description in test_cases:
        print(f"\nTesting: {card_name} ({description})")
        print("-" * 30)
        
        try:
            is_valid, error = card_service.validate_pokemon_card(card_name)
            print(f"Result: {'VALID' if is_valid else 'INVALID'}")
            if error:
                print(f"Error: {error}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_validation()
