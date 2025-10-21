from typing import Union
from .card_repository import CardRepository
from config import Config

def get_card_repository() -> Union[CardRepository, 'SupabaseCardRepository']:
    """Factory function to get the appropriate card repository"""
    
    if Config.USE_SUPABASE:
        if not Config.validate_supabase_config():
            raise ValueError("Supabase configuration is invalid")
        # Import Supabase repository only when needed
        from .supabase_card_repository import SupabaseCardRepository
        return SupabaseCardRepository()
    else:
        return CardRepository()
