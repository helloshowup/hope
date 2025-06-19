"""
Simplified AI API Module for ShowupSquaredV4 Output Library Editor

This module provides direct access to Claude and OpenAI models with minimal dependencies.
It handles API authentication, logging, and basic error handling.
"""
import os
import logging
import json
import requests
import time
try:
    import openai  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    openai = None
import re
from typing import Dict, Any, Optional, Tuple
from functools import wraps

# Define logs directory structure
def get_logs_dir() -> str:
    """Get the centralized logs directory"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base_dir, "logs")
    return logs_dir

def ensure_logs_directory(subdir: str = "") -> str:
    """
    Ensure logs directory structure exists and return path
    
    Args:
        subdir: Optional subdirectory within logs dir
    
    Returns:
        Full path to logs directory or subdirectory
    """
    logs_dir = get_logs_dir()
    
    # Create main logs directory if it doesn't exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # If a subdirectory is specified, create and return it
    if subdir:
        subdir_path = os.path.join(logs_dir, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
        return subdir_path
    
    return logs_dir

# Set up logging
logger = logging.getLogger("ai_api")

# Centralized Claude model configuration
CLAUDE_MODELS = {
    # Production-approved models only
    "CONTEXT_GEN": "claude-3-5-haiku-20241022",     # Fast, efficient for context generation (Haiku 3.5)
    "CONTENT_EDIT": "claude-opus-4-20250514",       # Intelligent for nuanced editing (Claude 4 Opus)
    
    # Cache configuration 
    "CACHE_ENABLED": ["claude-3-5-haiku-20241022", "claude-opus-4-20250514"],
}

# Centralized system prompt templates
CONTEXT_SYSTEM_PROMPT = """
You are an expert educational content analyst specializing in content preparation and enhancement guidance.
Your task is to analyze educational content and create a comprehensive preparatory context
that will guide subsequent content enhancement.

Focus on:
1. Identifying the core purpose and structure of the content
2. Extracting clear objectives from enhancement prompts
3. Adapting content appropriately for the specific target learner
4. Optimizing content for the learning medium specified in the profile
5. Providing strategic guidance for improvement while preserving value

Be concise yet thorough in your analysis. The quality of your preparatory context
directly impacts the effectiveness of subsequent content enhancement.
Generate content that serves as a foundation for further development, not as a final product.

IMPORTANT: Include all learner profile considerations directly in your context. This will be
the only guidance about the target learner available during enhancement.

Pay particular attention to any limitations mentioned in the learner profile related to the learning medium 
(such as asynchronous online learning, in-person classroom, mobile device, etc.), but avoid being
overly prescriptive about formatting or structural changes unless specifically requested.
"""

CONTENT_EDIT_SYSTEM_PROMPT = """
You are a markdown content editor that makes surgical, line-specific edits based on educational principles.
ONLY respond with edit commands - never explanations or commentary.
"""

CONTEXT_USER_PROMPT_TEMPLATE = """
# Analysis Task: Generate Preparatory Context for Enhancement
# Content Type: Educational Material
# Processing Mode: Batch Enhancement

Please analyze the current content, enhancement prompt, and target learner profile to create a comprehensive 
context that will guide content enhancement while:
1. Maintaining educational integrity
2. Addressing the specific needs in the enhancement prompt
3. Preserving the original content's core value
4. Adapting content appropriately for the target learner profile
5. Optimizing for the learning medium (asynchronous online, in-person classroom, etc.)

Your analysis must:
- Identify key themes and concepts in the current content
- Extract specific requirements from the enhancement prompt
- Determine appropriate language level, examples, and complexity based on the learner profile
- Note any limitations or considerations based on the learning medium
- Create a guidance framework for targeted content enhancement
- Suggest potential improvements while preserving original intent

Format your response as a pre-fill instruction that provides a high-level overview 
including:
1. Content Summary: Brief overview of the current content's purpose and structure
2. Enhancement Requirements: Clear objectives derived from the prompt
3. Target Learner Considerations: Specific adaptations needed for the target learner
4. Learning Medium Considerations: Brief note on any limitations imposed by the delivery medium
5. Key Considerations: Important elements to preserve or improve
6. Suggested Approach: Strategic recommendations for enhancement

This preparatory context will be used as guidance for subsequent content enhancement.
Focus on providing clear, actionable direction rather than specific edits.
Include everything relevant from the learner profile directly in this context - the profile information
will not be sent separately during enhancement.

<ENHANCEMENT_PROMPT>
## Enhancement Prompt
{prompt}
</ENHANCEMENT_PROMPT>

<LEARNER_PROFILE>
## Target Learner Profile
{learner_profile}
</LEARNER_PROFILE>

