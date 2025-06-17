"""
Extended Claude API Client with support for Claude 3.7 and extended thinking

This module extends the base Claude API functionality to support:
1. Claude 3.7 model
2. Extended thinking capability
3. Streaming responses for real-time updates
"""

import os
import json
import logging
import time
import requests
from typing import Dict, Any, Optional, Callable

# Set up logging
logger = logging.getLogger("claude_api_ext")

class ClaudeExtendedClient:
    """
    Client for interacting with Claude 3.7 with extended thinking capability
    """
    
    def __init__(self):
        """Initialize the Claude extended client"""
        self.api_key = self._get_api_key()
        self.model = "claude-3-7-sonnet-20250219"
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables or .env file"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if api_key:
            logger.info("Using ANTHROPIC_API_KEY from environment variables")
            return api_key
            
        try:
            # Try to load from .env file
            from dotenv import load_dotenv
            dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
            load_dotenv(dotenv_path)
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                logger.info("Using ANTHROPIC_API_KEY from .env file")
                return api_key
        except ImportError:
            logger.warning("Could not import dotenv, falling back to config")
        except Exception as e:
            logger.warning(f"Error loading from .env: {str(e)}")
        
        logger.error("ANTHROPIC_API_KEY not found in environment or .env file")
        return None

    def check_api_key(self) -> bool:
        """Check if the API key is available"""
        return self.api_key is not None

    def call_with_extended_thinking(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        thinking_budget: int = 8192,  
        max_tokens: int = 9000, 
        temperature: float = 1.0,
        stream: bool = False,
        stream_callback: Optional[Callable[[str, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Call Claude API with extended thinking capability
        
        Args:
            prompt (str): The user prompt
            system_prompt (str): Optional system prompt
            thinking_budget (int): Token budget for extended thinking (minimum 1024)
            max_tokens (int): Maximum tokens in the response
            temperature (float): Must be 1.0 when thinking is enabled
            stream (bool): Whether to stream the response
            stream_callback (Callable): Callback function for streaming updates
                                       Args: content_type (str), content (str)
                                       
        Returns:
            Dict[str, Any]: Response containing thinking and text content
        """
        if not self.api_key:
            error_msg = "ANTHROPIC_API_KEY not configured. Please add it to .env file."
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Enforce temperature 1.0 for extended thinking as per API requirements
        temperature = 1.0
        
        # Ensure thinking budget is at least the minimum (1024 tokens)
        thinking_budget = max(1024, thinking_budget)
        
        # Ensure max_tokens is greater than thinking_budget
        max_tokens = max(thinking_budget + 1000, max_tokens)
        
        # Warn if thinking budget is over 32K as per documentation
        if thinking_budget > 32000:
            logger.warning("Thinking budget over 32K tokens may cause timeouts or connection issues")
        
        # Prepare headers with API key
        headers = {
            "x-api-key": self.api_key,
            **self.headers
        }
        
        # Prepare the request data
        data = {
            "model": self.model,
            "max_tokens": max_tokens,
            "thinking": {
                "type": "enabled",
                "budget_tokens": thinking_budget
            },
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "stream": stream
        }
        
        # Add system prompt if provided
        if system_prompt:
            data["system"] = system_prompt
        
        # Save API request to file for debugging
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"claude_ext_request_{timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Create a safe version without API key
                safe_data = data.copy()
                json.dump(safe_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved API request to {filename}")
        except Exception as e:
            logger.error(f"Error saving API request: {str(e)}")
        
        # Log API call
        logger.info(f"Calling Claude 3.7 with extended thinking: tokens={thinking_budget}")
        
        api_start_time = time.time()
        
        try:
            if stream:
                return self._stream_response(headers, data, stream_callback)
            else:
                return self._send_request(headers, data)
        except Exception as e:
            error_msg = f"Error calling Claude API: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def _send_request(self, headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a non-streaming request to the Claude API"""
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=300  # Extended timeout for long thinking
        )
        
        if not response.ok:
            error_msg = f"Claude API error: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Process and return the response
        result = response.json()
        
        # Extract thinking and text blocks
        thinking_blocks = []
        text_blocks = []
        
        if "content" in result:
            for item in result["content"]:
                if item.get("type") == "thinking":
                    thinking_blocks.append(item.get("thinking", ""))
                elif item.get("type") == "text":
                    text_blocks.append(item.get("text", ""))
        
        return {
            "thinking": "\n".join(thinking_blocks),
            "text": "\n".join(text_blocks),
            "raw_response": result
        }
    
    def _stream_response(
        self, 
        headers: Dict[str, str], 
        data: Dict[str, Any],
        callback: Optional[Callable[[str, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Stream response from Claude API
        
        Args:
            headers: Request headers
            data: Request data
            callback: Function to call with each chunk of content
                     Args: content_type (str), content (str)
        
        Returns:
            Dict with aggregated response
        """
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            stream=True,
            timeout=300
        )
        
        if not response.ok:
            error_msg = f"Claude API streaming error: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Track content by block index and type
        thinking_blocks = []
        text_blocks = []
        current_thinking = ""
        current_text = ""
        
        # Track if we're currently in a thinking or text block
        current_block_type = None
        current_block_index = None
        
        for line in response.iter_lines():
            if not line:
                continue
            
            try:
                # Strip "data: " prefix
                if line.startswith(b"data: "):
                    line = line[6:]
                
                # Skip "event: " lines and empty lines
                if not line or line.startswith(b"event: "):
                    continue
                
                # Parse the JSON data
                data = json.loads(line)
                event_type = data.get("type", "")
                
                # Handle different event types
                if event_type == "content_block_start":
                    block = data.get("content_block", {})
                    block_type = block.get("type")
                    block_index = data.get("index")
                    
                    current_block_type = block_type
                    current_block_index = block_index
                    
                    # Initialize block content if needed
                    if block_type == "thinking":
                        if len(thinking_blocks) <= block_index:
                            thinking_blocks.extend([""] * (block_index - len(thinking_blocks) + 1))
                        current_thinking = thinking_blocks[block_index]
                    elif block_type == "text":
                        if len(text_blocks) <= block_index:
                            text_blocks.extend([""] * (block_index - len(text_blocks) + 1))
                        current_text = text_blocks[block_index]
                
                elif event_type == "content_block_delta":
                    delta = data.get("delta", {})
                    delta_type = delta.get("type", "")
                    
                    if delta_type == "thinking_delta":
                        thinking_content = delta.get("thinking", "")
                        current_thinking += thinking_content
                        if current_block_index is not None:
                            thinking_blocks[current_block_index] = current_thinking
                        
                        # Call callback if provided
                        if callback:
                            callback("thinking", thinking_content)
                    
                    elif delta_type == "text_delta":
                        text_content = delta.get("text", "")
                        current_text += text_content
                        if current_block_index is not None:
                            text_blocks[current_block_index] = current_text
                        
                        # Call callback if provided
                        if callback:
                            callback("text", text_content)
                
                elif event_type == "content_block_stop":
                    # Reset current block tracking
                    current_block_type = None
                    current_block_index = None
                    current_thinking = ""
                    current_text = ""
                
                elif event_type == "message_stop":
                    # Streaming is complete
                    break
                
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse streaming response line: {line}")
            except Exception as e:
                logger.error(f"Error processing streaming response: {str(e)}")
        
        # Return the aggregated response
        return {
            "thinking": "\n".join(thinking_blocks),
            "text": "\n".join(text_blocks)
        }