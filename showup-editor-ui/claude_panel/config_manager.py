#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Manager for the Output Library Editor
Handles loading, saving, and accessing application settings
"""

import os
import json
import logging
from .path_utils import get_project_root

# Get logger
logger = logging.getLogger("output_library_editor")

class ConfigManager:
    """Manages application configuration settings"""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        "library_path": os.path.join(os.path.expanduser("~"), "Documents", "showup-v4", "showup-library", "library"),
        "recent_files": [],
        "recent_projects": [],
        "library_prompts_path": "C:\\Users\\User\\Documents\\showup-v4\\showup-library\\prompts",
    }
    
    def __init__(self):
        # Path to the config file
        self.base_dir = str(get_project_root())
        self.config_file = os.path.join(self.base_dir, "settings.json")
        
        # Current configuration (loaded from file or defaults)
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create with defaults if it doesn't exist"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Ensure all required keys are present by updating with defaults
                    for key, value in self.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                logger.error(f"Error loading config file: {str(e)}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create a new config file with defaults
            config = self.DEFAULT_CONFIG.copy()
            self._save_config(config)
            return config
    
    def _save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving config file: {str(e)}")
            return False
    
    def get_setting(self, key):
        """Get a setting by key"""
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))
    
    def set_setting(self, key, value):
        """Set a setting and save to file"""
        self.config[key] = value
        return self._save_config()
    
    def get_library_path(self):
        """Get the library path setting"""
        return self.get_setting("library_path")
    
    def set_library_path(self, path):
        """Set the library path setting"""
        return self.set_setting("library_path", path)

# Create a singleton instance
config_manager = ConfigManager()
