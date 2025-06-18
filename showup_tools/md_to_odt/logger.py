"""
Logging module for the Markdown to ODT converter

This module sets up logging for the application and provides functions
for creating loggers with appropriate handlers and formatters.
"""

import os
import logging
from datetime import datetime

def setup_logger(name, level=logging.INFO):
    """
    Set up a logger with file and console handlers
    
    Args:
        name: Name of the logger
        level: Logging level (default: logging.INFO)
        
    Returns:
        Logger instance configured with appropriate handlers
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers if any
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create file handler with timestamped log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(logs_dir, f'md_to_odt_{timestamp}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger initialized: {name}")
    logger.info(f"Log file: {log_file}")
    
    return logger