<CONTENT>
## Current Content
{file_content}
</CONTENT>
"""

# Model token limits
MODEL_TOKEN_LIMITS = {
    "claude-3-haiku-20240307": 4096,  # Fixed to match actual limit
    "claude-3-sonnet-20240229": 200000,
    "claude-3-opus-20240229": 200000,
    "claude-3-7-sonnet-20250219": 200000,  # Added Claude 3.7 Sonnet with higher limit
    "claude-3-5-haiku-20241022": 200000,  # Added Claude 3.5 Haiku
    "claude-opus-4-20250514": 200000,  # Added Claude 4 Opus
    "gpt-4": 8192,
    "gpt-4-turbo": 128000
}

def estimate_token_count(text: str) -> int:
    """Estimate tokens using the 4 chars ≈ 1 token heuristic"""
    return len(text) // 4 if text else 0
    
def validate_token_limit(text: str, max_tokens: int) -> Dict[str, Any]:
    """
    Validate that text is within token limit
    
    Args:
        text: Text to validate
        max_tokens: Maximum allowed tokens
        
    Returns:
        Dictionary with validation result:
        {
            "valid": True/False,
            "estimated_tokens": int,
            "max_tokens": int
        }
    """
    estimated_tokens = estimate_token_count(text)
    
    return {
        "valid": estimated_tokens <= max_tokens,
        "estimated_tokens": estimated_tokens,
        "max_tokens": max_tokens
    }

def _call_claude_api(prompt: str, system_prompt: str = "", 
                    model_key: str = "CONTEXT_GEN", max_tokens: int = 4000, 
                    temperature: float = 0.0, task_type: str = "generation",
                    tools: list = None) -> str:
    """
    Central Claude API handler that enforces model policy
    
    This function provides a single point of control for all Claude API calls,
    enforcing model selection policy and providing consistent handling of API calls.
    
    Args:
        prompt: The prompt to send to Claude
        system_prompt: Optional system prompt to include
        model_key: Key from CLAUDE_MODELS dictionary ("CONTEXT_GEN" or "CONTENT_EDIT")
        max_tokens: Maximum tokens in response
        temperature: Temperature for generation
        task_type: Type of task for logging purposes
        tools: Optional tools for Claude API
        
    Returns:
        String response from Claude API
    """
    # Get API instance
    api = get_claude_api()
    
    # Model selection with strict enforcement
    if model_key not in CLAUDE_MODELS:
        logger.warning(f"Attempting to use non-approved model key: {model_key}. Defaulting to CONTEXT_GEN.")
        model_key = "CONTEXT_GEN"
        
    model = CLAUDE_MODELS[model_key]
    
    # Cache logic centralized
    use_cache = model in CLAUDE_MODELS["CACHE_ENABLED"]
    
    # Log API call
    logger.info(f"Calling Claude API with model={model}, task_type={task_type}")
    
    # Track start time
    start_time = time.time()
    
    # Make API call
    try:
        response_text = api.call_api(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            task_type=task_type,
            tools=tools
        )
        
        # Get elapsed time
        elapsed_time = time.time() - start_time
        
        # Validate response
        if response_text and len(response_text) > 10 and "error" not in response_text.lower()[:50]:
            logger.info(f"Claude API call successful: {task_type}, model={model}, time={elapsed_time:.2f}s")
            return response_text
        else:
            logger.warning(f"Claude API returned unexpected response: {response_text[:100]}...")
            return response_text
            
    except Exception as e:
        logger.error(f"Error calling Claude API: {str(e)}")
        raise
        
class BaseAPI:
    """Base class for API clients with common functionality"""
    
    def __init__(self, api_key_name: str, config_key_name: str):
        self.api_key_name = api_key_name
        self.config_key_name = config_key_name
        self.api_key = self._get_api_key()
        
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables or config"""
        api_key = os.getenv(self.api_key_name)
        
        if api_key:
            logger.info(f"Using {self.api_key_name} from environment variables")
            return api_key
            
        try:
            # Try to load from .env file
            from dotenv import load_dotenv
            dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
            load_dotenv(dotenv_path)
            
            api_key = os.getenv(self.api_key_name)
            if api_key:
                logger.info(f"Using {self.api_key_name} from .env file")
                return api_key
        except ImportError:
            logger.warning("Could not import dotenv, falling back to config")
        except Exception as e:
            logger.warning(f"Error loading from .env: {str(e)}")
        
        # If not found in environment, try config file
        try:
            import importlib
            config = importlib.import_module("config.api_keys")
            api_key = getattr(config, self.config_key_name, None)
            
            if api_key:
                logger.info(f"Using {self.api_key_name} from config file")
                return api_key
        except ImportError:
            logger.error(f"Could not import {self.config_key_name} from config.api_keys")
        except Exception as e:
            logger.error(f"Error getting API key from config: {str(e)}")
        
        return None
    
    def _log_api_call(self, model: str, task_type: str) -> None:
        logger.info(f"Calling {self.__class__.__name__}: model={model}, task_type={task_type}")
    
    def _log_api_success(self, task_type: str, start_time: float) -> None:
        end_time = time.time()
        logger.info(f"{self.__class__.__name__} call successful: {task_type}, time={end_time - start_time:.2f}s")
    
    def check_token_limits(self, prompt: str, system_prompt: str, model: str, max_tokens: int) -> Tuple[bool, str]:
        """Check if token count is within limits"""
        estimated_tokens = estimate_token_count(prompt) + estimate_token_count(system_prompt) + max_tokens
        model_limit = MODEL_TOKEN_LIMITS.get(model, 100000)  # Default if model not known
        
        if estimated_tokens > model_limit:
            return False, f"Content likely exceeds token limit: ~{estimated_tokens} tokens (limit: {model_limit})"
        return True, ""

