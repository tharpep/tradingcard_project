#!/usr/bin/env python
"""
Setup script for Trading Card Collection CLI
Creates virtual environment and installs dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"{description}...")
    print(f"   Command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed:")
        print(f"   Return code: {e.returncode}")
        print(f"   Error: {e.stderr}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        return False

def main():
    """Main setup function"""
    print("Trading Card Collection Setup")
    print("=" * 40)
    
    # Debug: Show current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {Path(__file__).parent}")
    
    # Check if we're in the backend directory
    requirements_path = Path("requirements.txt")
    print(f"Looking for requirements.txt at: {requirements_path.absolute()}")
    if not requirements_path.exists():
        print("ERROR: requirements.txt not found!")
        print("Please run this script from the backend directory")
        print("Expected location: backend/requirements.txt")
        sys.exit(1)
    print("Found requirements.txt")
    
    # Check if Python is available
    print("Checking Python installation...")
    if not run_command("python --version", "Checking Python version"):
        print("ERROR: Python is not installed or not in PATH")
        sys.exit(1)
    
    # Create virtual environment - try different methods
    print("Creating virtual environment...")
    
    # Try python -m venv first
    if not run_command("python -m venv venv", "Creating virtual environment with venv"):
        print("venv failed, trying virtualenv...")
        # Try virtualenv as fallback
        if not run_command("python -m virtualenv venv", "Creating virtual environment with virtualenv"):
            print("ERROR: Both venv and virtualenv failed")
            print("This might be a Python installation issue.")
            sys.exit(1)
    
    # Check if venv was created
    venv_path = Path("venv")
    if not venv_path.exists():
        print("ERROR: Virtual environment directory was not created!")
        sys.exit(1)
    print("Virtual environment directory created successfully")
    
    # Debug: List what's actually in the venv directory
    print("Contents of venv directory:")
    try:
        for item in venv_path.iterdir():
            print(f"  {item.name}")
            if item.is_dir() and item.name == "Scripts":
                print("    Scripts directory contents:")
                for script in item.iterdir():
                    print(f"      {script.name}")
    except Exception as e:
        print(f"Error listing venv contents: {e}")
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_path = "venv\\Scripts\\pip.exe"  # Windows needs .exe
        python_path = "venv\\Scripts\\python.exe"
    else:  # Unix/Linux/Mac
        activate_script = "venv/bin/activate"
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    print(f"Using pip path: {pip_path}")
    print(f"Using python path: {python_path}")
    
    # Check if pip exists in venv
    pip_full_path = Path(pip_path)
    if not pip_full_path.exists():
        print(f"ERROR: pip not found at {pip_full_path.absolute()}")
        print("Virtual environment was created but pip is missing.")
        print("This usually indicates a Python installation issue.")
        sys.exit(1)
    print("Found pip in virtual environment")
    
    # Upgrade pip using python -m pip instead of direct pip
    print("Upgrading pip...")
    if not run_command(f"{python_path} -m pip install --upgrade pip", "Upgrading pip"):
        print("ERROR: Failed to upgrade pip")
        sys.exit(1)
    
    # Install requirements using python -m pip
    print("Installing dependencies...")
    print(f"Requirements file: {Path('requirements.txt').absolute()}")
    if not run_command(f"{python_path} -m pip install -r requirements.txt", "Installing dependencies"):
        print("ERROR: Failed to install dependencies")
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\nTo use the CLI:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source venv/bin/activate")
    print("2. Run commands:")
    print("   python run --help")
    print("   python run add Charizard")
    print("   python run list")

if __name__ == "__main__":
    main()
