"""Claude API Module for ShowupSquaredV4

This module maintains backward compatibility with existing imports
by providing a clean interface to the claude_api.py functionality.
"""

# Rather than use relative imports which can be problematic,
# we'll use the existing sys.path structure to find the main module
import os
import sys
import importlib.util

# Get the path to the claude_api.py file
module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'claude_api.py')

# Load the module dynamically to avoid duplication while maintaining the interface
spec = importlib.util.spec_from_file_location('claude_api_impl', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Export all the needed names from the implementation module
# This follows the Single Source Rule by not duplicating code

# Constants
CONTEXT_SYSTEM_PROMPT = module.CONTEXT_SYSTEM_PROMPT
CONTEXT_USER_PROMPT_TEMPLATE = module.CONTEXT_USER_PROMPT_TEMPLATE
CLAUDE_MODELS = module.CLAUDE_MODELS

# Core functions
edit_markdown_with_claude = module.edit_markdown_with_claude
generate_with_claude_haiku = module.generate_with_claude_haiku
generate_with_claude_sonnet = module.generate_with_claude_sonnet
generate_with_claude_extended_thinking = module.generate_with_claude_extended_thinking
generate_with_claude_diff_edit = module.generate_with_claude_diff_edit
regenerate_markdown_with_claude = module.regenerate_markdown_with_claude

# Utility functions
get_api = module.get_api
get_claude_api = module.get_claude_api
get_openai_api = module.get_openai_api
validate_json_response = module.validate_json_response
validate_token_limit = module.validate_token_limit
estimate_token_count = module.estimate_token_count
