#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Markdown processor module for batch processing fitness instruction files.

Handles scanning directories for markdown files, extracting content, and generating
fitness voiceovers in batch mode.
"""

import os
import re
import sys
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Add the project root to system path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import fitness modules
from fitness_podcaster.fitness_script_generator import generate_fitness_script
from fitness_podcaster.audio_processor import convert_fitness_script_to_audio

# Configure logging
logger = logging.getLogger('fitness_podcaster')

# Global pause flag for thread control
pause_flag = False
cancel_flag = False


def scan_directory_for_markdown_files(directory_path: str) -> List[str]:
    """
    Returns a list of paths to all markdown files in the specified directory.
    Searches recursively through all subdirectories.
    """
    markdown_files = []
    
    try:
        # Walk through directory and all subdirectories
        for root, _, files in os.walk(directory_path):
            for file in files:
                # Check if file is a markdown file
                if file.lower().endswith(('.md', '.markdown')):
                    file_path = os.path.join(root, file)
                    markdown_files.append(file_path)
        
        logger.info(f"Found {len(markdown_files)} markdown files in {directory_path}")
        return markdown_files
    
    except Exception as e:
        logger.error(f"Error scanning directory {directory_path}: {str(e)}")
        return []


def extract_filename_and_content(markdown_file_path: str) -> Tuple[str, str]:
    """
    Parses the markdown file to extract the specified filename and content.
    Returns a tuple containing (filename, content).
    
    Looks for patterns like:
    File name: example.mp3
    Content to be covered: Exercise instructions...
    """
    try:
        # Read the markdown file
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract filename if specified
        filename_match = re.search(r'File name:\s*([\w\.-]+\.mp3)', content)
        output_filename = ""
        
        if filename_match:
            output_filename = filename_match.group(1).strip()
            # Remove the filename part from content to be processed
            content = re.sub(r'File name:\s*[\w\.-]+\.mp3', '', content)
        else:
            # Use the markdown filename but with .mp3 extension
            base_name = os.path.basename(markdown_file_path)
            name_without_ext = os.path.splitext(base_name)[0]
            output_filename = f"{name_without_ext}.mp3"
        
        # Extract content section if specified
        content_match = re.search(r'Content to be covered:(.*?)(?=File name:|$)', content, re.DOTALL)
        if content_match:
            extracted_content = content_match.group(1).strip()
        else:
            # Use the entire file content
            extracted_content = content.strip()
        
        # Ensure output filename has .mp3 extension
        if not output_filename.lower().endswith('.mp3'):
            output_filename += '.mp3'
        
        logger.debug(f"Extracted filename: {output_filename} from {markdown_file_path}")
        return (output_filename, extracted_content)
    
    except Exception as e:
        logger.error(f"Error extracting content from {markdown_file_path}: {str(e)}")
        # Return default filename based on the markdown file
        base_name = os.path.basename(markdown_file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        return (f"{name_without_ext}.mp3", "")


def process_markdown_file(file_path: str, output_dir: str, 
                       target_audience: str = "Adult fitness enthusiasts", 
                       word_limit: int = 500,
                       tts_config: Optional[Dict[str, Dict[str, str]]] = None) -> Tuple[bool, str]:
    """
    Processes a single markdown file and generates the audio output.
    Returns a tuple containing (success_status, output_file_path_or_error_message).
    """
    try:
        logger.info(f"Processing {file_path}...")
        
        # Extract filename and content
        output_filename, content = extract_filename_and_content(file_path)
        
        if not content:
            error_msg = f"No content extracted from {file_path}"
            logger.error(error_msg)
            return (False, error_msg)
        
        # Generate fitness script
        script = generate_fitness_script(content, target_audience, word_limit)
        
        if script.startswith("Error"):
            logger.error(f"Error generating script for {file_path}: {script}")
            return (False, script)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create full output path
        output_path = os.path.join(output_dir, output_filename)
        
        # Convert script to audio
        audio_file = convert_fitness_script_to_audio(script, tts_config, output_dir)
        
        if audio_file and os.path.exists(audio_file):
            # Rename if the returned path doesn't match our desired output filename
            if os.path.basename(audio_file) != output_filename:
                target_path = output_path
                try:
                    # If target already exists, don't overwrite
                    if os.path.exists(target_path):
                        base, ext = os.path.splitext(target_path)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        target_path = f"{base}_{timestamp}{ext}"
                    
                    os.rename(audio_file, target_path)
                    audio_file = target_path
                except Exception as e:
                    logger.warning(f"Could not rename {audio_file} to {output_filename}: {str(e)}")
            
            logger.info(f"Successfully processed {file_path} to {audio_file}")
            return (True, audio_file)
        else:
            error_msg = f"Failed to generate audio for {file_path}"
            logger.error(error_msg)
            return (False, error_msg)
    
    except Exception as e:
        error_msg = f"Error processing {file_path}: {str(e)}"
        logger.error(error_msg)
        return (False, error_msg)


def batch_process_directory(input_dir: str, output_dir: str, 
                          target_audience: str = "Adult fitness enthusiasts", 
                          word_limit: int = 500,
                          progress_callback=None, 
                          status_callback=None) -> Dict[str, List[str]]:
    """
    Processes all markdown files in the specified directory.
    Returns a dictionary with lists of successful and failed files.
    
    If callbacks are provided, they will be called to update progress and status:
    - progress_callback(current_index, total_files)
    - status_callback(file_path, success, message)
    """
    global pause_flag, cancel_flag
    
    # Reset control flags
    pause_flag = False
    cancel_flag = False
    
    results = {
        "successful": [],
        "failed": []
    }
    
    try:
        # Find all markdown files
        markdown_files = scan_directory_for_markdown_files(input_dir)
        total_files = len(markdown_files)
        
        if total_files == 0:
            logger.warning(f"No markdown files found in {input_dir}")
            if status_callback:
                status_callback(None, False, f"No markdown files found in {input_dir}")
            return results
        
        # Process each file
        for i, file_path in enumerate(markdown_files):
            # Check for cancellation
            if cancel_flag:
                logger.info("Batch processing canceled")
                if status_callback:
                    status_callback(None, False, "Batch processing canceled")
                break
            
            # Check for pause
            while pause_flag and not cancel_flag:
                # Wait while paused
                import time
                time.sleep(0.5)
            
            # Update progress
            if progress_callback:
                progress_callback(i, total_files)
            
            # Process file
            success, message = process_markdown_file(
                file_path, output_dir, target_audience, word_limit)
            
            # Track result
            if success:
                results["successful"].append(file_path)
            else:
                results["failed"].append(file_path)
            
            # Update status
            if status_callback:
                status_callback(file_path, success, message)
        
        # Final progress update
        if progress_callback and not cancel_flag:
            progress_callback(total_files, total_files)
        
        logger.info(f"Batch processing complete. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")
        return results
    
    except Exception as e:
        error_msg = f"Error during batch processing: {str(e)}"
        logger.error(error_msg)
        if status_callback:
            status_callback(None, False, error_msg)
        return results


def pause_processing():
    """Pause the batch processing."""
    global pause_flag
    pause_flag = True
    logger.info("Batch processing paused")


def resume_processing():
    """Resume the batch processing."""
    global pause_flag
    pause_flag = False
    logger.info("Batch processing resumed")


def cancel_processing():
    """Cancel the batch processing."""
    global cancel_flag
    cancel_flag = True
    logger.info("Batch processing canceled")
