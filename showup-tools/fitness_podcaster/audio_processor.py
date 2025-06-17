#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Audio processing module for fitness instructor voiceover.

Handles the conversion of fitness instruction scripts to audio using Azure TTS and SSML enhancement.
Uses DragonHD voice for high-quality audio outputs, with a temperature setting (0.35) to ensure
energetic performance delivery with appropriate variation - critical for fitness instruction
where clear, motivational pronunciation of exercise terms is essential.
"""

import os
import re
import html
import logging
import azure.cognitiveservices.speech as speechsdk
from typing import Dict, Optional, Match
from datetime import datetime

# Proper voice configuration for Azure Speech Service
VOICE_ID_HD = "en-US-AndrewNeural"
HD_MARKER = True  # Simple bool flag for HD voice

logger = logging.getLogger('fitness_podcaster')

# Default TTS voice configuration for fitness instructor
# Uses a single voice model with a temperature of 0.35 for livelier delivery
DEFAULT_TTS_CONFIG = {
    "fitness_instructor": {
        "voice_name": VOICE_ID_HD,
        "temperature": "0.35"
    }
}


def convert_break_duration(duration_str: str) -> str:
    """Convert a pause duration string to milliseconds for SSML break tags.
    
    Handles formats like '2s', '500ms', or defaults to 650ms if no duration specified.
    """
    if not duration_str:
        return "650ms"  # Default pause duration
    
    # Strip any whitespace
    duration_str = duration_str.strip()
    
    # If already in milliseconds format, return as is
    if duration_str.endswith("ms"):
        try:
            # Verify it's a valid number
            ms_value = int(duration_str[:-2])
            return f"{ms_value}ms"
        except ValueError:
            logger.warning(f"Invalid millisecond format: {duration_str}, using default")
            return "650ms"
    
    # If in seconds format, convert to milliseconds
    if duration_str.endswith("s"):
        try:
            seconds = float(duration_str[:-1])
            ms_value = int(seconds * 1000)
            return f"{ms_value}ms"
        except ValueError:
            logger.warning(f"Invalid seconds format: {duration_str}, using default")
            return "650ms"
    
    # If just a number, assume seconds and convert
    try:
        seconds = float(duration_str)
        ms_value = int(seconds * 1000)
        return f"{ms_value}ms"
    except ValueError:
        logger.warning(f"Invalid duration format: {duration_str}, using default")
        return "650ms"


def _get_optimized_emphasis(level: str, text: str) -> str:
    """Creates voice-optimized emphasis for Andrew/Dragon voice based on emphasis level."""
    if level == "strong":
        return f'<emphasis level="strong">{text}</emphasis>'
    elif level == "moderate":
        return f'<emphasis level="moderate">{text}</emphasis>'
    elif level == "reduced":
        return f'<emphasis level="reduced">{text}</emphasis>'
    return f'<emphasis level="moderate">{text}</emphasis>'


def rewrite_markers(text: str) -> str:
    """Convert emphasis and pause markers to SSML tags with enhanced features for Azure Dragon voice."""
    # Optimize emphasis markers for Dragon voice - using proper Azure-specific prosody
    text = re.sub(r'\[emphasis(?: (strong|moderate|reduced))?\]\s*(.*?)\s*(\[\/emphasis\]|\])', 
                lambda m: _get_optimized_emphasis(m.group(1) or "moderate", m.group(2)), 
                text)
    
    # Process variable-length pause markers with robust error handling
    # Format: [pause] or [pause 2s] or [pause 1500ms]
    def _pause_repl(match: Match) -> str:
        dur = convert_break_duration(match.group(1))
        return f'<break time="{dur}"/>'
    
    text = re.sub(r'\[pause(?: ([^\]]+))?\]',
                _pause_repl,
                text)
    
    # Optimized pattern for adding pauses at sentence boundaries
    text = re.sub(r'(\.\s+)([A-Z])', r'.<break time="350ms"/> \2', text)
    
    # Simplified pattern for adding slight pauses after commas
    text = re.sub(r'(,\s+)([a-zA-Z])', r',<break time="150ms"/> \2', text)
    
    # Add prosody settings for rep counting - as a single pass with consistent prosody values
    # This avoids nested prosody tags that conflict with each other
    text = re.sub(r'^(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\b\s*[-\u2013]\s*(.*?)$',
                r'<prosody rate="-5%" pitch="+10%">\1 - \2</prosody>',
                text, 
                flags=re.MULTILINE)
    
    return text


def contains_ssml(text: str) -> bool:
    """Check if text already contains SSML tags to prevent nesting."""
    return '<speak' in text or '<voice' in text


def enhance_fitness_script_with_ssml(script: str, tts_config: Optional[Dict[str, Dict[str, str]]] = None) -> str:
    """Transform fitness instruction script into SSML-enhanced output."""
    if tts_config is None:
        tts_config = DEFAULT_TTS_CONFIG
    
    # Reject scripts that already contain SSML to prevent nesting
    if contains_ssml(script):
        logger.error("Script already contains SSML tags. Cannot process.")
        # Return a minimally valid SSML document with an error message
        return ('<?xml version="1.0"?>\n'
                '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
                'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n'
                '<voice name="en-US-AndrewNeural">\n'
                '<p>Error: Input script already contains SSML tags. Cannot process.</p>\n'
                '</voice>\n'
                '</speak>')
    
    # Remove 'Instructor:' labels from the beginning of lines
    script = re.sub(r'^\s*Instructor:\s*', '', script, flags=re.MULTILINE)
    
    # Create a valid SSML document
    ssml_output = '<?xml version="1.0"?>\n'
    ssml_output += '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
    ssml_output += 'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n'

    # Apply fitness instructor voice characteristics
    voice_config = tts_config["fitness_instructor"]
    voice_name = voice_config["voice_name"]
    temperature = voice_config.get("temperature", "0.35")
    
    # Open one <voice> wrapper for the whole script
    ssml_output += f'<voice name="{voice_name}" parameters="temperature={temperature}">\n'
    
    # Add global prosody settings optimized for fitness instruction
    ssml_output += '<prosody rate="-5%" pitch="+2%" volume="+10%">\n'
    
    # Process each paragraph 
    paragraphs = script.split('\n\n')
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # First escape XML special characters
        content = html.escape(paragraph)
        
        # Then process markers by converting them to actual SSML tags
        # This ensures the markers become proper SSML tags, not escaped entities
        content = rewrite_markers(content)
        
        # Add paragraph tag around content
        ssml_output += f'<p>{content}</p>\n'
    
    # Close the prosody tag
    ssml_output += '</prosody>\n'
    # Close the voice and speak tags
    ssml_output += '</voice>\n'
    ssml_output += '</speak>'
    
    logger.debug(f"Generated SSML:\n{ssml_output}")
    return ssml_output


def convert_fitness_script_to_audio(script: str, tts_config: Optional[Dict[str, Dict[str, str]]] = None, 
                                 output_dir: Optional[str] = None) -> str:
    """Convert fitness instruction script to audio using Azure TTS with SSML enhancement."""
    # Use fitness-specific SSML enhancement
    ssml_script = enhance_fitness_script_with_ssml(script, tts_config)
    
    # If no output directory is specified, use the default generated_fitness_audio directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "generated_fitness_audio")
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"fitness_instruction_{timestamp}.mp3"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the SSML to a file for review
    ssml_filename = f"fitness_instruction_{timestamp}.ssml"
    ssml_path = os.path.join(output_dir, ssml_filename)
    with open(ssml_path, 'w', encoding='utf-8') as f:
        f.write(ssml_script)
    logger.info(f"SSML saved to {ssml_path} for review")
    
    # Convert to audio using Azure Speech service directly
    try:
        # Get subscription key and region from environment variables
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not speech_key or not speech_region:
            logger.error("Azure Speech credentials not found in environment variables")
            raise ValueError("Missing Azure Speech credentials. Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
        
        # Configure speech synthesizer
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        
        # Configure audio output
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        logger.debug(f"SSML script to synthesize:\n{ssml_script}")
        
        # Synthesize speech
        result = speech_synthesizer.speak_ssml_async(ssml_script).get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.info(f"Speech synthesis completed for {output_filename}")
            return output_path
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
            logger.error(f"Speech synthesis error details: {cancellation_details.error_details}")
            raise Exception(f"Speech synthesis failed: {cancellation_details.reason}")
        else:
            logger.warning(f"Speech synthesis result: {result.reason}")
            return output_path
    
    except Exception as e:
        logger.error(f"Error in speech synthesis: {str(e)}")
        raise
