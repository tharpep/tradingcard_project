#!/usr/bin/env python3
"""
Trading Card Collection CLI - Main Entry Point
Main entry point for the trading card management system.
Automatically uses virtual environment if available.
"""

import sys
import os
import subprocess
from pathlib import Path
from config import Config

def ensure_venv():
    """Ensure we're using the virtual environment"""
    # Check if we're already in a venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return True
    
    # Check if venv exists
    venv_path = Path(__file__).parent.parent / "venv"
    if not venv_path.exists():
        return False
    
    # Determine the correct Python executable
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        return False
    
    # Restart with venv Python
    try:
        # Use subprocess instead of os.execv to handle paths with spaces better
        import subprocess
        result = subprocess.run([str(python_exe)] + sys.argv)
        sys.exit(result.returncode)
    except Exception:
        return False
    
    return True

def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        from .help import show_help
        show_help()
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Handle setup command before any imports
    if command == 'setup':
        from .setup import run_setup
        run_setup()
        return
    
    # Try to use venv, fall back to system Python
    if not ensure_venv():
        print("Virtual environment not found. Using system Python.")
        print("Run 'python run setup' to create the virtual environment.")
    
    # Now import everything after venv is handled
    from utils.logger import setup_logging
    from services.card_service import CardService
    
    # Set up logging
    logger = setup_logging()
    
    # Admin CLI - Full system access
    # Initialize admin card service (bypasses user restrictions)
    card_service = CardService(admin=True)
    
    # Route commands to appropriate modules
    if command in ["add", "list", "search", "delete", "update", "stats"]:
        from .user_commands import handle_user_command
        handle_user_command(command, args, card_service)
    elif command in ["users", "cards"]:
        from .admin_commands import handle_admin_command
        handle_admin_command(command, args, card_service)
    elif command == "stats" and len(args) > 0 and args[0] == "all":
        from .admin_commands import handle_admin_command
        handle_admin_command("stats", args, card_service)
    elif command in ["start", "test", "api-health", "clear"]:
        from .system_commands import handle_system_command
        handle_system_command(command, args, card_service)
    elif command == "help":
        from .help import show_help
        show_help()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python run help' to see available commands")

if __name__ == '__main__':
    main()
