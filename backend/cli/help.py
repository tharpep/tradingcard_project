"""
Help system for CLI commands
"""

from config import Config

def show_help():
    """Show help information"""
    print("Trading Card Collection Manager")
    print("=" * 40)
    
    # Show database type
    db_type = Config.get_database_type()
    if db_type == "supabase":
        print(f"Database: Supabase (Cloud)")
    else:
        print(f"Database: SQLite (Local)")
    
    print("\nCommands:")
    print("  setup                    - Set up virtual environment and dependencies")
    print("  add <name>               - Add a new card")
    print("  list                     - List all cards")
    print("  list --favorites         - List favorite cards only")
    print("  search <name>            - Search cards by name")
    print("  delete <id>              - Delete a card by ID")
    print("  update <id> [options]    - Update a card")
    print("  stats                    - Show collection statistics")
    print("  start                    - Start the FastAPI server")
    print("  test [options]           - Run test suite")
    print("  test v                   - Run tests with verbose output")
    print("  test <filename>          - Run specific test file")
    print("  api-health               - Check Pokemon TCG API health")
    print("  clear                    - Delete all cards from database")
    print("\nAdmin Commands:")
    print("  users                    - List all users")
    print("  cards all                - Show ALL cards from ALL users")
    print("  cards user <user_id>     - Show cards for specific user")
    print("  stats all                - Show system-wide statistics")
    print("  help                     - Show this help")
    print("\nExamples:")
    print("  python run add Charizard")
    print("  python run add Pikachu --set 'Base Set' --rarity 'Common' --favorite")
    print("  python run list")
    print("  python run search Char")
    print("  python run delete 1")
    print("  python run update 1 --rarity 'Rare Holo' --favorite")
    print("  python run stats")
    print("  python run start")
    print("  python run test")
    print("  python run test v")
    print("  python run test test_models.py")
    print("\nAdmin Examples:")
    print("  python run users")
    print("  python run cards all")
    print("  python run cards user 123e4567-e89b-12d3-a456-426614174000")
    print("  python run stats all")
    print("\nAdd card options:")
    print("  --set <name>             - Set name (default: Unknown)")
    print("  --number <number>         - Card number")
    print("  --rarity <rarity>         - Card rarity")
    print("  --quantity <number>       - Quantity (default: 1)")
    print("  --favorite               - Mark as favorite")
    print("\nUpdate card options:")
    print("  --name <name>             - Update card name")
    print("  --set <name>              - Update set name")
    print("  --number <number>         - Update card number")
    print("  --rarity <rarity>         - Update rarity")
    print("  --quantity <number>       - Update quantity")
    print("  --favorite                - Toggle favorite status")
