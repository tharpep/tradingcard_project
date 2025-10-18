# Backend CLI Structure Plan

## Overview

Build the backend with a CLI interface for testing database operations locally. Once the logic is solid, we'll convert these CLI commands into FastAPI endpoints.

## Architecture

```
backend/
├── run                    # Main CLI entry point (no .py extension)
├── database/
│   ├── __init__.py
│   ├── connection.py      # Database connection manager (singleton)
│   └── schema.py          # Table definitions and migrations
├── models/
│   ├── __init__.py
│   ├── base.py            # Base model with common functionality
│   └── card.py            # Card model (Pydantic)
├── services/
│   ├── __init__.py
│   ├── base_service.py    # Abstract base service class
│   └── card_service.py    # Card service implementation
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py # Abstract base repository
│   └── card_repository.py # Card database operations
├── utils/
│   ├── __init__.py
│   ├── logger.py          # Logging configuration
│   └── validators.py      # Custom validation helpers
├── config.py              # (already created)
├── main.py                # (convert to API endpoints later)
├── requirements.txt       # Update with CLI dependencies
└── cards.db               # SQLite database (auto-generated)
```

## Database Schema

**cards table:**

- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `name` (TEXT NOT NULL) - e.g., "Charizard"
- `set_name` (TEXT NOT NULL) - e.g., "Base Set"
- `card_number` (TEXT) - e.g., "4/102"
- `rarity` (TEXT) - e.g., "Rare Holo"
- `quantity` (INTEGER DEFAULT 1)
- `is_favorite` (INTEGER DEFAULT 0) - Boolean: 0=false, 1=true
- `date_added` (TEXT) - ISO format timestamp

**Note:** Database auto-initializes on first use (no init command needed)

## CLI Commands to Implement

**Phase 1 - Basic CRUD:**

1. **`python run setup`** - Create venv and install dependencies
2. **`python run add <name>`** - Add card by name only (other fields default)
3. **`python run list`** - List all cards in collection
4. **`python run search <name>`** - Search cards by name
5. **`python run delete <id>`** - Delete a card by ID
6. **`python run stats`** - Show collection statistics

**Phase 2 - Pokemon API Integration (later):**

7. **`python run add <name> --fetch`** - Add card and auto-fill from Pokemon TCG API
8. **`python run update <id> --fetch`** - Update card data from API

**Note:** Database lazy-initializes on first command (no init needed)

## Repository Pattern Explained

**Repositories** handle raw database operations (SQL queries). This separates concerns:

```python
# repository/card_repository.py - talks to database
class CardRepository:
    def insert(self, card_data):
        cursor.execute("INSERT INTO cards ...")
    
    def find_all(self):
        cursor.execute("SELECT * FROM cards")

# services/card_service.py - business logic
class CardService:
    def __init__(self, repo: CardRepository):
        self.repo = repo
    
    def add_card(self, name, set_name):
        # Validate, transform data, then call repo
        card = {"name": name, "set_name": set_name}
        return self.repo.insert(card)
```

**Benefits:**
- Repository = "How to save/load from DB"
- Service = "What business rules to apply"
- Easy to swap SQLite → Supabase later (just change repository)

## Implementation Steps

### Step 1: Update Dependencies
Add `click` for CLI and update requirements.txt

### Step 2: Database Setup
- Create `database/` folder with connection and schema
- Lazy initialization (auto-create on first use)

### Step 3: Data Models
- Create `models/` folder with Pydantic models for card validation
- Ensures data consistency

### Step 4: Business Logic
- Create `services/` folder with card service
- Separate database operations from CLI/API layer
- Functions: `add_card()`, `list_cards()`, `search_cards()`, `delete_card()`, `get_stats()`

### Step 5: Repository Layer
- Create `repositories/` folder with card repository
- Handle all SQLite database operations
- Abstract database access from services

### Step 6: CLI Interface
- Create `run` file with Click commands
- Each command calls the appropriate service function
- Pretty-print output with tables (use `tabulate`)

### Step 7: Testing
- Manually test each CLI command
- Verify database persistence
- Check edge cases (duplicates, empty searches, etc.)

## Migration Paths

### Phase 1 → Phase 2: CLI to API
Once CLI is working, converting to API endpoints:

```python
# CLI: python run list
# API: GET /cards

# CLI: python run add <name>
# API: POST /cards

# CLI: python run search <name>
# API: GET /cards/search?name=<name>
```

The service layer stays the same - just swap CLI commands for FastAPI routes.

### SQLite → Supabase Migration
When moving from SQLite to Supabase, thanks to the repository pattern:

**What Changes:**
- `repositories/card_repository.py` - Update SQL queries for PostgreSQL syntax
- `database/connection.py` - Change from sqlite3 to Supabase client

**What Stays the Same:**
- `services/card_service.py` - Business logic unchanged
- `models/card.py` - Data validation unchanged
- `run` CLI commands - Work exactly the same
- `main.py` API endpoints - Work exactly the same

**Example:**
```python
# SQLite version (Phase 1)
class CardRepository:
    def find_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM cards")
        return cursor.fetchall()

# Supabase version (Phase 3)
class CardRepository:
    def find_all(self):
        response = self.supabase.table('cards').select('*').execute()
        return response.data
```

Everything else just works!

## Benefits of This Approach

- ✅ Test database logic without HTTP complexity
- ✅ Validate data models work correctly
- ✅ Easy debugging with direct Python execution
- ✅ Service layer is reusable for API endpoints
- ✅ No need to run frontend during backend development
- ✅ Repository pattern makes database migration easy
- ✅ Clean separation of concerns (models, services, repositories)

## To-dos

- [ ] Update requirements.txt with click and tabulate for CLI
- [ ] Create database/ folder with connection and schema
- [ ] Create models/ folder with Pydantic models for card validation
- [ ] Create repositories/ folder with card repository
- [ ] Create services/ folder with card service
- [ ] Create run file with Click commands for add, list, search, delete, stats
- [ ] Test all CLI commands and verify database persistence
