"""
Image Analyzer Module

This module handles analyzing and selecting the best image when multiple
images match a reference, using Claude API for image analysis.
"""

import os
import base64
import io
import json
import logging
from PIL import Image
import sys

# Import Claude API from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from claude_api import generate_with_claude_sonnet
except ImportError:
    print("Error: Unable to import Claude API. Make sure claude_api.py is available.")

logger = logging.getLogger('md_to_odt.image_analyzer')

class ImageAnalyzer:
    """Class for analyzing and selecting the best images from matches"""
    
    def __init__(self):
        """Initialize the image analyzer"""
        self.logger = logging.getLogger('md_to_odt.image_analyzer')
    
    def analyze_images(self, matched_images):
        """
        Analyze matched images and select the best ones
        
        Args:
            matched_images: Dictionary mapping references to lists of matched images
            
        Returns:
            Dictionary mapping references to selected images
        """
        selected_images = {}
        
        for reference, matches in matched_images.items():
            # Skip if no matches
            if not matches:
                self.logger.warning(f"No image matches to analyze for {reference}")
                selected_images[reference] = None
                continue
                
            # If only one match, use it directly
            if len(matches) == 1:
                self.logger.info(f"Single match found for {reference}, using it directly")
                selected_images[reference] = matches[0]
                continue
                
            # If multiple matches, analyze with Claude
            self.logger.info(f"Analyzing {len(matches)} matches for {reference} with Claude")
            try:
                best_match = self._select_best_image(matches)
                selected_images[reference] = best_match
                self.logger.info(f"Selected best image for {reference}: {best_match}")
            except Exception as e:
                self.logger.error(f"Error analyzing images with Claude: {str(e)}")
                # Fall back to highest confidence match
                selected_images[reference] = matches[0]
                self.logger.info(f"Falling back to highest confidence match: {matches[0]}")
        
        return selected_images
    
    def _select_best_image(self, matches):
        """
        Select the best image from multiple matches using Claude API
        
        Args:
            matches: List of MatchedImage objects
            
        Returns:
            Selected MatchedImage object
        """
        # If no Claude API, fall back to confidence scores
        if 'generate_with_claude_sonnet' not in globals():
            self.logger.warning("Claude API not available, using confidence scores")
            return matches[0]
        
        reference = matches[0].reference
        
        # Limit to top 4 matches to keep prompt size manageable
        top_matches = matches[:4]
        
        # Prepare images for Claude
        image_data = []
        for i, match in enumerate(top_matches):
            try:
                # Resize image for Claude
                resized_image = self._resize_image_for_claude(match.image_path)
                # Add to image data list
                image_data.append({
                    'index': i,
                    'path': match.image_path,
                    'data': resized_image,
                    'metadata': match.metadata
                })
            except Exception as e:
                self.logger.warning(f"Error preparing image {match.image_path}: {str(e)}")
        
        if not image_data:
            self.logger.warning("No valid images for Claude analysis, using confidence scores")
            return matches[0]
        
        # Create prompt for Claude
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_user_prompt(reference, image_data)
        
        try:
            # Call Claude API
            response = generate_with_claude_sonnet(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.3
            )
            
            # Parse response
            selected_index, modified_caption = self._parse_claude_response(response)
            
            # Select the corresponding match
            if 0 <= selected_index < len(top_matches):
                selected_match = top_matches[selected_index]
                
                # Update caption if needed
                if modified_caption:
                    self.logger.info(f"Caption modified: {modified_caption}")
                    selected_match.reference.modified_caption = modified_caption
                
                return selected_match
            else:
                self.logger.warning(f"Invalid index from Claude: {selected_index}, falling back to confidence scores")
                return matches[0]
                
        except Exception as e:
            self.logger.error(f"Error in Claude API call: {str(e)}")
            # Fall back to confidence scores
            return matches[0]
    
    def _resize_image_for_claude(self, image_path, max_dimension=800):
        """
        Resize image for Claude API to reduce token usage
        
        Args:
            image_path: Path to the image file
            max_dimension: Maximum dimension (width or height)
            
        Returns:
            Base64-encoded string of the resized image
        """
        try:
            with Image.open(image_path) as img:
                # Calculate new dimensions
                width, height = img.size
                if width > height:
                    if width > max_dimension:
                        new_width = max_dimension
                        new_height = int(height * (max_dimension / width))
                else:
                    if height > max_dimension:
                        new_height = max_dimension
                        new_width = int(width * (max_dimension / height))
                    else:
                        new_width, new_height = width, height
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Convert to JPEG and encode as base64
                buffer = io.BytesIO()
                resized_img.save(buffer, format="JPEG", quality=85)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
                
        except Exception as e:
            self.logger.error(f"Error resizing image {image_path}: {str(e)}")
            raise
    
    def _create_system_prompt(self):
        """
        Create system prompt for Claude API
        
        Returns:
            System prompt string
        """
        return """
        You are a visual analysis expert helping to select the most appropriate image
        for an educational document. You'll be shown multiple images and a caption.
        Your task is to:
        1. Determine which image best matches the provided caption
        2. If needed, suggest a modified caption that better describes the selected image
        3. Explain your choice briefly
        
        Return your answer in JSON format with these keys:
        - selected_image_index: the index (0-based) of the best image
        - modified_caption: updated caption if needed
        - explanation: brief explanation of your choice
        """
    
    def _create_user_prompt(self, reference, image_data):
        """
        Create user prompt for Claude API
        
        Args:
            reference: ImageReference object
            image_data: List of dictionaries with image data
            
        Returns:
            User prompt string
        """
        prompt = f"""
        Caption: "{reference.description}"
        
        Figure Number: {reference.figure_number or "None"}
        
        Please analyze the following images and select the best match for this caption.
        If necessary, suggest a modified caption that better describes your selected image.
        
        """
        
        # Add images
        for i, img in enumerate(image_data):
            prompt += f"\nImage {i}:\n"
            prompt += f"![Image {i}](data:image/jpeg;base64,{img['data']})\n"
        
        prompt += """
        Return your response in JSON format with these keys:
        - selected_image_index: the index (0-based) of the best image
        - modified_caption: updated caption if needed (or null if no changes needed)
        - explanation: brief explanation of your choice
        """
        
        return prompt
    
    def _parse_claude_response(self, response):
        """
        Parse Claude API response
        
        Args:
            response: Response string from Claude API
            
        Returns:
            Tuple of (selected_index, modified_caption)
        """
        # Extract JSON from response (might be embedded in markdown)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response
            
        try:
            # Parse JSON
            result = json.loads(json_str)
            
            # Extract selected image index
            selected_index = result.get('selected_image_index', 0)
            
            # Extract modified caption if available
            modified_caption = result.get('modified_caption')
            
            # Log explanation if available
            if 'explanation' in result:
                self.logger.info(f"Claude explanation: {result['explanation']}")
            
            return selected_index, modified_caption
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing Claude response: {str(e)}")
            self.logger.debug(f"Raw response: {response}")
            # Return defaults
            return 0, None

# Make sure module has access to regex
import re