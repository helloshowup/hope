"""
Configuration utilities for the 5 Whys Root Cause Analysis Chatbot
"""

import os
import json
import logging
from typing import Dict, Any

# Default configuration values
DEFAULT_CONFIG = {
    "thinking_budget": 16000,
    "max_tokens": 4000,
    "temperature": 0.3,
    "mermaid_theme": "default",
    "save_history": True,
    "history_dir": "history",
    "log_level": "INFO"
}

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize configuration
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Load configuration from file
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                return True
        except Exception as e:
            logging.error(f"Error loading config: {str(e)}")
        return False
    
    def save_config(self) -> bool:
        """
        Save configuration to file
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Error saving config: {str(e)}")
        return False
    
    def get(self, key: str, default=None) -> Any:
        """
        Get a configuration value
        
        Args:
            key (str): Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Any: The configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value
        
        Args:
            key (str): Configuration key
            value (Any): Configuration value
        """
        self.config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values
        
        Returns:
            Dict[str, Any]: All configuration values
        """
        return self.config.copy()