from typing import Dict, List, Optional, Any, Tuple
import anthropic
from anthropic.types import ContentBlock
import json
import re

from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_SONNET,
    CLAUDE_HAIKU,
    MAX_THINKING_TOKENS,
    MAX_OUTPUT_TOKENS
)


class ClaudeClient:
    """Handles interactions with Claude API for different models."""
    
    def __init__(self) -> None:
        """Initialize the Claude client with API key."""
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    def get_document_summary(self, document_text: str) -> str:
        """Get a summary of a document using the cheaper Claude Haiku model.
        
        Args:
            document_text: The text content of the document to summarize
            
        Returns:
            A concise summary of the document
        """
        prompt = (
            "Please provide a brief but comprehensive summary of the following document. "
            "Focus on key points and main ideas only:\n\n"
            f"{document_text}"
        )
        
        message = self.client.messages.create(
            model=CLAUDE_HAIKU,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract text from the response content
        return self._extract_text_from_content(message.content)
    
    def _extract_text_from_content(self, content: List[ContentBlock]) -> str:
        """Extract text from content blocks, handling different block types.
        
        Args:
            content: List of content blocks from Claude API response
            
        Returns:
            Extracted text content
        """
        result = []
        
        for block in content:
            if hasattr(block, 'text') and block.text:  # TextBlock
                result.append(block.text)
            elif hasattr(block, 'type') and block.type == 'text' and hasattr(block, 'text'):  # Dict with text
                result.append(block.text)
            elif isinstance(block, dict) and 'type' in block and block['type'] == 'text' and 'text' in block:
                result.append(block['text'])
        
        return '\n'.join(result)
    
    def _parse_confidence_response(self, response: str) -> Tuple[str, str]:
        """Parse a response that may include confidence information.
        
        Args:
            response: The raw response from Claude API
            
        Returns:
            Tuple of (category, confidence_info)
        """
        # Check for instruction error
        if response.startswith("INSTRUCTION_ERROR:"):
            return "INSTRUCTION_ERROR", response
            
        # Check for new category suggestion format
        new_category_match = re.search(r'NEW_CATEGORY:\s*([\w_]+)\s*\(Rationale:', response)
        if new_category_match:
            category = new_category_match.group(1)
            return category, response
            
        # Check for review required format
        if 'REVIEW_REQUIRED:' in response:
            return "REVIEW_REQUIRED", response
            
        # Check for medium confidence format
        medium_match = re.search(r'Category:\s*([\w_]+)\s*\(Consider alternatives:', response)
        if medium_match:
            category = medium_match.group(1)
            return category, response
            
        # Check for low confidence format
        low_match = re.search(r'Suggested Category:\s*([\w_]+)\s*\(Requires confirmation\)', response)
        if low_match:
            category = low_match.group(1)
            return category, response
            
        # High confidence - just the category name
        # Clean up any extra text or whitespace
        category = response.strip()
        
        # If there are multiple lines, take just the first one
        if '\n' in category:
            category = category.split('\n')[0].strip()
            
        return category, ""
    
    def get_organization_decision(self, 
                                 file_info: Dict[str, Any], 
                                 document_summary: Optional[str] = None,
                                 available_categories: List[str] = None,
                                 special_tags: List[str] = None,
                                 force_medium_confidence: bool = False) -> str:
        """Use Claude Sonnet to decide where to file a document.
        
        Args:
            file_info: Dictionary with file metadata (name, extension, size, etc.)
            document_summary: Optional summary of document content
            available_categories: List of available folder categories
            special_tags: Optional list of special handling tags
            force_medium_confidence: If True, forces medium confidence format for cold start
            
        Returns:
            The category where the file should be placed
        """
        # Initialize special tags if not provided
        special_tags = special_tags or []
        
        # Prepare file info as a string
        file_info_str = json.dumps(file_info, indent=2)
        
        # Create categories as string
        categories_str = "\n".join([f"- {cat}" for cat in available_categories]) if available_categories else "No predefined categories"
        
        # Create content blocks
        content = [
            {"type": "text", "text": (
                "# FILE CATEGORIZATION TASK\n\n"
                "## DECISION FRAMEWORK\n"
                "When categorizing files, apply this prioritized decision framework:\n"
                "1. Content relevance (highest priority): Evaluate the document's primary subject matter\n"
                "2. User-defined tags or metadata (if available)\n"
                "3. File type and format characteristics\n"
                "4. Creation date and temporal relevance\n"
                "5. Previously established patterns from user history\n\n"
                
                "## CONFIDENCE ASSESSMENT CRITERIA\n"
                "Use these specific indicators to assess confidence levels:\n"
                "- High confidence (>90%): Clear content match with category purpose OR explicit user tagging\n"
                "- Medium confidence (70-90%): Partial content match OR matching file type typically used for this category\n"
                "- Low confidence (<70%): Weak but relevant content signals OR matching only by format convention\n"
                "- New category (<50%): Content clearly falls outside all available categories\n\n"
                
                "## MULTI-CATEGORY HANDLING\n"
                "For files with equal relevance to multiple categories (within 10% confidence):\n"
                "1. Primary factor: User has previously established a preference pattern for similar files\n"
                "2. Secondary factor: The most specific applicable category\n"
                "3. If truly equal, select the category that appears first alphabetically\n\n"
                
                "## SPECIAL FILE HANDLING\n"
                "- For version-controlled files (containing v1, v2, etc.): Prioritize matching with the most recent version's category\n"
                "- For confidential/sensitive materials (marked as such in metadata or content): Add \"CONFIDENTIAL:\" prefix to any response format\n"
                "- For time-sensitive files (containing terms like \"urgent\", \"immediate\", etc.): Add \"PRIORITY:\" prefix to any response format\n\n"
                
                "## RESPONSE FORMAT\n"
                "- High confidence (>90%): Respond with only the category name\n"
                "- Medium confidence (70-90%): Respond with \"Category: [name] (Consider alternatives: [alt1], [alt2])\"\n"
                "- Low confidence (<70%): Respond with \"Suggested Category: [name] (Requires confirmation)\"\n"
                "- New category (<50%): Respond with \"NEW_CATEGORY: [suggested name] (Rationale: brief explanation)\"\n"
                "- Unreadable files: Respond with \"REVIEW_REQUIRED: (Reason: [brief explanation])\"\n\n"
                
                "## VERIFICATION\n"
                "If any portion of this instruction is unclear or cannot be followed, respond with \"INSTRUCTION_ERROR: [specific issue]\" instead of attempting to categorize.\n\n"
                
                "## FILE INFORMATION\n"
                f"{file_info_str}\n\n"
                
                "## AVAILABLE CATEGORIES\n"
                f"{categories_str}\n\n"
            )}
        ]
        
        # Add document summary if available
        if document_summary:
            content.append({"type": "text", "text": f"## DOCUMENT SUMMARY\n{document_summary}\n\n"})
        
        # Add special tags information if any present
        if special_tags:
            tags_str = ", ".join(special_tags)
            content.append({"type": "text", "text": f"## SPECIAL TAGS\nThis file has been identified with the following special characteristics: {tags_str}\n\n"})
            
        # Add final instruction with cold start guidance if needed
        if force_medium_confidence:
            content.append({"type": "text", "text": (
                "Based on the above information, determine the most appropriate category for this file. \n"
                "As this is an early categorization with limited user feedback, please respond in the medium confidence format: \n"
                "\"Category: [name] (Consider alternatives: [alt1], [alt2])\""
            )})
        else:
            content.append({"type": "text", "text": (
                "Based on the above information, determine the most appropriate category for this file. "
                "Apply the decision framework and format your response according to your confidence level."
            )})
        
        # Create API call parameters
        kwargs = {
            "model": CLAUDE_SONNET,
            "max_tokens": MAX_OUTPUT_TOKENS,
            "messages": [
                {"role": "user", "content": content}
            ],
            "temperature": 1.0,
            "system": "You are a precision file categorization system. Your only purpose is to determine the single most appropriate category for files based on the information provided. Maintain strict adherence to the confidence-based response formats specified in the user prompt."
        }
        
        # Add thinking parameter only for models that support it (Claude 3.7)
        if "claude-3-7" in CLAUDE_SONNET:  
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": MAX_THINKING_TOKENS}
            
        message = self.client.messages.create(**kwargs)
        
        # Extract text from the response content
        full_response = self._extract_text_from_content(message.content).strip()
        
        # Add prefixes for special tags if not already present
        if "confidential" in special_tags and not full_response.startswith("CONFIDENTIAL:"):
            full_response = f"CONFIDENTIAL: {full_response}"
            
        if "priority" in special_tags and not full_response.startswith("PRIORITY:") and not full_response.startswith("CONFIDENTIAL:"):
            full_response = f"PRIORITY: {full_response}"
        elif "priority" in special_tags and full_response.startswith("CONFIDENTIAL:") and "PRIORITY:" not in full_response:
            full_response = full_response.replace("CONFIDENTIAL:", "CONFIDENTIAL: PRIORITY:")
        
        # Parse the response to extract category and confidence info
        category, confidence_info = self._parse_confidence_response(full_response)
        
        # Return full response if it contains confidence information, otherwise just the category
        return full_response if confidence_info else category
    
    def chat(self, user_message: str, chat_history: List[Dict[str, str]] = None, system_message: str = None) -> str:
        """Handle a general chat message from the user.
        
        Args:
            user_message: The user's message
            chat_history: Optional list of previous messages
            system_message: Optional system message to provide context to Claude
            
        Returns:
            Claude's response to the user
        """
        messages = chat_history or []
        messages.append({"role": "user", "content": user_message})
        
        # Create API call with system message if provided
        kwargs = {
            "model": CLAUDE_SONNET,
            "max_tokens": MAX_OUTPUT_TOKENS,
            "messages": messages,
            "temperature": 1.0
        }
        
        # Add system message if provided
        if system_message:
            kwargs["system"] = system_message
            
        # Add thinking parameter only for models that support it (Claude 3.7)
        if "claude-3-7" in CLAUDE_SONNET:  
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": MAX_THINKING_TOKENS}
            
        response = self.client.messages.create(**kwargs)
        
        # Extract text from the response content
        return self._extract_text_from_content(response.content)
