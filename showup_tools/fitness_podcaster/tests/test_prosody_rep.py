#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for prosody boost on rep counting lines in fitness audio processor.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fitness_podcaster.audio_processor import rewrite_markers


class TestProsodyRep(unittest.TestCase):
    """Test cases for prosody boost on rep counting lines."""
    
    def test_prosody_applied_to_rep_lines(self) -> None:
        """Test that lines starting with rep words get prosody boost."""
        # Test each number word from One to Ten
        number_words = [
            "One", "Two", "Three", "Four", "Five", 
            "Six", "Seven", "Eight", "Nine", "Ten"
        ]
        
        for word in number_words:
            input_text = f"{word} more rep, push through it!"
            result = rewrite_markers(input_text)
            
            expected_start = f'<prosody rate="+5%" volume="+1dB">{word}'
            self.assertTrue(
                result.startswith(expected_start), 
                f"Line starting with '{word}' should have prosody boost"
            )
            self.assertIn("</prosody>", result)
    
    def test_prosody_not_applied_to_non_rep_lines(self) -> None:
        """Test that lines not starting with rep words don't get prosody boost."""
        # Test with various non-rep line starters
        non_rep_starters = [
            "Now", "Let's", "Great", "Keep", "The", "one more set"
        ]
        
        for starter in non_rep_starters:
            input_text = f"{starter} going with the exercise!"
            result = rewrite_markers(input_text)
            
            self.assertFalse(
                result.startswith('<prosody'), 
                f"Line starting with '{starter}' should NOT have prosody boost"
            )
    
    def test_prosody_only_triggers_at_start_of_line(self) -> None:
        """Test that number words in the middle of text don't trigger prosody boost."""
        input_text = "Let's do Ten more reps now!"
        result = rewrite_markers(input_text)
        
        self.assertFalse(
            '<prosody' in result,
            "Number word in middle of text should not trigger prosody boost"
        )
    
    def test_prosody_comprehensive_parameters(self) -> None:
        """Test that prosody boost includes both rate and volume parameters."""
        input_text = "Eight more seconds, hold it!"
        result = rewrite_markers(input_text)
        
        self.assertIn('rate="+5%"', result)
        self.assertIn('volume="+1dB"', result)


if __name__ == '__main__':
    unittest.main()
