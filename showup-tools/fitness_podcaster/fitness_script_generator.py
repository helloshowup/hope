#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fitness script generation module for fitness instructor voiceover generator.

Handles the creation of fitness instruction scripts using OpenAI API and script validation.
"""

import os
import re
import logging
import math
import requests
from dotenv import load_dotenv
import sys

# Ensure we can find the root directory to load the .env file
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the root directory to sys.path if it's not already there
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Load .env file from the root directory
env_path = os.path.join(root_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    
logger = logging.getLogger('fitness_instructor_voiceover')

# Check for OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables")


def _generate_fitness_script_internal(content: str, target_audience: str, word_limit: int = 500) -> str:
    """Internal script generation without validation - used by regeneration process."""
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key not found. Please check your .env file."
    
    try:
        # Fitness instructor specialized system prompt
        system_prompt = (
            f"You are an expert fitness script writer creating an audio script for the Azure Neural TTS Andrew voice (DragonHD). Create a {word_limit}-word script for a single exercise that will be processed with SSML tags.\n\n"
            "VOICE CHARACTERISTICS:\n"
            "- Male voice with medium-deep tone, moderate pace, natural-sounding\n"
            "- Optimized for clear pronunciation of technical fitness terms\n"
            "- Works best with shorter sentences (10-15 words) and natural pauses\n\n"
            
            "SCRIPT FORMAT:\n"
            "1. No 'Instructor:' labels anywhere - these cause audio artifacts\n"
            "2. Structure in 3 sections:\n"
            f"   - Brief welcome & setup ({math.floor(word_limit*0.05)}-{math.floor(word_limit*0.08)} words)\n"
            f"   - Main instruction segment ({int(word_limit*0.75)}-{int(word_limit*0.8)} words)\n"
            f"   - Brief conclusion ({int(word_limit*0.1)}-{int(word_limit*0.15)} words)\n\n"
            
            "SPECIAL MARKUP:\n"
            "- Use [pause] for pauses between instructions (converts to SSML break tags)\n" 
            "- For longer pauses, specify duration: [pause 2s] or [pause 3s]\n"
            "- Mark important cues with [emphasis]important form cue[/emphasis]\n"
            "- For stronger emphasis use [emphasis strong]critical reminder[/emphasis]\n\n"
            
            "COUNTING FORMAT:\n"
            "For exercise repetitions, use this exact format (optimized for voice):\n"
            "One – [emphasis]specific form cue[/emphasis] [pause]\n"
            "Two – [emphasis]another form cue[/emphasis] [pause]\n\n"
            
            "EXERCISE CONTENT REQUIREMENTS:\n"
            "- State specific exercise clearly at the beginning\n"
            "- Mention primary non-generic benefit of the exercise\n"
            "- Include one key safety reminder specific to the exercise\n"
            "- Describe starting position in detail\n"
            "- Lead through repetitions using the counting format above\n"
            "- Include a success check after initial instructions\n"
            "- Offer a modification option (easier or more challenging)\n"
            "- Summarize benefits in the conclusion\n\n"
            
            "CRITICAL TTS OPTIMIZATION REQUIREMENTS:\n"
            "- No 'Instructor:' labels (causes voice artifacts)\n"
            "- Keep sentences short (8-15 words) for better TTS performance\n"
            "- Use proper nouns and technical terms sparingly as they may be mispronounced\n"
            "- Balance instructional language with motivational cues\n"
            "- Always include [pause] after each numbered repetition\n"
            "- Include a [pause 3s] after the final repetition\n"
            "- Do NOT imply the instructor is physically present or watching the learner\n"
            "- Use simple, direct language\n"
            "- Avoid overused fitness clichés like 'No pain, no gain'\n"
        )
        
        # Call OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4.1",  # Using the latest model
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
        )
        
        if response.status_code == 200:
            script = response.json()["choices"][0]["message"]["content"]
            logger.info("Fitness instruction script generated successfully")
            return script
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return f"Error generating fitness script: {error_msg}"
            
    except Exception as e:
        error_msg = f"Error generating fitness script: {str(e)}"
        logger.error(error_msg)
        return error_msg


def validate_fitness_script(script: str) -> tuple:
    """Validate the fitness instruction script."""
    # Count words for informational purposes
    words = re.findall(r'\b\w+\b', script)
    word_count = len(words)
    logger.info(f"Fitness script word count: {word_count}")
    
    # Check for instructor labels
    instructor_blocks = re.findall(r'Instructor:', script, re.IGNORECASE)
    if len(instructor_blocks) < 3:  # At least opening, main content, and closing
        return False, "Script needs more clearly labeled instruction blocks"
    
    # Check for exercise instructions
    exercise_cues = ['position', 'form', 'breathe', 'engage', 'hold', 'repeat', 'seconds', 'sets', 'reps']
    cues_found = sum(1 for cue in exercise_cues if cue.lower() in script.lower())
    if cues_found < 4:  # At least 4 different exercise cues
        return False, "Script needs more detailed exercise instructions and cues"
    
    return True, "Fitness script validation passed"


def _regenerate_fitness_script_if_needed(script: str, content: str, target_audience: str, word_limit: int = 500, max_attempts=3) -> str:
    """Regenerate fitness script if validation fails, with max attempts."""
    attempt = 1
    current_script = script
    
    while attempt <= max_attempts:
        valid, message = validate_fitness_script(current_script)
        if valid:
            logger.info(f"Fitness script validation passed after {attempt} attempts")
            return current_script
        
        logger.warning(f"Fitness script validation failed (attempt {attempt}/{max_attempts}): {message}")
        
        # Add additional feedback to the system prompt based on validation failure
        additional_feedback = ""
        if "more clearly labeled" in message.lower():
            additional_feedback = "Include more 'Instructor:' labels to clearly mark different sections of the workout."
        elif "more detailed exercise instructions" in message.lower():
            additional_feedback = "Include specific form cues, breathing instructions, and timing for each exercise."
        else:
            additional_feedback = message  # Use the full validation message
        
        # Generate new script with feedback using the internal method directly
        if attempt < max_attempts:
            modified_content = content + "\n\nIMPORTANT FEEDBACK: " + additional_feedback
            attempt += 1
            # Use internal method to avoid recursion
            current_script = _generate_fitness_script_internal(modified_content, target_audience, word_limit)
            
            # If generation failed, exit the loop
            if current_script.startswith("Error"):
                logger.error(f"Fitness script regeneration failed on attempt {attempt}: {current_script}")
                break
        else:
            logger.error(f"Failed to generate valid fitness script after {max_attempts} attempts")
            # Return the best script we have, with a warning prepended
            return f"// Note: This fitness script may not meet all quality guidelines. Please review carefully.\n\n{current_script}"
    
    return current_script


def generate_fitness_script(content: str, target_audience: str, word_limit: int = 500) -> str:
    """Generate fitness instruction script using OpenAI API with optimized prompt."""
    # Generate the script using the internal method
    script = _generate_fitness_script_internal(content, target_audience, word_limit)
    
    # Skip validation if there was an error
    if script.startswith("Error"):
        return script
    
    # Log the word count for information purposes only
    word_count = len(script.split())
    logger.info(f"Fitness script word count: {word_count}")
    
    # Accept the first generated script without validation
    logger.info("Accepting first generated script without validation")
    
    return script
