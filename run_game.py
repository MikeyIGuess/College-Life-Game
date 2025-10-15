#!/usr/bin/env python3
import os
import sys
import subprocess

def check_requirements():
    try:
        import pygame
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Packages installed successfully!")

def main():
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check and install requirements
    check_requirements()
    
    # Import and run the game
    import main
    main.main()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")