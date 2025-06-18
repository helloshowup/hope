"""
Logging utilities for the 5 Whys Root Cause Analysis Chatbot
"""

import os
import logging
import sys
from datetime import datetime
from typing import Optional

def setup_logger(name: str = "five_whys", 
                 level: str = "INFO", 
                 log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with console and file handlers
    
    Args:
        name (str): Logger name
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str, optional): Path to log file. If None, a default path is used.
        
    Returns:
        logging.Logger: Configured logger
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Clear existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified or create a default one
    if log_file is None:
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Generate log filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f"logs/five_whys_{timestamp}.log"
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = "five_whys") -> logging.Logger:
    """
    Get a logger with the specified name.
    If the logger doesn't exist, it creates a default one.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: The requested logger
    """
    logger = logging.getLogger(name)
    
    # If logger doesn't have handlers, set up a default one
    if not logger.handlers:
        return setup_logger(name)
    
    return logger