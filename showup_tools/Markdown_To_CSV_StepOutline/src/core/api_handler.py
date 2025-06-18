#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""API handler for AI integration."""

import logging
from typing import Optional

# API library imports
try:
    import anthropic
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

logger = logging.getLogger("APIHandler")


class APIHandler:
    """Handles AI API requests for content enhancement.
    
    This class provides an interface to AI services for enhancing 
    educational content during the Markdown to CSV conversion process.
    """
    
    @classmethod
    def is_available_class(cls) -> bool:
        """Class method to check if AI integration is available in the environment.
        
        Returns:
            bool: True if AI integration is available, False otherwise
        """
        return AI_AVAILABLE
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the API handler.
        
        Args:
            api_key: API key for authentication with the AI service
        """
        self.client = None
        self.max_retries = 3
        
        if api_key and AI_AVAILABLE:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
                logger.info("AI integration initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize AI client: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the AI client is available.
        
        Returns:
            bool: True if the client is initialized and ready, False otherwise
        """
        return self.client is not None
    
    def make_api_request(self, prompt: str, attempt: int = 0) -> Optional[str]:
        """Make a single API request with proper error handling.
        
        Args:
            prompt: The prompt to send to the AI service
            attempt: Current attempt number for retry handling
            
        Returns:
            Optional[str]: The response text if successful, None otherwise
        """
        if not self.client:
            return None
            
        try:
            logger.info(f"Sending API request (attempt {attempt + 1})...")
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                temperature=0.1,  # Low temperature for more consistent results
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            if hasattr(response, 'content'):
                if isinstance(response.content, list):
                    content = response.content[0]
                    if hasattr(content, 'text'):
                        text = content.text
                        if text.strip():
                            return text
            
            raise ValueError("Could not extract valid text from response")
            
        except Exception as e:
            logger.warning(f"API request error (attempt {attempt + 1}): {str(e)}")
            if attempt < self.max_retries - 1:
                return self.make_api_request(prompt, attempt + 1)
            return None
    
    def classify_step_type(self, step_content: str) -> str:
        """Use AI to classify step type if standard rules are ambiguous.
        
        Args:
            step_content: The content of the educational step to classify
            
        Returns:
            str: The classified step type ('Content', 'Activity', 'Assessment', or 'Quiz')
        """
        prompt = f"""Classify this educational step into exactly ONE of these categories:
- Content: explanatory material that teaches concepts or presents information
- Activity: exercise requiring direct learner participation or creation
- Assessment: non-question evaluation that measures understanding
- Quiz: question-and-answer format for knowledge testing

Educational step:
{step_content}

Return ONLY the category name, with no additional text."""
        
        response = self.make_api_request(prompt)
        if response:
            response = response.strip()
            # Normalize the response
            if "content" in response.lower():
                return "Content"
            elif "activity" in response.lower():
                return "Activity"
            elif "assessment" in response.lower():
                return "Assessment"
            elif "quiz" in response.lower():
                return "Quiz"
        
        # Default fallback
        return "Content"
    
    def generate_rationale(self, step_title: str, step_content: str, 
                           module_title: str = "", lesson_title: str = "") -> str:
        """Generate a rationale when none is explicitly provided in the markdown.
        
        Args:
            step_title: Title of the educational step
            step_content: Content of the educational step
            module_title: Title of the parent module (optional)
            lesson_title: Title of the parent lesson (optional)
            
        Returns:
            str: Generated rationale text
        """
        # Truncate very long content to prevent token overflow
        if len(step_content) > 8000:
            step_content = step_content[:4000] + "\n...[content truncated]...\n" + step_content[-4000:]
            
        prompt = f"""Write a concise educational rationale (2-3 sentences) that explains the pedagogical value of this step.

CONTEXT:
Module: {module_title}
Lesson: {lesson_title}
Step: {step_title}

CONTENT:
{step_content}

The rationale must:
1. Identify specific learning outcomes this step supports
2. Connect to broader educational objectives
3. Use professional language suitable for instructor documentation

Return ONLY the rationale text with no additional formatting."""
        
        response = self.make_api_request(prompt)
        if response:
            return response.strip()
        
        # Default fallback
        return f"Understanding {step_title} is important for mastering this subject matter."
    
    def generate_content_outline(self, step_content: str) -> str:
        """Generate a bullet-point content outline from step content when not explicitly formatted.
        
        Args:
            step_content: The content of the educational step
            
        Returns:
            str: Generated bullet-point outline
        """
        # Truncate very long content to prevent token overflow
        if len(step_content) > 8000:
            step_content = step_content[:4000] + "\n...[content truncated]...\n" + step_content[-4000:]
            
        prompt = f"""Create 3-5 bullet points that summarize the key content from this educational step.

CONTENT:
{step_content}

FORMAT REQUIREMENTS:
- Each point must start with a dash (-)
- Each point must be 8-15 words
- Use parallel grammatical structure (e.g., all starting with verbs or all noun phrases)
- Cover distinct concepts without overlap
- Collectively capture the most important elements

Return ONLY the bullet points, with each on a separate line."""
        
        response = self.make_api_request(prompt)
        if response:
            # Clean up the response
            outline = response.strip()
            # Ensure each line starts with a dash
            lines = outline.split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('-'):
                    line = f"- {line}"
                if line:
                    formatted_lines.append(line)
            return '\n'.join(formatted_lines)
        
        # Default fallback
        return "- Key content in this section"
