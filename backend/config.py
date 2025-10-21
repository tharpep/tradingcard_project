import os
from pathlib import Path
from typing import Optional

def load_env_file():
    """Load environment variables from .env file in root directory"""
    root_dir = Path(__file__).parent.parent  # Go up from backend/ to root
    env_file = root_dir / '.env'
    
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Only set if not already set (environment variables take precedence)
                        if key not in os.environ:
                            os.environ[key] = value
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")

# Load .env file before reading environment variables
load_env_file()

class Config:
    """Configuration management for the application"""
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', 'cards.db')
    USE_SUPABASE: bool = bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'))
    
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = os.getenv('SUPABASE_URL')
    SUPABASE_KEY: Optional[str] = os.getenv('SUPABASE_KEY')
    
    # API Configuration
    POKEMON_TCG_API_BASE_URL: str = os.getenv('POKEMON_TCG_API_BASE_URL', 'https://api.pokemontcg.io/v2')
    POKEMON_TCG_API_TIMEOUT: int = int(os.getenv('POKEMON_TCG_API_TIMEOUT', '30'))
    POKEMON_TCG_API_ENABLED: bool = os.getenv('POKEMON_TCG_API_ENABLED', 'true').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # FastAPI Configuration
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
    API_PORT: int = int(os.getenv('API_PORT', '8000'))
    API_RELOAD: bool = os.getenv('API_RELOAD', 'true').lower() == 'true'
    
    @classmethod
    def validate_supabase_config(cls) -> bool:
        """Validate that Supabase configuration is complete"""
        if not cls.SUPABASE_URL:
            print("ERROR: SUPABASE_URL environment variable not set")
            return False
        
        if not cls.SUPABASE_KEY:
            print("ERROR: SUPABASE_KEY environment variable not set")
            return False
        
        # Basic validation of URL format
        if not cls.SUPABASE_URL.startswith('https://') or '.supabase.co' not in cls.SUPABASE_URL:
            print("ERROR: SUPABASE_URL appears to be invalid")
            return False
        
        return True
    
    @classmethod
    def get_database_type(cls) -> str:
        """Get the database type being used"""
        if cls.USE_SUPABASE:
            return "supabase"
        return "sqlite"