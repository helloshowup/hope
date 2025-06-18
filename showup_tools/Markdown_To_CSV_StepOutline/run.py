#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simplified entry point for the Markdown to CSV Converter application."""

import os
import sys

# Basic error handling for missing dependencies
try:
    import tkinter
except ImportError:
    print("ERROR: tkinter is not installed. This is required for the GUI.")
    print("Please install tkinter and try again.")
    sys.exit(1)

# Define the application directory structure
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(APP_DIR, 'src')

# Add the application directory to the Python path
sys.path.insert(0, APP_DIR)

print(f"Starting application from {APP_DIR}")
print(f"Python version: {sys.version}")

# Check if the src directory exists and is importable
if not os.path.isdir(SRC_DIR):
    print(f"ERROR: Source directory not found: {SRC_DIR}")
    sys.exit(1)

# Try to run the GUI directly without complex imports
try:
    # Import the GUI module directly
    from src.gui.app_gui import run_gui
    
    # Start the application
    print("Starting Markdown to CSV Converter...")
    run_gui()
    
except ImportError as e:
    print(f"ERROR: Failed to import application modules: {e}")
    print("\nThis could be caused by:")
    print("1. Missing Python dependencies")
    print("2. Incorrect Python path configuration")
    print("\nTry running 'install_dependencies.bat' and try again.")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: An unexpected error occurred: {e}")
    sys.exit(1)