class ClaudeAPI(BaseAPI):
    """API class for Claude API calls"""
    
    def __init__(self):
        super().__init__("ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
    
    def call_api(self, prompt: str, system_prompt: str = "", 
                model: str = CLAUDE_MODELS["CONTEXT_GEN"], max_tokens: int = 4000, temperature: float = 0.7,
                task_type: str = "general", tools=None) -> str:
        
        if not self.api_key:
            return "Error: ANTHROPIC_API_KEY not configured. Please add it to .env or config/api_keys.json"
        
        # Check token limits but don't block execution
        is_within_limits, limit_message = self.check_token_limits(prompt, system_prompt, model, max_tokens)
        if not is_within_limits:
            logger.warning(limit_message)
            # Continue with API call despite token limit warning
        
        # Prepare request
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Determine if the model supports caching
        cache_supported_models = [
            "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022", 
            "claude-3-5-haiku-20241022", "claude-3-haiku-20240307", "claude-3-opus-20240229",
            "claude-opus-4-20250514"
        ]
        
        use_cache = model in cache_supported_models
        cache_minimum_tokens = 1024  # For most models
        
        # Higher threshold for Haiku models
        if "haiku" in model.lower():
            cache_minimum_tokens = 2048
        
        # Tools should be cached when available (first in cache order)
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Add tools if provided (should be first in cache order)
        if tools:
            data["tools"] = tools
            
            # Mark the last tool for caching if we're using a cache-supported model
            # and the tools are substantial enough
            if use_cache and len(str(tools)) > 250:
                # We need to estimate token count of tools
                tools_token_estimate = estimate_token_count(str(tools))
                
                if tools_token_estimate >= cache_minimum_tokens:
                    # Add cache control to the last tool
                    if isinstance(tools, list) and len(tools) > 0:
                        tools[-1]["cache_control"] = {"type": "ephemeral"}
        
        # Prepare messages array
        messages = []
        
        # System message should be next in cache order after tools
        if system_prompt:
            # If system prompt is substantial and we're using a supported model,
            # include it as a message with cache control
            system_tokens = estimate_token_count(system_prompt)
            
            if use_cache and system_tokens >= cache_minimum_tokens and not tools:
                # Include system as a message with cache control
                messages.append({
                    "role": "system",
                    "content": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                })
                system_in_messages = True
            else:
                # Use system as a top-level parameter (traditional way)
                data["system"] = system_prompt
                system_in_messages = False
        else:
            system_in_messages = False
            
        # Add user prompt message (last in cache order)
        messages.append({"role": "user", "content": prompt})
        
        # Add messages to data
        data["messages"] = messages
        
        self._log_api_call(model, task_type)
        
        # Try with input truncation if needed
        if len(prompt) > 100000:  # Arbitrary threshold
            logger.warning(f"Large input detected ({len(prompt)} chars), truncating to 100K chars")
            truncated_prompt = prompt[:100000] + "... [content truncated due to length]"
            # Update the last message (user message) with truncated content
            messages[-1]["content"] = truncated_prompt
        
        # Save API request to file before sending
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        # Create subdirectory for Claude API requests
        api_logs_dir = ensure_logs_directory("claude")
        filename = os.path.join(api_logs_dir, f"request_{timestamp}.json")
        try:
            # Create a copy of data with the API key removed for safety
            safe_data = data.copy()
            # Save to logs directory
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(safe_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved API request to {filename}")
        except Exception as e:
            logger.error(f"Error saving API request: {str(e)}")
        
        # Make API request with model-specific timeout
        api_start_time = time.time()
        response = None
        
        # Set timeout based on model - Claude 4 Opus needs more time for complex content
        if "opus-4" in model.lower():
            timeout_seconds = 300  # 5 minutes for Claude 4 Opus
        elif "opus" in model.lower():
            timeout_seconds = 240  # 4 minutes for other Opus models
        elif "sonnet" in model.lower():
            timeout_seconds = 180  # 3 minutes for Sonnet models
        else:
            timeout_seconds = 120  # 2 minutes for Haiku and other models
        
        logger.info(f"Making Claude API request with {timeout_seconds}s timeout for model: {model}")
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=timeout_seconds
            )
            
            # Also save the raw response if there's an error
            if not response.ok:
                error_logs_dir = ensure_logs_directory("claude/errors")
                error_filename = os.path.join(error_logs_dir, f"error_{timestamp}.txt")
                try:
                    with open(error_filename, 'w', encoding='utf-8') as f:
                        f.write(f"Status Code: {response.status_code}\n\n")
                        f.write(f"Headers: {dict(response.headers)}\n\n")
                        f.write(f"Content: {response.text}")
                    logger.info(f"Saved error response to {error_filename}")
                except Exception as e:
                    logger.error(f"Error saving API error response: {str(e)}")
            
            response.raise_for_status()
            result = response.json()
            
            content = ""
            if "content" in result and isinstance(result["content"], list):
                for item in result["content"]:
                    if item.get("type") == "text":
                        content += item.get("text", "")
            
            self._log_api_success(task_type, api_start_time)
            return content
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Claude API error: {str(e)}"
            
            if response := getattr(e, 'response', None):
                try:
                    error_detail = response.json()
                    error_msg = f"Claude API error: {error_detail.get('error', {}).get('message', str(e))}"
                except:
                    error_msg = f"Claude API error: HTTP {response.status_code}"
                
                # Special handling for 400 errors
                if response.status_code == 400:
                    logger.error(f"{error_msg} - Content may be too large or violate content policy")
                    # Don't retry for content policy issues
                    if "content policy" in error_msg.lower():
                        return "Error generating content with Claude API: Content policy violation"
                    
                    # Check if it's a token limit issue
                    if "token" in error_msg.lower() and "limit" in error_msg.lower():
                        return "Error generating content with Claude API: Token limit exceeded - try reducing content size"
            
            logger.error(error_msg)
            return f"Error generating content with Claude API: {error_msg}"
            
        except Exception as e:
            error_msg = f"Unexpected error calling Claude API: {str(e)}"
            logger.error(error_msg)
            return f"Error generating content with Claude API: {error_msg}"

class OpenAIAPI(BaseAPI):
    """API class for OpenAI API calls"""
    
    def __init__(self):
        super().__init__("OPENAI_API_KEY", "OPENAI_API_KEY")
    
    def call_api(self, prompt: str, system_prompt: str = "",
               model: str = "gpt-4",
               max_tokens: int = 4000, temperature: float = 0.7,
               task_type: str = "general") -> str:
        
        if not self.api_key:
            return "Error: OPENAI_API_KEY not configured. Please add it to .env or config/api_keys.py"
        
        # Check token limits but don't block execution
        is_within_limits, limit_message = self.check_token_limits(prompt, system_prompt, model, max_tokens)
        if not is_within_limits:
            logger.warning(limit_message)
            # Continue with API call despite token limit warning
            
        if openai is None:
            logger.error("openai package not installed")
            return "Error: openai package not installed"

        client = openai.OpenAI(api_key=self.api_key)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        self._log_api_call(model, task_type)
        
        # Save API request to file before sending
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        api_logs_dir = ensure_logs_directory("openai")
        filename = os.path.join(api_logs_dir, f"request_{timestamp}.json")
        
        try:
            # Create a copy of data with sensible information
            request_data = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            # Save to logs directory
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(request_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved OpenAI API request to {filename}")
        except Exception as e:
            logger.error(f"Error saving OpenAI API request: {str(e)}")
        
        # Make API request
        api_start_time = time.time()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=120
            )
            
            content = response.choices[0].message.content
            
            # Save successful response
            response_logs_dir = ensure_logs_directory("openai/responses")
            response_filename = os.path.join(response_logs_dir, f"response_{timestamp}.json")
            try:
                with open(response_filename, 'w', encoding='utf-8') as f:
                    response_data = {
                        "model": model,
                        "content": content,
                        "usage": response.usage.model_dump() if hasattr(response, 'usage') else {}
                    }
                    json.dump(response_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved OpenAI API response to {response_filename}")
            except Exception as e:
                logger.error(f"Error saving OpenAI API response: {str(e)}")
            
            self._log_api_success(task_type, api_start_time)
            return content
            
        except Exception as e:
            error_msg = f"OpenAI API error: {str(e)}"
            
            # Save error response
            error_logs_dir = ensure_logs_directory("openai/errors")
            error_filename = os.path.join(error_logs_dir, f"error_{timestamp}.txt")
            try:
                with open(error_filename, 'w', encoding='utf-8') as f:
                    f.write(f"Error: {error_msg}\n\n")
                    f.write(f"Model: {model}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                logger.info(f"Saved OpenAI API error to {error_filename}")
            except Exception as e_file:
                logger.error(f"Error saving OpenAI API error response: {str(e_file)}")
                
            logger.error(error_msg)
            return f"Error generating content with OpenAI API: {error_msg}"

# Singleton API instances
_api_instances = {}

def get_api(api_class):
    """Get a singleton API instance"""
    if api_class not in _api_instances:
        _api_instances[api_class] = api_class()
    return _api_instances[api_class]

def get_claude_api():
    """Get the Claude API singleton instance"""
    return get_api(ClaudeAPI)

def get_openai_api():
    """Get the OpenAI API singleton instance"""
    return get_api(OpenAIAPI)

def with_retry(max_retries=3, non_retryable_errors=None):
    """Decorator for API call functions with retry logic"""
    if non_retryable_errors is None:
        non_retryable_errors = ["content policy violation", "token limit exceeded"]
        
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    response = func(*args, **kwargs)
                    
                    # Check if this is a dictionary response (from extended thinking)
                    if isinstance(response, dict):
                        # Check if there's an error in the text field
                        text_content = response.get("text", "")
                        if isinstance(text_content, str) and text_content.startswith("Error generating content with"):
                            error_message = text_content.lower()
                            # Don't retry certain errors
                            if any(err in error_message for err in non_retryable_errors):
                                logger.warning(f"Non-retryable error detected: {text_content[:100]}...")
                                return response
                                
                            logger.warning(f"API call failed on attempt {attempt}/{max_retries}: {text_content[:100]}...")
                            if attempt < max_retries:
                                logger.info(f"Retrying API call (attempt {attempt+1}/{max_retries})...")
                                # If the error is about large content, try truncating
                                if "too large" in error_message or "token limit" in error_message:
                                    if "prompt" in kwargs:
                                        # Truncate the prompt by 25% on each retry
                                        prompt_len = len(kwargs["prompt"])
                                        new_len = int(prompt_len * 0.75)
                                        kwargs["prompt"] = kwargs["prompt"][:new_len] + "... [truncated]"
                                        logger.info(f"Truncated prompt from {prompt_len} to {new_len} chars")
                                continue
                            else:
                                logger.error(f"All {max_retries} API call attempts failed")
                                return response
                        # No error in the response dictionary, return it
                        return response
                    
                    # Original string response handling
                    elif isinstance(response, str) and response.startswith("Error generating content with"):
                        error_message = response.lower()
                        # Don't retry certain errors
                        if any(err in error_message for err in non_retryable_errors):
                            logger.warning(f"Non-retryable error detected: {response[:100]}...")
                            return response
                            
                        logger.warning(f"API call failed on attempt {attempt}/{max_retries}: {response[:100]}...")
                        if attempt < max_retries:
                            logger.info(f"Retrying API call (attempt {attempt+1}/{max_retries})...")
                            # If the error is about large content, try truncating
                            if "too large" in error_message or "token limit" in error_message:
                                if "prompt" in kwargs:
                                    # Truncate the prompt by 25% on each retry
                                    prompt_len = len(kwargs["prompt"])
                                    new_len = int(prompt_len * 0.75)
                                    kwargs["prompt"] = kwargs["prompt"][:new_len] + "... [truncated]"
                                    logger.info(f"Truncated prompt from {prompt_len} to {new_len} chars")
                            continue
                        else:
                            logger.error(f"All {max_retries} attempts failed")
                            return response
                    
                    return response
                except Exception as e:
                    last_error = str(e)
                    logger.warning(f"Error on attempt {attempt}/{max_retries}: {last_error}")
                    if attempt < max_retries:
                        logger.info(f"Retrying (attempt {attempt+1}/{max_retries})...")
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                        return f"Error: {last_error} after {max_retries} attempts"
            
            return f"Error: All {max_retries} attempts failed with: {last_error}"
        return wrapper
    return decorator

def validate_json_response(response):
    """Validate and clean JSON in API response"""
    try:
        # Basic cleanup - find content between curly braces
        json_pattern = r'(\{.*\})'
        json_match = re.search(json_pattern, response, re.DOTALL)
        if json_match:
            clean_json = json_match.group(1)
            # Test if it's valid JSON by parsing it
            json.loads(clean_json)
            # If we got here, JSON is valid
            return True, response
        return False, "No JSON object found in response"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in response: {str(e)}"

@with_retry(max_retries=3)
def generate_with_claude_haiku(prompt: str, system_prompt: str = "",
                             max_tokens: int = 2000, temperature: float = 0.3,
                             model: str = None):
    """
    Generate context using Claude 3 Haiku
    
    This function is optimized for quick context generation, using Claude Haiku
    for maximum efficiency (lower cost and faster responses).
    
    Args:
        prompt: The prompt to send to Claude
        system_prompt: Optional system prompt to include
        max_tokens: Maximum tokens in the response
        temperature: Temperature for response generation
        model: Claude model to use (defaults to centralized CONTEXT_GEN model)
        
    Returns:
        Generated context from Claude
    """
    # Use centralized model configuration if no model specified
    if model is None:
        model = CLAUDE_MODELS["CONTEXT_GEN"]
    
    # Create a default system prompt if none provided
    if not system_prompt:
        system_prompt = """
You're an AI assistant analyzing educational content to extract key facts, concepts, themes, structure and other contextual information.
Provide a concise context summary focusing on the most important information for an instructor to know. 
The context should help a teacher understand the content's purpose, structure, and key points.

Keep the context concise but comprehensive.
"""
    
    # Log warning if model parameter is used (maintaining backward compatibility)
    if model != CLAUDE_MODELS["CONTEXT_GEN"]:
        logger.warning(f"Model parameter override detected in generate_with_claude_haiku: {model}. Using CONTEXT_GEN model instead.")
        # We'll ignore the passed model parameter and use our standardized model
    
    # Call the centralized Claude API handler
    return _call_claude_api(
        prompt=prompt,
        system_prompt=system_prompt,
        model_key="CONTEXT_GEN", # Force use of standardized context generation model
        max_tokens=max_tokens,
        temperature=temperature,
        task_type="context_generation"
    )

@with_retry(max_retries=3)
def generate_with_claude_sonnet(prompt: str, system_prompt: str = "",
                              max_tokens: int = 4000, temperature: float = 0.2,
                              model: str = None) -> str:
    """
    Edit content using Claude 3 Sonnet
    
    This function is optimized for content editing, using Claude Sonnet
    to provide higher quality output for creative tasks.
    
    Args:
        prompt: The prompt to send to Claude
        system_prompt: Optional system prompt to include
        max_tokens: Maximum tokens in the response
        temperature: Temperature for response generation
        model: Claude model to use (defaults to centralized CONTENT_EDIT model)
        
    Returns:
        Generated content from Claude
    """
    # Use centralized model configuration if no model specified
    if model is None:
        model = CLAUDE_MODELS["CONTENT_EDIT"]
    
    # Create a default system prompt if none provided
    if not system_prompt:
        system_prompt = """
You're an expert educational content editor. 
Your task is to improve educational content while maintaining the author's voice, style, and key information.
Focus on clarity, engagement, accuracy, and educational value.
"""
    
    # Log warning if model parameter is used (maintaining backward compatibility)
    if model != CLAUDE_MODELS["CONTENT_EDIT"]:
        logger.warning(f"Model parameter override detected in generate_with_claude_sonnet: {model}. Using CONTENT_EDIT model instead.")
        # We'll ignore the passed model parameter and use our standardized model
    
    # Call the centralized Claude API handler
    return _call_claude_api(
        prompt=prompt,
        system_prompt=system_prompt,
        model_key="CONTENT_EDIT", # Force use of standardized content editing model
        max_tokens=max_tokens,
        temperature=temperature,
        task_type="content_enhancement"
    )

@with_retry(max_retries=3)
def generate_with_claude_extended_thinking(prompt: str, system_prompt: str = "",
                           max_tokens: int = 16000, thinking_budget: int = 8000, temperature: float = 1.0,
                           model: str = None):
    """
    Generate content using Claude 3.7 with extended thinking capability
    
    Args:
        prompt: User prompt
        system_prompt: System prompt
        max_tokens: Maximum tokens in response (must be greater than thinking_budget)
        thinking_budget: Token budget for extended thinking (minimum 1024)
        temperature: Temperature (must be 1.0 when using extended thinking)
        model: Claude model to use (defaults to centralized CONTENT_EDIT model)
        
    Returns:
        Dict with generated text content and thinking content
    """
    # Use centralized model configuration if no model specified
    if model is None:
        model = CLAUDE_MODELS["CONTENT_EDIT"]
    
    # Enforce minimum value for thinking budget
    if thinking_budget < 1024:
        logger.warning(f"Thinking budget {thinking_budget} is less than minimum 1024. Using 1024 instead.")
        thinking_budget = 1024
    
    # Enforce temperature = 1.0 for Extended Thinking
    if temperature != 1.0:
        logger.warning(f"Temperature {temperature} is not 1.0. Extended Thinking requires temperature=1.0. Adjusting.")
        temperature = 1.0
    
    # Get the Claude API instance
    api = get_claude_api()
    
    if not system_prompt:
        # Default system prompt for extended thinking
        base_system = """
You are an expert content creator who thinks deeply before responding. 
When given a task, first describe your thinking process, 
exploring the key considerations, options, and tradeoffs before presenting your final content.
"""
    else:
        base_system = system_prompt
    
    # Create the specialized Claude 3.7 system prompt with extended thinking
    extended_system = f"""
{base_system}

<thinking>
You have {thinking_budget} tokens to think through this problem step by step.
This thinking will be visible to the user.
Use this space to work through the problem thoroughly before providing your response.
</thinking>
"""

    # Log API call
    logger.info(f"Calling Claude API for extended thinking: model={model}")
    
    # Track start time
    start_time = time.time()
    
    try:
        # Make the API call with enforced model
        response = api.call_api(
            prompt=prompt,
            system_prompt=extended_system,
            model=model,  # Use centralized model
            max_tokens=max_tokens,
            temperature=temperature,  # Keep required temperature for extended thinking
            task_type="extended_thinking"
        )
        
        # Parse thinking and content sections
        thinking_pattern = r'<thinking>(.*?)<\/thinking>'
        thinking_match = re.search(thinking_pattern, response, re.DOTALL)
        
        result = {
            "thinking": thinking_match.group(1).strip() if thinking_match else "",
            "content": re.sub(thinking_pattern, '', response, flags=re.DOTALL).strip()
        }
        
        # Get elapsed time
        elapsed_time = time.time() - start_time
        logger.info(f"Extended thinking completed in {elapsed_time:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"Extended thinking error: {str(e)}")
        raise

@with_retry(max_retries=3)
def generate_with_claude_diff_edit(prompt: str, original_content: str, system_prompt: str = "",
                              max_tokens: int = 16000, temperature: float = 0.2,
                              model: str = None):
    """
    Generate edits/diffs for content using Claude rather than regenerating the entire content
    
    This function is optimized for making minor edits to content, instructing Claude to only
    return the specific changes needed rather than regenerating the entire file.
    
    Args:
        prompt: The instruction describing what edits to make
        original_content: The original content to be edited
        system_prompt: Optional system prompt
        max_tokens: Maximum tokens in response
        temperature: Temperature for response generation
        model: Claude model to use (defaults to centralized CONTENT_EDIT model)
        
    Returns:
        Dict with edited content and a diff report
    """
    # Use centralized model configuration if no model specified
    if model is None:
        model = CLAUDE_MODELS["CONTENT_EDIT"]
    
    # Get Claude API instance
    api = get_claude_api()
    
    # Create default system prompt if not provided
    if not system_prompt:
        system_prompt = """
You are an expert editor who helps make precise changes to content.
When given original content and edit instructions, only make the specific requested changes.
Include a detailed diff report explaining what you changed and why.

Your tasks:
1. Apply the requested edits to the original content
2. Create a diff report summarizing what you changed (only note substantial edits, not minor formatting)
3. Return both the edited content and the diff report

DO NOT add unnecessary content, change formatting, or make unrequested edits.
"""
    
    # Create the prompt with original content
    full_prompt = f"""
# Edit Instructions
{prompt}

# Original Content
```
{original_content}
```

Please edit according to the instructions, preserving all content not specifically mentioned for change.
Provide:
1. The complete edited content
2. A brief diff report summarizing what you changed
"""
    
    # Track start time
    start_time = time.time()
    logger.info(f"Calling Claude API for diff editing with {model}")
    
    try:
        # Call the Claude API with the centralized model
        response = api.call_api(
            prompt=full_prompt,
            system_prompt=system_prompt,
            model=model,  # Use centralized model
            max_tokens=max_tokens,
            temperature=temperature,
            task_type="diff_edit"
        )
        
        # Process the response to extract edited content and diff report
        edited_content = ""
        diff_report = ""
        
        # Extract content within code blocks
        code_block_pattern = r"```(?:\w*\n)?(.*?)```"
        content_blocks = re.findall(code_block_pattern, response, re.DOTALL)
        
        if content_blocks:
            # The first code block should be the edited content
            edited_content = content_blocks[0].strip()
        
        # Extract diff report - look for text after the last code block
        last_code_block = response.rfind("```")
        if last_code_block != -1:
            diff_report = response[last_code_block + 3:].strip()
            
            # Look for headers that might indicate the diff report
            diff_headers = ["# Diff Report", "## Diff Report", "### Changes Made", "## Changes", "# Changes"]
            for header in diff_headers:
                pos = diff_report.find(header)
                if pos != -1:
                    diff_report = diff_report[pos:].strip()
                    break
        
        # If we couldn't extract the edited content or diff report
        if not edited_content:
            logger.warning("Could not extract edited content from response, using the whole response")
            edited_content = response
            diff_report = "Could not extract diff report from response."
            
        # Get elapsed time
        elapsed_time = time.time() - start_time
        logger.info(f"Diff editing completed in {elapsed_time:.2f}s")
        
        # Return the result
        return {
            "edited_content": edited_content,
            "diff_report": diff_report,
            "original_content": original_content,
            "elapsed_time": elapsed_time
        }
        
    except Exception as e:
        logger.error(f"Error in diff editing: {str(e)}")
        return {
            "edited_content": original_content,  # Return original content on error
            "diff_report": f"Error: {str(e)}",
            "original_content": original_content,
            "elapsed_time": time.time() - start_time,
            "error": str(e)
        }

@with_retry(max_retries=3)
def edit_markdown_with_claude(markdown_text, instructions, context="", model=None, temperature=0.0):
    """
    Edit markdown content using Claude in a line-by-line approach without requiring tool usage.
    
    Args:
        markdown_text (str): The original markdown content to edit
        instructions (str): Instructions for how to edit the content
        context (str): Optional context about the content for Claude (includes learner profile info)
        model (str): Claude model to use for editing (defaults to centralized CONTENT_EDIT model)
        temperature (float): Temperature for generation
        
    Returns:
        str: The edited markdown content
    """
    import time
    import logging
    import re
    import requests
    
    logger = logging.getLogger(__name__)
    start_time = time.time()
    
    logger.info("Starting direct line-based markdown editing with Claude")
    
    try:
        # Get the Claude API instance
        api = get_claude_api()
        
        # Add line numbers to the markdown content
        lines = markdown_text.split('\n')
        numbered_content = "\n".join([f"[{i+1}] {line}" for i, line in enumerate(lines)])
        
        # Create a clean, focused system prompt that establishes role and constraints only
        system_prompt = """
        You are a markdown content editor that makes surgical, line-specific edits based on educational principles.
        ONLY respond with edit commands - never explanations or commentary.
        """
        
        if context:
            system_prompt += f"\n\nCONTEXT (includes target learner considerations):\n{context}"
        
        # Create user message with task-first information hierarchy
        user_message = f"""
        INSTRUCTIONS:
        {instructions}
        
        EDIT FORMAT SPECIFICATIONS:
        1. To INSERT content after a specific line:
          [EDIT:INSERT:X]
          Your new content here
          [/EDIT]
        
        2. To REPLACE content:
          [EDIT:REPLACE:X-Y]
          Your replacement content here
          [/EDIT]
        
        X and Y represent line numbers from the document.
        DO NOT include line numbers in your output content.
        DO NOT provide any explanation - only the edit commands.
        
        MARKDOWN CONTENT (with line numbers):
        {numbered_content}
        """
        
        # Use centralized model configuration if no model specified
        if model is None:
            model = CLAUDE_MODELS["CONTENT_EDIT"]
        
        # Directly prepare the API request to avoid system prompt as a message role
        headers = {
            "x-api-key": api.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model,  # Use centralized model
            "max_tokens": 4096,
            "temperature": temperature,
            "system": system_prompt,  # System as top-level parameter
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        
        # Make direct API call to ensure correct parameter structure
        logger.info("Making direct API call to ensure correct parameter format")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if not response.ok:
            logger.error(f"Error calling Claude API: {response.status_code} - {response.text}")
            raise Exception(f"API error: {response.status_code}")
        
        # Parse the response
        response_data = response.json()
        api_response = ""
        
        # Extract the content text from the response
        if "content" in response_data and isinstance(response_data["content"], list):
            for item in response_data["content"]:
                if item.get("type") == "text":
                    api_response += item.get("text", "")
        
        logger.info("Received response from Claude, processing edits")
        
        # Process the response to extract edit instructions with new standardized format
        insert_pattern = r'\[EDIT\s*:\s*INSERT\s*:\s*(\d+)\s*\]([\s\S]*?)\[/\s*EDIT\s*\]'
        replace_pattern = r'\[EDIT\s*:\s*REPLACE\s*:\s*(\d+)\s*-\s*(\d+)\s*\]([\s\S]*?)\[/\s*EDIT\s*\]'
        
        # Collect all edits first, then process them in reverse order to prevent line number shifts
        all_edits = []
        
        # Collect insertions (new format)
        for match in re.finditer(insert_pattern, api_response, re.IGNORECASE):
            line_num = int(match.group(1))
            content = match.group(2).strip()
            
            if 1 <= line_num <= len(lines):  # Validate against original lines
                all_edits.append({
                    'type': 'insert',
                    'line_num': line_num,
                    'content': content,
                    'format': 'new'
                })
            else:
                logger.warning(f"Invalid line number for insertion: {line_num}")
        
        # Collect replacements (new format)
        for match in re.finditer(replace_pattern, api_response, re.IGNORECASE):
            start_line = int(match.group(1)) 
            end_line = int(match.group(2))
            content = match.group(3).strip()
            
            if 1 <= start_line <= len(lines) and 1 <= end_line <= len(lines):  # Validate against original lines
                all_edits.append({
                    'type': 'replace',
                    'start_line': start_line,
                    'end_line': end_line,
                    'content': content,
                    'format': 'new'
                })
            else:
                logger.warning(f"Invalid line range for replacement: {start_line}-{end_line}")


        if not all_edits:
            raise ValueError("Claude returned no edit tags or they did not parse")

        # Sort edits in reverse order by line number to prevent line shifting issues
        # For insertions, sort by line_num; for replacements, sort by start_line
        def get_sort_key(edit):
            if edit['type'] == 'insert':
                return edit['line_num']
            else:  # replace
                return edit['start_line']
        
        all_edits.sort(key=get_sort_key, reverse=True)
        
        # Make a copy of the original lines to edit
        edited_lines = lines.copy()
        edits_made = 0
        
        # Apply edits in reverse order (bottom to top)
        for edit in all_edits:
            if edit['type'] == 'insert':
                line_num = edit['line_num']
                content = edit['content']
                format_type = edit['format']
                
                logger.info(f"Inserting content after line {line_num} ({format_type} format)")
                content_lines = content.split('\n')
                # Insert new content after the specified line
                edited_lines[line_num:line_num] = content_lines
                edits_made += 1
                
            elif edit['type'] == 'replace':
                start_line = edit['start_line']
                end_line = edit['end_line']
                content = edit['content']
                format_type = edit['format']
                
                logger.info(f"Replacing lines {start_line}-{end_line} ({format_type} format)")
                # Convert from 1-indexed to 0-indexed
                start_idx = start_line - 1
                end_idx = end_line - 1  # inclusive end
                
                content_lines = content.split('\n')
                # Replace the specified line range
                edited_lines[start_idx:end_idx+1] = content_lines
                edits_made += 1
        
        # Join the edited lines back together
        edited_content = '\n'.join(edited_lines)
        
        # Calculate stats
        elapsed_time = time.time() - start_time
        logger.info(f"Direct line-based editing process completed in {elapsed_time:.2f}s")
        logger.info(f"Applied {edits_made} edits to the document")
        
        return edited_content
        
    except Exception as e:
        logger.error(f"Error in direct line-based markdown editing: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        # Fall back to the original content in case of errors
        return markdown_text

@with_retry(max_retries=3)
def regenerate_markdown_with_claude(markdown_text, instructions, context="", model=None, temperature=0.0):
    """
    Regenerate markdown content using Claude to create a completely new document based on the original.
    Unlike edit_markdown_with_claude, this function creates an entirely new document rather than making line edits.
    
    Args:
        markdown_text (str): The original markdown content
        instructions (str): Instructions for how to regenerate the content
        context (str): Optional context about the content for Claude (includes learner profile info)
        model (str): Claude model to use for editing (defaults to centralized CONTENT_EDIT model)
        temperature (float): Temperature for generation (low temperature reduces creativity)
        
    Returns:
        str: The regenerated markdown content
    """
    import time
    import logging
    import requests
    
    logger = logging.getLogger(__name__)
    start_time = time.time()
    
    logger.info("Starting full markdown document regeneration with Claude")
    
    try:
        # Get the Claude API instance
        api = get_claude_api()
        
        # Create a system prompt that establishes role and constraints
        system_prompt = """
        You are a markdown content regenerator that transforms content based on educational principles.
        Your task is to regenerate the entire content following specific instructions.
        You must return ONLY the complete regenerated content with no additional commentary.
        Keep the structure and meaning of the original document but apply the requested changes.
        DO NOT be creative - follow the instructions precisely with minimal changes to the original content.
        """
        
        if context:
            system_prompt += f"\n\nCONTEXT (includes target learner considerations):\n{context}"
        
        # Create user message with explicit instructions to regenerate entire document
        user_message = f"""
        INSTRUCTIONS:
        {instructions}
        
        IMPORTANT GUIDELINES:
        1. Generate the COMPLETE document incorporating the requested changes.
        2. Return ONLY the regenerated content with NO explanation or commentary.
        3. Maintain the same overall structure and content unless specifically instructed otherwise.
        4. Make minimal changes beyond what is explicitly requested.
        5. DO NOT add creative flourishes or extra content.
        
        ORIGINAL MARKDOWN CONTENT:
        {markdown_text}
        """
        
        # Use centralized model configuration if no model specified
        if model is None:
            model = CLAUDE_MODELS["CONTENT_EDIT"]
        
        # Directly prepare the API request to avoid system prompt as a message role
        headers = {
            "x-api-key": api.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model,  # Use centralized model
            "max_tokens": 16384,  # Larger token limit for full document regeneration
            "temperature": temperature,  # Low temperature to reduce creativity
            "system": system_prompt,  # System as top-level parameter
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        
        # Make direct API call to ensure correct parameter structure
        logger.info("Making direct API call for full document regeneration")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=120  # Increased timeout for larger documents
        )
        
        if not response.ok:
            logger.error(f"Error calling Claude API: {response.status_code} - {response.text}")
            raise Exception(f"API error: {response.status_code}")
        
        # Parse the response
        response_data = response.json()
        regenerated_content = ""
        
        # Extract the content text from the response
        if "content" in response_data and isinstance(response_data["content"], list):
            for item in response_data["content"]:
                if item.get("type") == "text":
                    regenerated_content += item.get("text", "")
        
        # Calculate stats
        elapsed_time = time.time() - start_time
        logger.info(f"Full document regeneration completed in {elapsed_time:.2f}s")
        
        return regenerated_content.strip()
        
    except Exception as e:
        logger.error(f"Error in regenerate_markdown_with_claude: {str(e)}")
        raise e