#!/usr/bin/env python3
"""
Direct test of Pokemon TCG API
"""

import requests
import json

def test_api_direct():
    """Test the Pokemon TCG API directly"""
    print("Testing Pokemon TCG API directly...")
    
    # Test basic API access
    try:
        url = "https://api.pokemontcg.io/v2/cards"
        params = {'pageSize': 1}
        
        print(f"Making request to: {url}")
        print(f"Parameters: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            if 'data' in data:
                print(f"Number of cards: {len(data['data'])}")
                if data['data']:
                    card = data['data'][0]
                    print(f"First card: {card.get('name', 'Unknown')}")
            else:
                print("No 'data' key in response")
                print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test specific card search
    print("\n" + "="*50)
    print("Testing specific card search...")
    
    try:
        url = "https://api.pokemontcg.io/v2/cards"
        params = {'q': 'name:Pikachu', 'pageSize': 3}
        
        print(f"Searching for: Pikachu")
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            cards = data.get('data', [])
            print(f"Found {len(cards)} cards")
            
            for i, card in enumerate(cards):
                print(f"  Card {i+1}: {card.get('name', 'Unknown')}")
                if 'set' in card:
                    print(f"    Set: {card['set'].get('name', 'Unknown')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_direct()
