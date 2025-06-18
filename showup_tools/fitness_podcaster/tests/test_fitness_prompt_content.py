#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for fitness content preparation function to ensure it contains required phrases.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fitness_podcaster.text_processing import prepare_fitness_content_for_prompt


class TestFitnessPromptContent(unittest.TestCase):
    """Test cases for the fitness content preparation function."""
    
    def test_prompt_contains_required_phrases(self) -> None:
        """Test that the formatted prompt contains required phrases for fitness instruction."""
        # Create a test file path
        test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_data/sample_exercise.md'))
        
        # Create test directory if it doesn't exist
        test_dir = os.path.dirname(test_file)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        # Create a simple test file with exercise content
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("# Wall Push-ups\n\nA beginner-friendly upper body exercise.\n\n")
            f.write("## Form\n\n* Stand at arm's length from a wall\n* Place palms flat against the wall\n")
            f.write("* Bend elbows to bring chest toward wall\n* Push back to starting position\n")
        
        try:
            # Call the function with our test file
            result = prepare_fitness_content_for_prompt([test_file])
            
            # Check that the required phrases are in the result
            self.assertIn("guides a learner through the exercise", result)
            self.assertIn("action-oriented cues", result)
            self.assertIn("audio-friendly", result)
            self.assertIn("asynchronous learners", result)
            self.assertIn("adult learners at any fitness level", result)
            
            # Check that the old phrases from educational content are NOT in the result
            self.assertNotIn("middle school students", result)
            self.assertNotIn("classroom language", result)
            
            print("Test passed: Fitness prompt contains all required phrases")
        finally:
            # Clean up - remove the test file
            if os.path.exists(test_file):
                os.remove(test_file)
            
            # Remove the test directory if it's empty
            if os.path.exists(test_dir) and not os.listdir(test_dir):
                os.rmdir(test_dir)


if __name__ == '__main__':
    unittest.main()
