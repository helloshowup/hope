#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for variable-length pause SSML markers in fitness audio processor.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fitness_podcaster.audio_processor import rewrite_markers, convert_break_duration


class TestPauseVariants(unittest.TestCase):
    """Test cases for variable-length pause SSML markers."""
    
    def test_default_pause(self) -> None:
        """Test that [pause] produces the default 650ms break."""
        input_text = "Let's take a moment to prepare. [pause] Now we're ready."
        expected = "Let's take a moment to prepare. <break time=\"650ms\"/> Now we're ready."
        result = rewrite_markers(input_text)
        self.assertIn("<break time=\"650ms\"/>", result)
        
    def test_seconds_pause(self) -> None:
        """Test that [pause 2s] converts to milliseconds correctly."""
        input_text = "Deep breath in. [pause 2s] And exhale."
        result = rewrite_markers(input_text)
        self.assertIn("<break time=\"2000ms\"/>", result)
        
    def test_milliseconds_pause(self) -> None:
        """Test that [pause 1500ms] passes through correctly."""
        input_text = "Hold the position. [pause 1500ms] And release."
        result = rewrite_markers(input_text)
        self.assertIn("<break time=\"1500ms\"/>", result)
        
    def test_decimal_seconds_pause(self) -> None:
        """Test that [pause 0.5s] converts to milliseconds correctly."""
        input_text = "Quick breath. [pause 0.5s] Continue."
        result = rewrite_markers(input_text)
        self.assertIn("<break time=\"500ms\"/>", result)
        
    def test_convert_break_duration(self) -> None:
        """Test the convert_break_duration helper function directly."""
        self.assertEqual(convert_break_duration(None), "650ms")
        self.assertEqual(convert_break_duration(""), "650ms")
        self.assertEqual(convert_break_duration("2s"), "2000ms")
        self.assertEqual(convert_break_duration("1.5s"), "1500ms")
        self.assertEqual(convert_break_duration("800ms"), "800ms")
        self.assertEqual(convert_break_duration("3"), "3000ms")
        self.assertEqual(convert_break_duration("invalid"), "650ms")


if __name__ == '__main__':
    unittest.main()
