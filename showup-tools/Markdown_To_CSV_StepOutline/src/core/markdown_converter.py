#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Core Markdown to CSV conversion functionality."""

import os
import re
import csv
import logging
from typing import Dict, List, Optional, Any, Callable

from src.core.api_handler import APIHandler

logger = logging.getLogger("MarkdownConverter")


class MarkdownToCSVConverter:
    """Converts structured Markdown content to CSV format for ShowUpSquared.
    
    This class handles the parsing of structured educational content in markdown format
    and converts it to CSV format suitable for ShowUpSquared platform.
    """
    
    def __init__(self, input_file: str, output_file: str, api_handler: Optional[APIHandler] = None):
        """Initialize the converter with input and output file paths.
        
        Args:
            input_file: Path to the input markdown file
            output_file: Path where the output CSV file will be saved
            api_handler: Optional API handler for AI-assisted enhancements
        """
        self.input_file = input_file
        self.output_file = output_file
        self.api_handler = api_handler
        self.markdown_content = ""
        self.csv_data: List[Dict[str, str]] = []
        
    def load_file(self) -> bool:
        """Load the Markdown file content.
        
        Returns:
            bool: True if file loaded successfully, False otherwise
        """
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                self.markdown_content = file.read()
            logger.info(f"Successfully loaded file: {self.input_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading file {self.input_file}: {str(e)}")
            return False
    
    def extract_modules(self) -> List[Dict[str, Any]]:
        """Extract module sections from markdown content.
        
        Returns:
            List of module dictionaries containing title and content
        """
        modules: List[Dict[str, Any]] = []
        
        # Try multiple module header patterns
        # Pattern 1: Standard markdown headers (# Module Title)
        module_matches = re.finditer(r'# (.+?)\n', self.markdown_content)
        module_positions = [(m.group(1), m.start()) for m in module_matches]
        
        # Pattern 2: Bold module headers like **Module X: Title**
        if not module_positions:
            module_matches = re.finditer(r'\*\*Module\s+(\d+):\s+([^*]+)\*\*', self.markdown_content)
            module_positions = [(f"Module {m.group(1)}: {m.group(2).strip()}", m.start()) 
                              for m in module_matches]
            
        # Process each module's content
        for i, (module_title, module_start) in enumerate(module_positions):
            # Determine end of current module (start of next module or end of file)
            module_end = module_positions[i+1][1] if i < len(module_positions) - 1 else len(self.markdown_content)
            
            # Extract module content
            module_content = self.markdown_content[module_start:module_end].strip()
            
            modules.append({
                'title': module_title.strip(),
                'content': module_content,
                'position': module_start
            })
            
            logger.info(f"Extracted module: {module_title}")
        
        return modules
    
    def extract_lessons(self, module_content: str) -> List[Dict[str, Any]]:
        """Extract lesson sections from a module's content.
        
        Args:
            module_content: The content of a module section
            
        Returns:
            List of lesson dictionaries containing title and content
        """
        lessons: List[Dict[str, Any]] = []
        
        # Try multiple lesson patterns
        # Pattern 1: Standard markdown headers (## Lesson Title)
        lesson_matches = re.finditer(r'## (.+?)\n', module_content)
        lesson_positions = [(m.group(1), m.start()) for m in lesson_matches]
        
        # Pattern 2: Numbered lesson headers (1. Lesson Title)
        if not lesson_positions:
            lesson_matches = re.finditer(r'(\d+\.\s+)([A-Z][^\n.]+)', module_content)
            lesson_positions = [(m.group(2), m.start()) for m in lesson_matches]
        
        # Pattern 3: Bold headings that could be lessons
        if not lesson_positions:
            lesson_matches = re.finditer(r'\*\*([A-Z][^*:]{4,})\*\*', module_content)
            lesson_positions = [(m.group(1), m.start()) for m in lesson_matches]
            
        # Process each lesson's content
        for i, (lesson_title, lesson_start) in enumerate(lesson_positions):
            lesson_end = lesson_positions[i+1][1] if i < len(lesson_positions) - 1 else len(module_content)
            
            # Extract lesson content
            lesson_content = module_content[lesson_start:lesson_end].strip()
            
            lessons.append({
                'title': lesson_title.strip(),
                'content': lesson_content,
                'position': lesson_start
            })
        
        # If no lessons found, create a single lesson from the module content
        if not lessons:
            # Extract the first sentence or use a default title
            first_sentence = re.search(r'([^.!?]+[.!?])', module_content)
            lesson_title = first_sentence.group(1).strip() if first_sentence else "Module Content"
            
            lessons.append({
                'title': lesson_title[:50] + ('...' if len(lesson_title) > 50 else ''),  # Truncate long titles
                'content': module_content,
                'position': 0
            })
            
        return lessons
    
    def extract_steps(self, lesson_content: str) -> List[Dict[str, Any]]:
        """Extract individual steps from a lesson's content.
        
        Args:
            lesson_content: The content of a lesson section
            
        Returns:
            List of step dictionaries containing step details
        """
        steps: List[Dict[str, Any]] = []
        
        # Try multiple step patterns
        # Pattern 1: Standard markdown headers (### Step Title)
        step_matches = re.finditer(r'### (.+?)\n', lesson_content)
        step_positions = [(m.group(1), m.start()) for m in step_matches]
        
        # Pattern 2: Bulleted items with bold text
        if not step_positions:
            step_matches = re.finditer(r'[\*\-•]\s+\*\*([^*]+?)\*\*', lesson_content)
            step_positions = [(m.group(1), m.start()) for m in step_matches]
        
        # Pattern 3: Numbered items with bold first part
        if not step_positions:
            step_matches = re.finditer(r'\d+\.\s+\*\*([^*]+?)\*\*', lesson_content)
            step_positions = [(m.group(1), m.start()) for m in step_matches]
            
        # Process each step's content
        for i, (step_title, step_start) in enumerate(step_positions):
            step_end = step_positions[i+1][1] if i < len(step_positions) - 1 else len(lesson_content)
            
            # Extract step content
            step_content_raw = lesson_content[step_start:step_end].strip()
            
            # Split the title line from the rest of the content
            content_lines = step_content_raw.split('\n', 1)
            step_content = content_lines[1].strip() if len(content_lines) > 1 else step_content_raw
            
            # Extract step type, rationale, and content
            step_info = self._parse_step_content(step_title, step_content)
            
            steps.append(step_info)
        
        # If no steps found, create a single step from the lesson content
        if not steps:
            # Use the lesson content as a single step
            step_title = lesson_content.split('\n', 1)[0].strip()[:50]  # First line, limited to 50 chars
            
            # Clean title of markdown formatting
            step_title = re.sub(r'\*\*|__|##|\*|_', '', step_title)  # Remove formatting marks
            step_title = re.sub(r'^\d+\.\s+', '', step_title)  # Remove leading numbers
            
            step_info = self._parse_step_content(step_title, lesson_content)
            steps.append(step_info)
            
        return steps
    
    def _parse_step_content(self, step_title: str, step_content: str) -> Dict[str, Any]:
        """Parse the content of a single step to extract metadata.
        
        Args:
            step_title: The title of the step
            step_content: The content of the step
            
        Returns:
            Dictionary containing parsed step information
        """
        # Default values
        step_info = {
            'title': step_title.strip(),
            'content': step_content,
            'type': 'Content',  # Default type
            'rationale': '',
            'content_outline': ''
        }
        
        # Extract step type if specified
        type_match = re.search(r'\*\*Type:\*\*\s*(.+?)(?:\n|$)', step_content)
        if type_match:
            step_info['type'] = type_match.group(1).strip()
        elif self.api_handler and self.api_handler.is_available():
            # Use AI to classify step type if not explicitly defined
            step_info['type'] = self.api_handler.classify_step_type(step_content)
        
        # Extract rationale if specified
        rationale_match = re.search(r'\*\*Rationale:\*\*\s*(.+?)(?:\n\n|$)', step_content)
        if rationale_match:
            step_info['rationale'] = rationale_match.group(1).strip()
        elif self.api_handler and self.api_handler.is_available():
            # Generate rationale if not explicitly defined
            step_info['rationale'] = self.api_handler.generate_rationale(
                step_info['title'], step_content
            )
        
        # Extract content outline
        outline_match = re.search(r'\*\*Content Outline:\*\*\s*(.+?)(?:\n\n|$)', step_content, re.DOTALL)
        if outline_match:
            step_info['content_outline'] = outline_match.group(1).strip()
        elif self.api_handler and self.api_handler.is_available():
            # Generate content outline if not explicitly defined
            step_info['content_outline'] = self.api_handler.generate_content_outline(step_content)
        
        return step_info
    
    def convert(self, progress_callback: Optional[Callable[[float, str], None]] = None) -> bool:
        """Execute the full markdown to CSV conversion process.
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        try:
            # Load the markdown file
            if not self.load_file():
                return False
            
            if progress_callback:
                progress_callback(0.1, "Markdown file loaded successfully")
            
            # Extract modules
            modules = self.extract_modules()
            if not modules:
                logger.error("No modules found in markdown content")
                if progress_callback:
                    progress_callback(0.2, "No modules found in markdown content")
                return False
            
            if progress_callback:
                progress_callback(0.3, f"Extracted {len(modules)} modules")
            
            # Process each module, lesson, and step
            total_steps = 0
            for module_idx, module in enumerate(modules):
                # Extract lessons in this module
                lessons = self.extract_lessons(module['content'])
                
                # Update progress
                if progress_callback:
                    progress_value = 0.3 + (0.6 * (module_idx / len(modules)))
                    progress_callback(progress_value, f"Processing module {module_idx+1}/{len(modules)}")
                
                # Process each lesson
                for lesson_idx, lesson in enumerate(lessons):
                    # Extract steps in this lesson
                    steps = self.extract_steps(lesson['content'])
                    
                    # Add each step to the CSV data
                    for step_idx, step in enumerate(steps):
                        self.csv_data.append({
                            'Module': module['title'],
                            'Lesson': lesson['title'],
                            'Step': step['title'],
                            'Type': step['type'],
                            'Rationale': step['rationale'],
                            'Content': step['content'],
                            'ContentOutline': step['content_outline']
                        })
                        total_steps += 1
            
            # If no steps were found, create at least one row per module
            if total_steps == 0:
                logger.warning("No detailed steps found, creating module-level entries")
                for module in modules:
                    # Create a module-level entry
                    self.csv_data.append({
                        'Module': module['title'],
                        'Lesson': 'Module Overview',
                        'Step': module['title'],
                        'Type': 'Content',
                        'Rationale': f"Understanding {module['title']} is essential for this orientation.",
                        'Content': module['content'],
                        'ContentOutline': '- Key content in this module'
                    })
                    total_steps += 1
            
            # Write the CSV file
            self._write_csv()
            
            if progress_callback:
                progress_callback(1.0, "Conversion complete")
            
            logger.info(f"Conversion completed successfully: {total_steps} steps processed")
            return True
            
        except Exception as e:
            logger.error(f"Error during conversion: {str(e)}")
            if progress_callback:
                progress_callback(1.0, f"Error: {str(e)}")
            return False
    
    def _write_csv(self) -> None:
        """Write the extracted data to a CSV file."""
        # Create output directory if needed
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Define CSV field names
        fieldnames = ['Module', 'Lesson', 'Step', 'Type', 'Rationale', 'Content', 'ContentOutline']
        
        # Write to CSV file
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.csv_data)
        
        logger.info(f"CSV file written successfully: {self.output_file}")
