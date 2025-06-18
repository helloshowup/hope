#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the fitness instructor voice configuration.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fitness_podcaster.audio_processor import DEFAULT_TTS_CONFIG


class TestVoiceConfig(unittest.TestCase):
    """Test cases for the fitness instructor voice configuration."""
    
    def test_fitness_instructor_voice_config(self) -> None:
        """Test that the fitness instructor voice configuration is correctly defined."""
        # Check that the fitness_instructor key exists in the DEFAULT_TTS_CONFIG
        self.assertIn("fitness_instructor", DEFAULT_TTS_CONFIG, 
                     "DEFAULT_TTS_CONFIG should contain 'fitness_instructor' key")
        
        # Get the voice configuration
        config = DEFAULT_TTS_CONFIG["fitness_instructor"]
        
        # Check the voice name
        self.assertIn("voice_name", config, 
                     "Fitness instructor config should contain 'voice_name'")
        self.assertTrue(config["voice_name"].startswith("en-US-Andrew"), 
                       "Fitness instructor voice should use 'en-US-Andrew'")
        self.assertIn(":DragonHD", config["voice_name"], 
                     "Fitness instructor voice should use DragonHD voice quality")
        
        # Check the temperature setting
        self.assertIn("temperature", config, 
                     "Fitness instructor config should contain 'temperature'")
        self.assertEqual(config["temperature"], "0.25", 
                       "Fitness instructor temperature should be set to '0.25'")
        
        # Ensure specialist2 key doesn't exist to avoid ambiguity
        self.assertNotIn("specialist2", DEFAULT_TTS_CONFIG, 
                        "DEFAULT_TTS_CONFIG should not contain 'specialist2' key")
        self.assertNotIn("specialist1", DEFAULT_TTS_CONFIG, 
                        "DEFAULT_TTS_CONFIG should not contain 'specialist1' key")
        
        print("Test passed: Fitness instructor voice configuration validated")


if __name__ == '__main__':
    unittest.main()
