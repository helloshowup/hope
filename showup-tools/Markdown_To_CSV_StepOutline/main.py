#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main entry point for the Markdown to CSV Converter application."""

import os
import sys
import logging
from typing import Optional
import argparse

# Debug imports
print("Starting main.py")
print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Add project root to path to enable imports (with debugging)
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
print(f"Added {project_root} to Python path")
print(f"Updated sys.path: {sys.path[0:3]}")

# Try basic imports first to ensure nothing is broken
try:
    print("Testing basic imports...")
    import src
    print("Successfully imported src package")
except ImportError as e:
    print(f"Failed to import src package: {e}")
    sys.exit(1)

from src.utils.logging_utils import setup_logging
from src.utils.config import ConfigManager
from src.core.api_handler import APIHandler
from src.core.markdown_converter import MarkdownToCSVConverter


def convert_markdown_to_csv(input_file: str, output_file: str, 
                          use_ai: bool = False, api_key: Optional[str] = None,
                          conversion_method: str = "hybrid",
                          progress_callback: Optional[callable] = None) -> bool:
    """Convert a markdown file to CSV format.
    
    Args:
        input_file: Path to the input markdown file
        output_file: Path where the output CSV file will be saved
        use_ai: Whether to use AI enhancement
        api_key: API key for AI service
        conversion_method: One of 'hybrid', 'ai_driven', or 'rule_based'
        progress_callback: Optional callback function for progress updates
            Format: progress_callback(progress_value: float, message: str)
    
    Returns:
        bool: Success status
    """
    # Setup logging
    logger = logging.getLogger("Convert")
    
    # Validate input file
    if not os.path.isfile(input_file):
        logger.error(f"Input file not found: {input_file}")
        return False
    
    # Setup API handler if AI is requested
    api_handler = None
    if use_ai:
        # If no API key is provided, try to get it from config
        if not api_key:
            config = ConfigManager()
            api_key = config.get_anthropic_api_key()
        
        if api_key:
            api_handler = APIHandler(api_key)
            if not api_handler.is_available():
                logger.warning("AI requested but not available. Proceeding without AI enhancement.")
        else:
            logger.warning("AI requested but no API key found. Proceeding without AI enhancement.")
    
    # Create and run converter
    converter = MarkdownToCSVConverter(
        input_file=input_file,
        output_file=output_file,
        api_handler=api_handler
    )
    
    return converter.convert(progress_callback=progress_callback)


def run_gui() -> None:
    """Run the application in GUI mode."""
    from src.gui.app_gui import run_gui as start_gui
    start_gui()


def run_cli() -> int:
    """Run the application in CLI mode.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert structured Markdown to CSV format for ShowUpSquared")
    
    parser.add_argument(
        "input_file", 
        help="Path to input Markdown file"
    )
    
    parser.add_argument(
        "output_file", 
        nargs="?",
        help="Path to output CSV file (defaults to input file with .csv extension)"
    )
    
    parser.add_argument(
        "--use-ai", 
        action="store_true",
        help="Use AI enhancement for content processing"
    )
    
    parser.add_argument(
        "--method",
        choices=["hybrid", "ai_driven", "rule_based"],
        default="hybrid",
        help="Conversion method to use"
    )
    
    args = parser.parse_args()
    
    # Determine output file if not specified
    input_file = args.input_file
    output_file = args.output_file
    
    if not output_file:
        # Use input filename with .csv extension
        output_file = os.path.splitext(input_file)[0] + ".csv"
    
    # Run conversion
    success = convert_markdown_to_csv(
        input_file=input_file,
        output_file=output_file,
        use_ai=args.use_ai,
        conversion_method=args.method
    )
    
    if success:
        logging.info(f"Conversion successful! Output saved to: {output_file}")
        return 0
    else:
        logging.error("Conversion failed. See log for details.")
        return 1


def main() -> int:
    """Main entry point function.
    
    Returns:
        int: Exit code
    """
    # Setup logging
    setup_logging()
    
    # Check if GUI or CLI mode
    if len(sys.argv) > 1:
        # CLI mode
        return run_cli()
    else:
        # GUI mode
        run_gui()
        return 0


if __name__ == "__main__":
    sys.exit(main())
