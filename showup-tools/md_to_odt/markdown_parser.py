"""
Markdown Parser Module

This module handles parsing of Markdown files to extract image references
in both standard and figure-based formats.
"""

import re
import logging

logger = logging.getLogger('md_to_odt.parser')

class ImageReference:
    """Class representing an image reference in a markdown file"""
    
    def __init__(self, reference_text, figure_number=None, description=None, caption=None, position=None):
        """
        Initialize an image reference
        
        Args:
            reference_text: The original reference text from markdown
            figure_number: Optional figure number (e.g., "Fig 1")
            description: The description text for the image
            caption: Optional caption text
            position: Position in the markdown file (line number)
        """
        self.reference_text = reference_text
        self.figure_number = figure_number
        self.description = description
        self.caption = caption
        self.position = position
        self.matched_image = None
        self.modified_caption = None
    
    def __str__(self):
        """String representation of the image reference"""
        return f"ImageReference(figure={self.figure_number}, desc={self.description[:30]}...)"
    
    def get_search_text(self):
        """Get the text to use for image searching"""
        if self.description:
            return self.description
        elif self.caption:
            return self.caption
        return self.reference_text

class MarkdownParser:
    """Parser for extracting image references from markdown files"""
    
    def __init__(self):
        """Initialize the parser"""
        self.logger = logging.getLogger('md_to_odt.parser')
    
    def parse_file(self, file_path):
        """
        Parse a markdown file and extract image references
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            List of ImageReference objects
        """
        self.logger.info(f"Parsing markdown file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Parse content
            image_references = self.parse_content(content)
            
            self.logger.info(f"Found {len(image_references)} image references in {file_path}")
            return image_references
            
        except Exception as e:
            self.logger.error(f"Error parsing markdown file {file_path}: {str(e)}")
            raise
    
    def parse_content(self, content):
        """
        Parse markdown content to extract image references
        
        Args:
            content: Markdown content as string
            
        Returns:
            List of ImageReference objects
        """
        image_references = []
        
        # Try to identify the format by looking for specific patterns
        if self._has_figure_format(content):
            self.logger.info("Detected figure-based format")
            image_references = self._parse_figure_format(content)
        else:
            self.logger.info("Using standard image reference format")
            image_references = self._parse_standard_format(content)
        
        return image_references
    
    def _has_figure_format(self, content):
        """
        Check if the content uses figure-based format
        
        Args:
            content: Markdown content
            
        Returns:
            Boolean indicating if figure format is used
        """
        # Look for patterns like [Image: ... Caption: "Fig X: ...]
        figure_pattern = r'\[Image:.*?Caption:\s*"Fig\s+\d+:'
        # Or standalone figure headers
        header_pattern = r'##\s+Fig\s+\d+'
        
        return bool(re.search(figure_pattern, content, re.DOTALL)) or bool(re.search(header_pattern, content))
    
    def _parse_figure_format(self, content):
        """
        Parse content with figure-based format
        
        Args:
            content: Markdown content
            
        Returns:
            List of ImageReference objects
        """
        image_references = []
        
        # Try first format: [Image: ... Caption: "Fig X: ...]
        image_pattern = r'\[Image:(.*?)Caption:\s*"(Fig\s+\d+):(.*?)"\]'
        matches = re.finditer(image_pattern, content, re.DOTALL)
        
        for match in matches:
            description = match.group(1).strip()
            figure_number = match.group(2).strip()
            caption = match.group(3).strip()
            
            reference = ImageReference(
                reference_text=match.group(0),
                figure_number=figure_number,
                description=description,
                caption=caption
            )
            image_references.append(reference)
        
        # If no matches found, try alternative format with ## Fig X headers
        if not image_references:
            # Split by figure headers
            sections = re.split(r'##\s+Fig\s+\d+', content)
            headers = re.findall(r'##\s+(Fig\s+\d+)', content)
            
            # Process each section
            for i, section in enumerate(sections[1:]):  # Skip first empty section
                if i < len(headers):  # Ensure we have a header for this section
                    figure_number = headers[i]
                    
                    # Extract description (text before suggested terms)
                    description = section.strip()
                    if "Suggested search terms:" in section:
                        description = section.split("Suggested search terms:")[0].strip()
                    
                    reference = ImageReference(
                        reference_text=f"## {figure_number}\n{section}",
                        figure_number=figure_number,
                        description=description
                    )
                    image_references.append(reference)
        
        self.logger.info(f"Parsed {len(image_references)} figure references")
        return image_references
    
    def _parse_standard_format(self, content):
        """
        Parse content with standard image reference format
        
        Args:
            content: Markdown content
            
        Returns:
            List of ImageReference objects
        """
        image_references = []
        
        # Look for [Image: description] pattern
        image_pattern = r'\[Image:(.*?)\]'
        matches = re.finditer(image_pattern, content, re.DOTALL)
        
        for match in matches:
            description = match.group(1).strip()
            
            reference = ImageReference(
                reference_text=match.group(0),
                description=description
            )
            image_references.append(reference)
        
        self.logger.info(f"Parsed {len(image_references)} standard image references")
        return image_references