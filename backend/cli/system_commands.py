"""
System-level CLI commands
"""

import sys
import subprocess
import os
import uvicorn
from services.card_service import CardService
from services.pokemon_api_service import pokemon_api_service
from config import Config

def handle_system_command(command: str, args: list, card_service: CardService):
    """Route system commands to appropriate handlers"""
    if command == "start":
        start_api_server()
    elif command == "test":
        run_tests(args)
    elif command == "api-health":
        check_api_health(args)
    elif command == "clear":
        clear_all_cards(args, card_service)

def start_api_server():
    """Start the FastAPI server"""
    try:
        print("Starting FastAPI server...")
        print("Server will be available at: http://localhost:8000")
        print("API documentation: http://localhost:8000/docs")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Import uvicorn after ensuring venv
        import uvicorn
        
        # Start the server with import string for reload to work
        uvicorn.run("main:app", host=Config.API_HOST, port=Config.API_PORT, reload=Config.API_RELOAD)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

def run_tests(args):
    """Run the test suite"""
    try:
        print("Running test suite...")
        print("=" * 50)
        
        # Import pytest after ensuring venv
        import pytest
        import subprocess
        import os
        
        # Get the tests directory (backend/tests)
        tests_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
        
        # Build pytest command
        cmd = [sys.executable, '-m', 'pytest']
        
        # Handle specific test file or verbose mode
        if len(args) > 0:
            if args[0] == 'v' or args[0] == '-v' or args[0] == '--verbose':
                # Verbose mode - run all tests with verbose output
                cmd.extend([tests_dir, '-v'])
            else:
                # Specific test file
                test_file = args[0]
                if not test_file.endswith('.py'):
                    test_file += '.py'
                test_path = os.path.join(tests_dir, test_file)
                if os.path.exists(test_path):
                    cmd.extend([test_path, '-v'])
                else:
                    print(f"Test file not found: {test_path}")
                    sys.exit(1)
        else:
            # Default: run all tests without verbose output
            cmd.append(tests_dir)
        
        print(f"Running: {' '.join(cmd)}")
        print("-" * 50)
        
        # Run tests
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code: {result.returncode}")
            sys.exit(1)
            
    except ImportError:
        print("Error: pytest not found. Run 'python run setup' first to install dependencies.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

def check_api_health(args):
    """Check Pokemon TCG API health"""
    try:
        print("Checking Pokemon TCG API health...")
        print("=" * 50)
        
        from services.pokemon_api_service import pokemon_api_service
        
        is_available, status_message = pokemon_api_service.health_check()
        
        if is_available:
            print(f"SUCCESS: Pokemon TCG API: {status_message}")
        else:
            print(f"FAILED: Pokemon TCG API: {status_message}")
            
    except Exception as e:
        print(f"ERROR: Error checking API health: {e}")
        sys.exit(1)

def clear_all_cards(args, card_service: CardService):
    """Clear all cards from the database"""
    try:
        print("WARNING: This will delete ALL cards from the database!")
        print("This action cannot be undone.")
        
        # Ask for confirmation
        confirm = input("Type 'yes' to confirm deletion: ").strip().lower()
        if confirm != 'yes':
            print("Operation cancelled.")
            return
        
        # Import services after ensuring venv
        from services.card_service import CardService
        
        card_service = CardService()
        
        # Get current count
        stats = card_service.get_collection_stats()
        total_cards = stats.get('total_cards', 0)
        
        if total_cards == 0:
            print("No cards to delete.")
            return
        
        print(f"Deleting {total_cards} cards...")
        
        # Use batch delete for efficiency
        deleted_count = card_service.delete_all_cards()
        
        print(f"Successfully deleted {deleted_count} cards.")
        
    except Exception as e:
        print(f"ERROR: Failed to clear cards: {e}")
        sys.exit(1)
