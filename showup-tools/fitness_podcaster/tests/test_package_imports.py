#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script to verify that all imports in the new fitness_podcaster package work correctly.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import from fitness_podcaster package
import fitness_podcaster
from fitness_podcaster import text_processing
from fitness_podcaster import audio_processor
from fitness_podcaster import fitness_script_generator


class TestPackageImports(unittest.TestCase):
    """Test that all imports in the fitness_podcaster package work correctly."""
    
    def test_package_imports(self) -> None:
        """Test that importing the fitness_podcaster package works."""
        self.assertIsNotNone(fitness_podcaster)
        self.assertIsNotNone(fitness_podcaster.__version__)
    
    def test_text_processing_imports(self) -> None:
        """Test that importing text_processing module works."""
        self.assertIsNotNone(text_processing)
        self.assertTrue(hasattr(text_processing, 'prepare_fitness_content_for_prompt'))
        self.assertTrue(callable(text_processing.prepare_fitness_content_for_prompt))
    
    def test_audio_processor_imports(self) -> None:
        """Test that importing audio_processor module works."""
        self.assertIsNotNone(audio_processor)
        self.assertTrue(hasattr(audio_processor, 'DEFAULT_TTS_CONFIG'))
        self.assertTrue(hasattr(audio_processor, 'enhance_fitness_script_with_ssml'))
        self.assertTrue(hasattr(audio_processor, 'convert_fitness_script_to_audio'))
        self.assertTrue(hasattr(audio_processor, 'rewrite_markers'))
        self.assertTrue(hasattr(audio_processor, 'convert_break_duration'))
    
    def test_script_generator_imports(self) -> None:
        """Test that importing fitness_script_generator module works."""
        self.assertIsNotNone(fitness_script_generator)
        self.assertTrue(hasattr(fitness_script_generator, 'generate_fitness_script'))


if __name__ == '__main__':
    unittest.main()
