#!/usr/bin/env python3
"""
Standalone Pokemon TCG API Test Script

This script tests the Pokemon TCG API directly to diagnose timeout and reliability issues.
Run this script to understand what's happening with the API calls.
"""

import requests
import time
import json
from typing import Dict, List, Optional, Tuple
from requests.exceptions import Timeout, ConnectionError, RequestException

class PokemonAPITester:
    """Test the Pokemon TCG API with various configurations"""
    
    def __init__(self):
        self.base_url = "https://api.pokemontcg.io/v2"
        self.test_cards = [
            "Pikachu",
            "Charizard", 
            "Blastoise",
            "Venusaur",
            "Mewtwo",
            "InvalidCardName123"  # This should fail
        ]
    
    def test_basic_connectivity(self) -> Tuple[bool, str]:
        """Test basic API connectivity"""
        print("🔍 Testing basic API connectivity...")
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/sets", timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"   Response time: {response_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ API is responding (Status: {response.status_code})")
                print(f"   📊 Response contains {len(data.get('data', []))} sets")
                return True, f"API responding in {response_time:.2f}s"
            else:
                print(f"   ❌ API returned status {response.status_code}")
                return False, f"API returned status {response.status_code}"
                
        except Timeout:
            print("   ❌ Request timed out after 10 seconds")
            return False, "Request timed out"
        except ConnectionError:
            print("   ❌ Connection error - cannot reach API")
            return False, "Connection error"
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            return False, f"Unexpected error: {e}"
    
    def test_card_search(self, card_name: str, timeout: int = 30) -> Tuple[bool, str, float]:
        """Test searching for a specific card"""
        print(f"🔍 Testing card search for '{card_name}'...")
        
        try:
            start_time = time.time()
            params = {
                'q': f'name:"{card_name}"',
                'pageSize': 1
            }
            
            response = requests.get(
                f"{self.base_url}/cards",
                params=params,
                timeout=timeout
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"   Response time: {response_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                cards = data.get('data', [])
                print(f"   ✅ Found {len(cards)} cards")
                
                if cards:
                    card = cards[0]
                    print(f"   📋 First result: {card.get('name', 'Unknown')} from {card.get('set', {}).get('name', 'Unknown Set')}")
                
                return True, f"Found {len(cards)} cards", response_time
            else:
                print(f"   ❌ API returned status {response.status_code}")
                return False, f"Status {response.status_code}", response_time
                
        except Timeout:
            print(f"   ❌ Request timed out after {timeout} seconds")
            return False, f"Timeout after {timeout}s", timeout
        except ConnectionError:
            print("   ❌ Connection error")
            return False, "Connection error", 0
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False, f"Error: {e}", 0
    
    def test_different_timeouts(self) -> Dict[int, Tuple[bool, str, float]]:
        """Test API with different timeout values"""
        print("\n🔍 Testing different timeout values...")
        
        timeouts = [5, 10, 15, 30, 60]
        results = {}
        
        for timeout in timeouts:
            print(f"\n   Testing with {timeout}s timeout:")
            success, message, response_time = self.test_card_search("Pikachu", timeout)
            results[timeout] = (success, message, response_time)
            
            if success:
                print(f"   ✅ Success with {timeout}s timeout")
                break
            else:
                print(f"   ❌ Failed with {timeout}s timeout: {message}")
        
        return results
    
    def test_multiple_cards(self) -> Dict[str, Tuple[bool, str, float]]:
        """Test searching for multiple different cards"""
        print("\n🔍 Testing multiple card searches...")
        
        results = {}
        
        for card_name in self.test_cards:
            print(f"\n   Testing card: '{card_name}'")
            success, message, response_time = self.test_card_search(card_name, 15)
            results[card_name] = (success, message, response_time)
            
            if success:
                print(f"   ✅ Success: {message}")
            else:
                print(f"   ❌ Failed: {message}")
        
        return results
    
    def test_rate_limiting(self) -> List[Tuple[bool, str, float]]:
        """Test if rapid requests cause issues"""
        print("\n🔍 Testing rate limiting with rapid requests...")
        
        results = []
        
        for i in range(5):
            print(f"   Request {i+1}/5...")
            success, message, response_time = self.test_card_search("Pikachu", 10)
            results.append((success, message, response_time))
            
            if not success:
                print(f"   ❌ Request {i+1} failed: {message}")
                break
            else:
                print(f"   ✅ Request {i+1} succeeded in {response_time:.2f}s")
            
            # Small delay between requests
            time.sleep(0.5)
        
        return results
    
    def run_comprehensive_test(self):
        """Run all tests and provide a comprehensive report"""
        print("🚀 Starting Pokemon TCG API Comprehensive Test")
        print("=" * 60)
        
        # Test 1: Basic connectivity
        print("\n1. BASIC CONNECTIVITY TEST")
        print("-" * 30)
        connectivity_success, connectivity_message = self.test_basic_connectivity()
        
        if not connectivity_success:
            print("\n❌ CRITICAL: Basic connectivity failed!")
            print("   The API is completely unreachable.")
            print("   Possible causes:")
            print("   - Network connectivity issues")
            print("   - API server is down")
            print("   - Firewall blocking requests")
            return
        
        # Test 2: Different timeouts
        print("\n2. TIMEOUT TESTING")
        print("-" * 30)
        timeout_results = self.test_different_timeouts()
        
        # Test 3: Multiple cards
        print("\n3. MULTIPLE CARD TESTING")
        print("-" * 30)
        card_results = self.test_multiple_cards()
        
        # Test 4: Rate limiting
        print("\n4. RATE LIMITING TEST")
        print("-" * 30)
        rate_results = self.test_rate_limiting()
        
        # Generate report
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        print(f"\n✅ Basic Connectivity: {connectivity_message}")
        
        print(f"\n⏱️  Timeout Analysis:")
        for timeout, (success, message, response_time) in timeout_results.items():
            status = "✅" if success else "❌"
            print(f"   {timeout}s: {status} {message} ({response_time:.2f}s)")
        
        print(f"\n🎴 Card Search Results:")
        for card, (success, message, response_time) in card_results.items():
            status = "✅" if success else "❌"
            print(f"   {card}: {status} {message} ({response_time:.2f}s)")
        
        print(f"\n🔄 Rate Limiting Results:")
        successful_requests = sum(1 for success, _, _ in rate_results if success)
        print(f"   Successful requests: {successful_requests}/5")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if any(success for success, _, _ in timeout_results.values()):
            working_timeout = min(timeout for timeout, (success, _, _) in timeout_results.items() if success)
            print(f"   ✅ Use {working_timeout}s timeout for reliable requests")
        else:
            print("   ❌ No timeout value worked - API may be unreliable")
        
        if successful_requests < 5:
            print("   ⚠️  Rate limiting detected - add delays between requests")
        
        if any(not success for success, _, _ in card_results.values()):
            print("   ⚠️  Some card searches failed - implement fallback logic")
        
        print(f"\n🎯 CONCLUSION:")
        if connectivity_success and any(success for success, _, _ in timeout_results.values()):
            print("   ✅ API is functional but may have reliability issues")
            print("   💡 Consider implementing retry logic and graceful degradation")
        else:
            print("   ❌ API has significant reliability issues")
            print("   💡 Consider disabling validation or using cached data")

def test_pokemon_api_comprehensive():
    """Comprehensive Pokemon TCG API test"""
    tester = PokemonAPITester()
    tester.run_comprehensive_test()

def main():
    """Main test function"""
    tester = PokemonAPITester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
