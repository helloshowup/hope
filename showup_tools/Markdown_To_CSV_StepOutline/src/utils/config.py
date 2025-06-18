#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration utilities for loading environment variables."""

import os
from typing import Dict, Optional
import logging

logger = logging.getLogger("Config")


class ConfigManager:
    """Manages configuration and environment variables for the application."""
    
    def __init__(self) -> None:
        """Initialize configuration manager and load environment variables."""
        self.env_vars: Dict[str, str] = {}
        self.load_env_from_root()
    
    def load_env_from_root(self) -> None:
        """Load environment variables from root .env file."""
        try:
            # Get the root directory of the overall project
            # Start with current directory and try multiple parent directories
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            possible_root_dirs = [
                # Current directory
                current_dir,
                # Parent directory
                os.path.dirname(current_dir),
                # Grandparent directory
                os.path.dirname(os.path.dirname(current_dir)),
                # Great-grandparent directory
                os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            ]
            
            # Try to find .env in any of the possible directories
            env_file_path = None
            for dir_path in possible_root_dirs:
                potential_env_file = os.path.join(dir_path, '.env')
                if os.path.exists(potential_env_file):
                    env_file_path = potential_env_file
                    logger.info(f"Found .env file at: {env_file_path}")
                    break
            
            if env_file_path and os.path.exists(env_file_path):
                logger.info(f"Loading environment from: {env_file_path}")
                with open(env_file_path, 'r', encoding='utf-8') as env_file:
                    for line in env_file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            try:
                                key, value = line.split('=', 1)
                                self.env_vars[key] = value
                                # Only set as environment variable if not already set
                                if key not in os.environ:
                                    os.environ[key] = value
                                    logger.debug(f"Set environment variable: {key}")
                            except ValueError:
                                logger.warning(f"Skipping malformed line in .env file: {line}")
            else:
                logger.warning("No .env file found in any parent directory")
                # Create a dummy entry so the UI knows we looked for it
                self.env_vars["ENV_FILE_FOUND"] = "FALSE"
        except Exception as e:
            logger.error(f"Error loading environment variables: {str(e)}")
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get an environment variable value.
        
        Args:
            key: The environment variable name
            default: Default value if the variable is not found
            
        Returns:
            The value of the environment variable or the default value
        """
        return self.env_vars.get(key, os.environ.get(key, default))
    
    def get_anthropic_api_key(self) -> Optional[str]:
        """Get the Anthropic API key from environment variables."""
        return self.get('ANTHROPIC_API_KEY')
    
    def get_openai_api_key(self) -> Optional[str]:
        """Get the OpenAI API key from environment variables."""
        return self.get('OPENAI_API_KEY')
    
    def get_azure_speech_key(self) -> Optional[str]:
        """Get the Azure Speech key from environment variables."""
        return self.get('AZURE_SPEECH_KEY')
    
    def get_azure_speech_region(self) -> Optional[str]:
        """Get the Azure Speech region from environment variables."""
        return self.get('AZURE_SPEECH_REGION')
