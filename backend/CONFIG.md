# Configuration Guide

## Environment Variables

The application can be configured using environment variables. Create a `.env` file in the `backend/` directory with the following settings:

### Database Configuration
```env
# SQLite database file path (default: cards.db)
DATABASE_PATH=cards.db

# Supabase Configuration (optional - if not set, uses SQLite)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### Pokemon TCG API Configuration
```env
# Pokemon TCG API settings
POKEMON_TCG_API_BASE_URL=https://api.pokemontcg.io/v2
POKEMON_TCG_API_TIMEOUT=30
POKEMON_TCG_API_ENABLED=true
```

### Logging Configuration
```env
# Logging settings
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### FastAPI Configuration
```env
# API server settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```

## Configuration Priority

1. **Environment Variables** (highest priority)
2. **Default Values** (lowest priority)

## Database Selection

The application automatically chooses the database based on environment variables:

- **SQLite**: Used when `SUPABASE_URL` or `SUPABASE_KEY` is not set
- **Supabase**: Used when both `SUPABASE_URL` and `SUPABASE_KEY` are set

## Example .env File

```env
# Database
DATABASE_PATH=cards.db

# Supabase (comment out to use SQLite)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

# API
POKEMON_TCG_API_TIMEOUT=30
POKEMON_TCG_API_ENABLED=true

# Logging
LOG_LEVEL=INFO

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```
