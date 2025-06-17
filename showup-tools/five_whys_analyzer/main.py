"""
Main Entry Point for the 5 Whys Root Cause Analysis Chatbot

This module initializes the application, sets up logging,
and launches the main window.
"""

import os
import sys
import tkinter as tk
import argparse
from pathlib import Path

# Add parent directory to path to allow imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from five_whys_analyzer.ui.main_window import MainWindow
from five_whys_analyzer.utils.logger import setup_logger
from five_whys_analyzer.utils.config import Config

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="5 Whys Root Cause Analysis Chatbot")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      default="INFO", help="Set the logging level")
    parser.add_argument("--log-file", help="Path to log file")
    parser.add_argument("--config", help="Path to configuration file")
    return parser.parse_args()

def main():
    """Main entry point for the application"""
    # Parse arguments
    args = parse_arguments()
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Set up logging
    logger = setup_logger(
        name="five_whys",
        level=args.log_level,
        log_file=args.log_file
    )
    
    logger.info("Starting 5 Whys Root Cause Analysis Chatbot")
    
    # Load configuration
    config_path = args.config if args.config else "config.json"
    config = Config(config_path)
    
    # Create main window
    root = tk.Tk()
    root.title("5 Whys Root Cause Analysis")
    
    # Set window icon (if available)
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception as e:
        logger.warning(f"Could not set window icon: {str(e)}")
    
    # Initialize application
    app = MainWindow(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    # Start the application
    logger.info("Application initialized")
    root.mainloop()
    logger.info("Application closed")

if __name__ == "__main__":
    main()