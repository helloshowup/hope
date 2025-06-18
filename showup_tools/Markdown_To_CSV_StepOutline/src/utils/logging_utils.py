#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Logging configuration and utilities."""

import os
import logging
from datetime import datetime
from typing import Optional


def setup_logging(log_level: int = logging.INFO,
                  log_to_file: bool = True,
                  log_dir: Optional[str] = None) -> logging.Logger:
    """Configure and setup logging for the application.
    
    Args:
        log_level: The logging level to use
        log_to_file: Whether to log to a file in addition to console
        log_dir: Directory to store log files
        
    Returns:
        The configured root logger
    """
    # Setup basic logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:  
        logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        # Create log directory if it doesn't exist
        if log_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            log_dir = os.path.join(base_dir, 'logs')
            
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"md_to_csv_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Logging to file: {log_file}")
    
    return logger
