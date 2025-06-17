"""
Image Matcher Module

This module handles finding and matching images based on metadata
extracted from image EXIF data, and selecting the best image when
multiple matches exist using Claude API.
"""

import os
import re
import piexif
import json
import logging
import base64
import io
import sys
from PIL import Image

# Import Claude API from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from claude_api import generate_with_claude_sonnet
except ImportError:
    print("Error: Unable to import Claude API. Make sure claude_api.py is available.")

logger = logging.getLogger('md_to_odt.image_matcher')

class MatchedImage:
    """Class representing a matched image for a reference"""
    
    def __init__(self, image_path, reference, metadata=None, confidence=0):
        """
        Initialize a matched image
        
        Args:
            image_path: Path to the image file
            reference: The ImageReference this image matches
            metadata: Optional extracted metadata from the image
            confidence: Optional confidence score for the match (0-100)
        """
        self.image_path = image_path
        self.reference = reference
        self.metadata = metadata or {}
        self.confidence = confidence
    
    def __str__(self):
        """String representation of the matched image"""
        return f"MatchedImage(path={os.path.basename(self.image_path)}, confidence={self.confidence})"

class ImageMatcher:
    """Class for finding and matching images to references"""
    
    def __init__(self):
        """Initialize the image matcher"""
        self.logger = logging.getLogger('md_to_odt.image_matcher')
        # Flag to enable/disable Claude API calls
        self.use_claude_api = True  # Enabled by default
        # Maximum number of images to consider for Claude API
        self.max_claude_images = 2  # Reduced to 2 images max to save tokens
        # Minimum confidence threshold for matching images
        self.min_confidence_threshold = 20.0  # Increased to only consider higher confidence matches
    
    def match_images(self, references, base_directory):
        """
        Find and match images for references
        
        Args:
            references: List of ImageReference objects
            base_directory: Base directory to search for images
            
        Returns:
            Dictionary mapping references to selected images (not lists)
        """
        self.logger.info(f"Matching images for {len(references)} references in {base_directory}")
        
        # Dictionary to store final selected images
        selected_images = {}
        
        # Get list of image files in the directory
        image_files = self._find_image_files(base_directory)
        self.logger.info(f"Found {len(image_files)} potential image files")
        
        # Extract metadata from images
        images_with_metadata = self._extract_metadata(image_files)
        self.logger.info(f"Extracted metadata from {len(images_with_metadata)} images")
        
        # Match images to references
        for reference in references:
            # Find matches for this reference
            matches = self._find_matches_for_reference(reference, images_with_metadata)
            
            if not matches:
                self.logger.warning(f"No matches found for {reference}")
                selected_images[reference] = None
                continue
                
            # If only one match found, use it directly
            if len(matches) == 1:
                self.logger.info(f"Single match found for {reference}, using it directly")
                selected_images[reference] = matches[0]
                continue
                
            # Limit the number of matches to consider for Claude API
            top_matches = matches[:self.max_claude_images]
            self.logger.info(f"Limited to top {len(top_matches)} matches for {reference}")
                
            # If multiple matches and Claude API is enabled, use it
            if len(top_matches) > 1 and self.use_claude_api:
                self.logger.info(f"Analyzing {len(top_matches)} matches for {reference} with Claude")
                try:
                    best_match = self._select_best_image_with_claude(top_matches)
                    selected_images[reference] = best_match
                    self.logger.info(f"Selected best image for {reference}: {best_match}")
                    continue
                except Exception as e:
                    self.logger.error(f"Error analyzing images with Claude: {str(e)}")
                    # Fall through to confidence-based selection below
            
            # Use confidence score-based selection as fallback
            self.logger.info(f"Using confidence scores to select best match for {reference}")
            selected_images[reference] = matches[0]  # Matches are already sorted by confidence
            self.logger.info(f"Selected best image for {reference}: {matches[0]}")
        
        return selected_images
    
    def _find_image_files(self, directory):
        """
        Find all image files in the directory
        
        Args:
            directory: Directory to search
            
        Returns:
            List of paths to image files
        """
        image_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if self._is_image_file(file):
                    image_files.append(os.path.join(root, file))
        
        return image_files
    
    def _is_image_file(self, filename):
        """
        Check if a file is an image based on extension
        
        Args:
            filename: Filename to check
            
        Returns:
            Boolean indicating if file is an image
        """
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        return any(filename.lower().endswith(ext) for ext in image_extensions)
    
    def _extract_metadata(self, image_files):
        """
        Extract metadata from image files
        
        Args:
            image_files: List of paths to image files
            
        Returns:
            List of tuples (image_path, metadata)
        """
        images_with_metadata = []
        
        for image_path in image_files:
            try:
                metadata = self._extract_image_metadata(image_path)
                images_with_metadata.append((image_path, metadata))
            except Exception as e:
                self.logger.warning(f"Error extracting metadata from {image_path}: {str(e)}")
        
        return images_with_metadata
    
    def _extract_image_metadata(self, image_path):
        """
        Extract metadata from an image file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing extracted metadata
        """
        metadata = {}
        
        try:
            # Open image with PIL
            with Image.open(image_path) as img:
                # Check if image has EXIF data
                if hasattr(img, '_getexif') and img._getexif():
                    exif_dict = piexif.load(img.info.get('exif', b''))
                    
                    # Look for metadata in UserComment field
                    if piexif.ExifIFD.UserComment in exif_dict['Exif']:
                        user_comment = exif_dict['Exif'][piexif.ExifIFD.UserComment]
                        
                        # Try to decode as JSON
                        try:
                            if isinstance(user_comment, bytes):
                                metadata = json.loads(user_comment.decode('utf-8', errors='ignore'))
                            else:
                                metadata = json.loads(user_comment)
                        except json.JSONDecodeError:
                            self.logger.debug(f"Could not decode UserComment as JSON in {image_path}")
                    
                    # Extract standard EXIF fields
                    if piexif.ImageIFD.Artist in exif_dict['0th']:
                        artist = exif_dict['0th'][piexif.ImageIFD.Artist]
                        if isinstance(artist, bytes):
                            metadata['photographer'] = artist.decode('utf-8', errors='ignore')
                    
                    if piexif.ImageIFD.DateTime in exif_dict['0th']:
                        datetime = exif_dict['0th'][piexif.ImageIFD.DateTime]
                        if isinstance(datetime, bytes):
                            date_str = datetime.decode('utf-8', errors='ignore')
                            if date_str:
                                metadata['year'] = date_str.split(':')[0]
                    
                    if piexif.ImageIFD.ImageDescription in exif_dict['0th']:
                        description = exif_dict['0th'][piexif.ImageIFD.ImageDescription]
                        if isinstance(description, bytes):
                            metadata['description'] = description.decode('utf-8', errors='ignore')
                
                # Add basic image info
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['format'] = img.format
                
                # Try to extract figure info from filename
                filename = os.path.basename(image_path)
                if 'figure_number' not in metadata:
                    fig_match = re.search(r'fig(\d+)', filename, re.IGNORECASE)
                    if fig_match:
                        metadata['figure_number'] = f"Fig {fig_match.group(1)}"
                
                # Try to extract lesson and step from path or filename
                if 'lesson_number' not in metadata:
                    lesson_match = re.search(r'lesson\s*(\d+)', image_path, re.IGNORECASE)
                    if lesson_match:
                        metadata['lesson_number'] = lesson_match.group(1)
                
                if 'step_number' not in metadata:
                    step_match = re.search(r'step\s*(\d+)', image_path, re.IGNORECASE)
                    if step_match:
                        metadata['step_number'] = step_match.group(1)
        
        except Exception as e:
            self.logger.warning(f"Error processing metadata for {image_path}: {str(e)}")
        
        return metadata
    
    def _find_matches_for_reference(self, reference, images_with_metadata):
        """
        Find matching images for a reference
        
        Args:
            reference: ImageReference object
            images_with_metadata: List of tuples (image_path, metadata)
            
        Returns:
            List of MatchedImage objects
        """
        matches = []
        
        # Get figure number if available
        figure_number = reference.figure_number
        figure_number_normalized = self._normalize_figure_number(figure_number) if figure_number else ""
        
        for image_path, metadata in images_with_metadata:
            confidence = 0
            
            # For exact figure number matches, assign very high confidence
            if figure_number and 'figure_number' in metadata:
                metadata_fig_num = self._normalize_figure_number(metadata['figure_number'])
                if metadata_fig_num == figure_number_normalized:
                    confidence = 90.0  # High confidence for exact figure match
            
            # Check if description contains keywords from image metadata
            if 'description' in metadata and reference.description:
                desc_similarity = self._calculate_text_similarity(
                    metadata['description'], 
                    reference.description
                )
                # Only add description similarity if significant
                if desc_similarity > 0.1:  # Minimum threshold for description similarity
                    confidence += desc_similarity * 20
            
            # Check for lesson/step match
            if 'lesson_number' in metadata and 'step_number' in metadata:
                # Extract lesson/step from reference path if possible
                ref_lesson_match = re.search(r'lesson\s*(\d+)', str(reference), re.IGNORECASE)
                ref_step_match = re.search(r'step\s*(\d+)', str(reference), re.IGNORECASE)
                
                if ref_lesson_match and metadata['lesson_number'] == ref_lesson_match.group(1):
                    confidence += 5.0  # Bonus for lesson match
                
                if ref_step_match and metadata['step_number'] == ref_step_match.group(1):
                    confidence += 10.0  # Bonus for step match
            
            # Only include matches with confidence above the threshold
            if confidence >= self.min_confidence_threshold:
                match = MatchedImage(
                    image_path=image_path,
                    reference=reference,
                    metadata=metadata,
                    confidence=confidence
                )
                matches.append(match)
        
        # Sort matches by confidence (highest first)
        matches.sort(key=lambda m: m.confidence, reverse=True)
        
        # Limit number of matches
        return matches[:5]  # Return at most 5 matches
    
    def _normalize_figure_number(self, fig_num):
        """
        Normalize figure number for comparison
        
        Args:
            fig_num: Figure number string
            
        Returns:
            Normalized figure number string
        """
        if not fig_num:
            return ""
        
        # Extract digits and normalize format to "Fig X"
        match = re.search(r'(\d+)', fig_num)
        if match:
            return f"Fig {match.group(1)}"
        
        return fig_num
    
    def _calculate_text_similarity(self, text1, text2):
        """
        Calculate similarity between two text strings (simple version)
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0
            
        # Convert to lowercase and split into words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Calculate intersection and union
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        # Jaccard similarity
        if union:
            return len(intersection) / len(union)
        
        return 0
        
    def _select_best_image_with_claude(self, matches):
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
        
        # Prepare images for Claude
        image_data = []
        for i, match in enumerate(matches):
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
        
        # Log token estimate
        prompt_size = self._estimate_prompt_size(user_prompt)
        self.logger.info(f"Estimated prompt size: {prompt_size} tokens")
        
        try:
            # Call Claude API
            response = generate_with_claude_sonnet(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=500,  # Reduced to save tokens
                temperature=0.2   # Reduced to make responses more consistent
            )
            
            if not response or response.strip() == "":
                raise ValueError("Empty response from Claude API")
                
            # Parse response
            selected_index, modified_caption = self._parse_claude_response(response)
            
            # Select the corresponding match
            if 0 <= selected_index < len(matches):
                selected_match = matches[selected_index]
                
                # Update caption if needed
                if modified_caption:
                    self.logger.info(f"Caption modified by Claude: {modified_caption}")
                    selected_match.reference.modified_caption = modified_caption
                
                return selected_match
            else:
                self.logger.warning(f"Invalid index from Claude: {selected_index}, falling back to confidence scores")
                return matches[0]
                
        except Exception as e:
            self.logger.error(f"Error in Claude API call: {str(e)}")
            # Fall back to confidence scores
            return matches[0]
    
    def _estimate_prompt_size(self, prompt):
        """Estimate token size of prompt"""
        # Very rough estimate: 1 token ≈ 4 characters for English text
        text_tokens = len(prompt) / 4
        
        # Count base64 images (they're huge)
        base64_images = prompt.count("data:image/jpeg;base64,")
        
        # Find average base64 length
        base64_lengths = []
        for match in re.finditer(r'data:image/jpeg;base64,([^)]+)', prompt):
            base64_lengths.append(len(match.group(1)))
        
        image_tokens = 0
        if base64_lengths:
            avg_length = sum(base64_lengths) / len(base64_lengths)
            # Very rough estimate: 1 token ≈ 3 base64 characters for binary data
            image_tokens = sum(base64_lengths) / 3
        
        return int(text_tokens + image_tokens)
            
    def _resize_image_for_claude(self, image_path, max_dimension=400):
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
                        new_width, new_height = width, height
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
                resized_img.save(buffer, format="JPEG", quality=50)  # Reduced quality to save tokens
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
        You're selecting the best image match for a caption and providing a properly formatted caption. 
        Be concise.
        
        IMPORTANT: Format captions exactly like: 
        Fig.X (Photographer on Pexels, N.d) Brief descriptive caption
        
        Return JSON with:
        - selected_image_index: (0-based) index of best image
        - modified_caption: formatted caption
        - explanation: brief reason for selection (1-2 sentences)
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
        # Keep prompt minimal to reduce tokens
        prompt = f"""Caption: "{reference.description.strip()[:200]}..."
Figure: {reference.figure_number or "None"}
        
Analysis task: Select best matching image and provide caption in format:
Fig.X (Photographer on Pexels, N.d) Brief descriptive caption.

Metadata:"""
        
        # Add minimal metadata
        for i, img in enumerate(image_data):
            metadata = img['metadata']
            photographer = metadata.get('photographer', 'Unknown')
            prompt += f"\nImage {i}: Photographer={photographer}"
        
        # Add images with minimal text
        for i, img in enumerate(image_data):
            prompt += f"\n\nImage {i}:\n![Image {i}](data:image/jpeg;base64,{img['data']})"
        
        # Very concise instructions
        prompt += """

Return JSON with:
- selected_image_index: best image's index
- modified_caption: formatted caption
- explanation: brief reason (1-2 sentences)"""
        
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