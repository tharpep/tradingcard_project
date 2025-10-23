"""
Pokemon TCG API Service

This service handles communication with the Pokemon TCG API to validate
card names and retrieve card information.
"""

import requests
import logging
from typing import Optional, Dict, List, Tuple
from requests.exceptions import Timeout, ConnectionError, RequestException
from config import Config

logger = logging.getLogger(__name__)

class PokemonAPIService:
    """Service for interacting with the Pokemon TCG API"""
    
    def __init__(self):
        self.base_url = Config.POKEMON_TCG_API_BASE_URL
        self.timeout = Config.POKEMON_TCG_API_TIMEOUT
        self.max_retries = 2  # allow retries
        self.enabled = Config.POKEMON_TCG_API_ENABLED
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the Pokemon TCG API with error handling
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            API response data or None if request failed
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.info(f"Making request to Pokemon TCG API: {url}")
            logger.info(f"Query parameters: {params}")
            
            response = requests.get(
                url, 
                params=params, 
                timeout=10  # Reduced timeout for faster failure
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully received response from Pokemon TCG API")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error when calling Pokemon TCG API: {url}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error when calling Pokemon TCG API: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when calling Pokemon TCG API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error when calling Pokemon TCG API: {e}")
            return None
    
    def validate_card_name(self, card_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if a card name exists in the Pokemon TCG API
        
        Args:
            card_name: Name of the card to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if card exists, False otherwise
            - error_message: Error message if validation failed, None if successful
        """
        if not card_name or not card_name.strip():
            return False, "Card name cannot be empty"
        
        # Clean the card name
        clean_name = card_name.strip()
        
        try:
            # Search for cards with the exact name - just need to know if any exist
            params = {
                'q': f'name:"{clean_name}"',  # Use exact match with quotes for faster search
                'pageSize': 1  # Only need 1 result to verify existence
            }
            
            data = self._make_request('cards', params)
            
            if data is None:
                # API request failed - this is a hard failure, don't allow the card
                logger.error(f"Pokemon API request failed for '{clean_name}' - cannot validate card")
                return False, "Unable to validate card name. Pokemon TCG API is not responding. Please try again later."
            
            cards = data.get('data', [])
            
            # Simple validation - just check if any cards exist
            logger.info(f"Pokemon API search for '{clean_name}' found {len(cards)} cards")
            
            if not cards:
                return False, f"'{clean_name}' is not a valid Pokemon card. Please check the name and try again."
            
            # If we found any cards, the card exists
            logger.info(f"Successfully validated Pokemon card: {clean_name}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error validating card name '{card_name}': {e}")
            return False, "An error occurred while validating the card name. Please try again."
    
    def search_cards(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for Pokemon cards by name
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of card data dictionaries
        """
        if not query or not query.strip():
            return []
        
        try:
            params = {
                'q': f'name:"{query}"',
                'pageSize': limit
            }
            
            data = self._make_request('cards', params)
            
            if data is None:
                return []
            
            return data.get('data', [])
            
        except Exception as e:
            logger.error(f"Error searching for cards with query '{query}': {e}")
            return []
    
    def get_card_details(self, card_name: str) -> Optional[Dict]:
        """
        Get detailed information about a specific Pokemon card
        
        Args:
            card_name: Name of the card
            
        Returns:
            Card data dictionary or None if not found
        """
        try:
            params = {
                'q': f'name:"{card_name}"',
                'pageSize': 1
            }
            
            data = self._make_request('cards', params)
            
            if data is None:
                return None
            
            cards = data.get('data', [])
            
            if not cards:
                return None
            
            # Return the first exact match
            for card in cards:
                if card.get('name', '').lower() == card_name.lower():
                    return card
            
            # If no exact match, return the first result
            return cards[0] if cards else None
            
        except Exception as e:
            logger.error(f"Error getting card details for '{card_name}': {e}")
            return None
    
    def health_check(self) -> Tuple[bool, str]:
        """
        Check if the Pokemon TCG API is available with detailed status
        
        Returns:
            Tuple of (is_available, status_message)
        """
        try:
            logger.info("Performing Pokemon TCG API health check...")
            
            # Use the same endpoint as card validation for consistency
            response = requests.get(
                f"{self.base_url}/cards", 
                params={'q': 'name:"Pikachu"', 'pageSize': 1}, 
                timeout=5  # Shorter timeout for health check
            )
            response.raise_for_status()
            
            data = response.json()
            if data and 'data' in data:
                logger.info("Pokemon TCG API health check: SUCCESS")
                return True, "API is responding normally"
            else:
                logger.warning("Pokemon TCG API health check: Invalid response format")
                return False, "API responded but with invalid format"
                
        except Timeout:
            logger.error("Pokemon TCG API health check: TIMEOUT")
            return False, "API request timed out (5 seconds)"
        except ConnectionError:
            logger.error("Pokemon TCG API health check: CONNECTION ERROR")
            return False, "Cannot connect to API (network issue)"
        except RequestException as e:
            logger.error(f"Pokemon TCG API health check: REQUEST ERROR - {e}")
            return False, f"API request failed: {e}"
        except Exception as e:
            logger.error(f"Pokemon TCG API health check: UNEXPECTED ERROR - {e}")
            return False, f"Unexpected error: {e}"
    
    def is_api_available(self) -> bool:
        """
        Check if the Pokemon TCG API is available (simple boolean check)
        
        Returns:
            True if API is available, False otherwise
        """
        is_available, _ = self.health_check()
        return is_available

# Create a singleton instance
pokemon_api_service = PokemonAPIService()
