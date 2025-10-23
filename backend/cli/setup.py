"""
Setup functionality for CLI
"""

import subprocess
import sys
from pathlib import Path

def run_setup():
    """Run the setup script"""
    print("Setting up virtual environment and dependencies...")
    
    try:
        # Run the setup script
        setup_script = Path(__file__).parent.parent / "setup.py"
        result = subprocess.run([sys.executable, str(setup_script)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Setup completed successfully!")
            print("\nYou can now use all CLI commands:")
            print("   python run add Charizard")
            print("   python run list")
            print("   python run stats")
        else:
            print(f"Setup failed with return code: {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            if result.stdout:
                print(f"Standard output: {result.stdout}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Setup error: {e}")
        sys.exit(1)
