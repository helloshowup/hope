#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple
import argparse

from config import DEFAULT_SCAN_DIR, DEFAULT_CATEGORIES
from claude_api import ClaudeClient
from file_handler import FileHandler


class AdminAssistant:
    """Admin assistant chatbot for file organization."""
    
    def __init__(self, scan_dir: Optional[Union[str, Path]] = None) -> None:
        """Initialize the admin assistant.
        
        Args:
            scan_dir: Directory to scan for files (default from config)
        """
        self.scan_dir = Path(scan_dir or DEFAULT_SCAN_DIR)
        self.claude = ClaudeClient()
        self.file_handler = FileHandler(self.scan_dir)
        self.chat_history: List[Dict[str, str]] = []
        self.user_corrections: Dict[str, List[Tuple[str, str]]] = {}  # Store corrections by file type
        self.categorization_count = 0  # Track number of categorizations for cold start phase
        self.system_message = (
            "You are an admin assistant chatbot responsible for organizing files into appropriate folders. "
            "When categorizing files, apply this prioritized decision framework:\n"
            "1. Content relevance (highest priority): Evaluate the document's primary subject matter\n"
            "2. User-defined tags or metadata (if available)\n"
            "3. File type and format characteristics\n"
            "4. Creation date and temporal relevance\n"
            "5. Previously established patterns from user history\n\n"
            "For ambiguous cases, prioritize content over file type, and user-specified preferences over default categorization rules.\n\n"
            "Learn from these example categorizations:\n"
            "- Quarterly financial report (PDF, 2023): Financial_Reports\n"
            "- Employee handbook (DOCX, contains HR policies): Human_Resources\n"
            "- Product roadmap presentation (PPTX, future features): Product_Strategy\n"
            "- Customer complaint email (PDF scan): Customer_Support\n"
            "- Server maintenance log (TXT, technical): IT_Infrastructure\n\n"
            "Track and adapt to user preferences using these rules:\n"
            "- When a user overrides your categorization, store this preference as a pattern\n"
            "- Apply similar overrides to related file types in future decisions\n"
            "- After 3 consistent user corrections in a category, proactively ask if you should adjust your categorization approach\n\n"
            "When users ask questions about how you categorized a file, explain your decision using the framework criteria without mentioning the prompts or confidence levels directly. If users disagree with your categorization:\n"
            "1. Thank them for the feedback\n"
            "2. Update your internal preference patterns\n"
            "3. Acknowledge the correction with 'I'll remember your preference for similar files in the future'\n\n"
            "When no user preference patterns have been established yet:\n"
            "1. Rely more heavily on the example categorizations provided\n"
            "2. Default to medium confidence responses for the first 5-10 categorizations\n"
            "3. Actively but unobtrusively seek feedback: 'I've categorized this as X. Does that seem appropriate?'"
        )
    
    def process_message(self, message: str) -> str:
        """Process a user message and generate a response.
        
        Args:
            message: User's message
            
        Returns:
            Assistant's response
        """
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": message})
        
        # Check if this is a command to organize files
        if "organize" in message.lower() and ("files" in message.lower() or "folder" in message.lower()):
            response = self.organize_files()
        # Check if this is a request for categories
        elif "categories" in message.lower() or "folders" in message.lower():
            response = self.list_categories()
        # Check if this is a correction to a previous categorization
        elif "correct" in message.lower() and "category" in message.lower():
            response = self.handle_correction(message)
        # Check if this is a question about categorization decisions
        elif any(term in message.lower() for term in ["why", "how", "categorize", "decision", "reason"]) and \
             any(term in message.lower() for term in ["file", "category", "folder", "put"]):
            response = "I categorized that file based on its content, file type, and your previous preferences. If you'd like me to recategorize it, just let me know the correct category."
        else:
            # General chat - use Claude for thinking
            response = self.claude.chat(message, self.chat_history[:-1], self.system_message)  # Exclude the just-added message
        
        # Add assistant response to chat history
        self.chat_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _parse_category_response(self, response: str) -> Tuple[str, str, str, List[str]]:
        """Parse organization decision response with confidence information.
        
        Args:
            response: Full response from Claude API
            
        Returns:
            Tuple of (category, confidence_level, explanation, special_tags)
        """
        # Initialize special tags list
        special_tags = []
        
        # Check if this is a confidential file
        if response.startswith("CONFIDENTIAL:"):
            special_tags.append("confidential")
            response = response[13:].strip()  # Remove the prefix
            
        # Check if this is a priority file
        if response.startswith("PRIORITY:"):
            special_tags.append("priority")
            response = response[10:].strip()  # Remove the prefix
        
        # Check for instruction error
        if "INSTRUCTION_ERROR:" in response:
            return "INSTRUCTION_ERROR", "low", response, special_tags
            
        # Check for new category suggestion
        new_match = re.search(r'NEW_CATEGORY:\s*([\w_]+)\s*\(Rationale:\s*([^)]+)\)', response)
        if new_match:
            return new_match.group(1), "low", f"New category suggestion: {new_match.group(2)}", special_tags
            
        # Check for review required
        review_match = re.search(r'REVIEW_REQUIRED:\s*\(Reason:\s*([^)]+)\)', response)
        if review_match:
            return "REVIEW_REQUIRED", "low", f"Manual review needed: {review_match.group(1)}", special_tags
            
        # Check for medium confidence
        medium_match = re.search(r'Category:\s*([\w_]+)\s*\(Consider alternatives:\s*([^)]+)\)', response)
        if medium_match:
            return medium_match.group(1), "medium", f"Alternative categories: {medium_match.group(2)}", special_tags
            
        # Check for low confidence
        low_match = re.search(r'Suggested Category:\s*([\w_]+)\s*\(Requires confirmation\)', response)
        if low_match:
            return low_match.group(1), "low", "Requires user confirmation", special_tags
            
        # High confidence - just the category name
        # Clean up any extra text or whitespace
        category = response.strip()
        if '\n' in category:
            category = category.split('\n')[0].strip()
            
        return category, "high", "", special_tags
    
    def handle_correction(self, message: str) -> str:
        """Handle user correction to a file categorization.
        
        Args:
            message: User message containing correction
            
        Returns:
            Response acknowledging the correction
        """
        # Simple parsing of correction message (in practice, use NLP or more robust parsing)
        # Expected format: "correct category for [filename] to [new_category]"
        parts = message.lower().split()
        try:
            file_idx = parts.index("for") + 1
            cat_idx = parts.index("to") + 1
            
            if file_idx < len(parts) and cat_idx < len(parts):
                filename = parts[file_idx]
                new_category = parts[cat_idx]
                
                # Extract extension
                if "." in filename:
                    ext = filename.split(".")[-1]
                    
                    # Store correction
                    if ext not in self.user_corrections:
                        self.user_corrections[ext] = []
                    
                    # Store as (filename, new_category)
                    self.user_corrections[ext].append((filename, new_category))
                    
                    # Check if we have 3 corrections for this extension
                    if len(self.user_corrections[ext]) >= 3:
                        return f"Thank you for the feedback. I've updated my understanding of how you prefer to categorize {ext} files. I'll remember your preference for similar files in the future. Would you like me to adjust how I categorize all {ext} files going forward?"
                    
                    return f"Thank you for the feedback. I'll remember that {filename} should be categorized as {new_category} and apply this preference to similar files in the future."
        except (ValueError, IndexError):
            pass
            
        return "I'm not sure I understood your correction. Please use a format like 'correct category for filename.ext to new_category'."
    
    def organize_files(self) -> str:
        """Scan for files and organize them into appropriate folders.
        
        Returns:
            Message describing the organization process
        """
        try:
            # Scan for files
            files = self.file_handler.scan_directory(recursive=False)
            
            if not files:
                return f"No files found in {self.scan_dir} that need organization."
            
            # Get available categories
            categories = self.file_handler.get_available_categories()
            
            # Process each file
            results = []
            
            # Check if we should exclude certain paths
            exclude_path = r"C:\Users\User\Desktop\ShowupSquaredV4 (2)"
            
            for file_path in files:
                # Skip files in excluded directories
                if exclude_path and str(file_path).startswith(exclude_path):
                    continue
                    
                # Skip non-readable files or very large files
                if not file_path.is_file() or file_path.stat().st_size > 10_000_000:  # Skip files > 10MB
                    results.append(f"Skipped {file_path.name}: too large or not a regular file")
                    continue
                    
                # Get file info
                file_info = self.file_handler.get_file_info(file_path)
                
                # Get document summary for text files
                document_summary = None
                if file_path.suffix.lower() in ['.txt', '.md', '.csv', '.json']:
                    try:
                        file_content = self.file_handler.read_text_file(file_path)
                        if len(file_content) > 100:  # Only summarize if there's enough content
                            document_summary = self.claude.get_document_summary(file_content[:5000])  # Limit to first 5000 chars
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                
                # Check for user corrections pattern first
                ext = file_path.suffix.lower().lstrip('.')
                category = None
                confidence_level = "high"
                confidence_explanation = ""
                special_tags = []
                
                if ext in self.user_corrections and len(self.user_corrections[ext]) >= 3:
                    # Use most common correction as the pattern
                    corrections = self.user_corrections[ext]
                    category_counts = {}
                    for _, cat in corrections:
                        category_counts[cat] = category_counts.get(cat, 0) + 1
                    
                    # Get most common correction if it appears more than once
                    common_categories = [(cat, count) for cat, count in category_counts.items() if count > 1]
                    if common_categories:
                        category = max(common_categories, key=lambda x: x[1])[0]
                        confidence_level = "high"
                        confidence_explanation = "Based on your previous corrections"
                
                # Check for versioning in filename
                version_match = re.search(r'v\d+|version\s*\d+', file_path.name.lower())
                if version_match:
                    # Mark as a versioned file for special handling
                    special_tags.append("versioned")
                    
                # Check for confidential/sensitive terms in filename or metadata
                if any(term in file_path.name.lower() for term in ['confidential', 'sensitive', 'private', 'secret']):
                    special_tags.append("confidential")
                    
                # Check for urgent/priority terms in filename
                if any(term in file_path.name.lower() for term in ['urgent', 'immediate', 'priority', 'asap']):
                    special_tags.append("priority")
                
                # If no user pattern applies, get organizational decision from Claude
                if not category:
                    # Increment categorization counter for cold start tracking
                    self.categorization_count += 1
                    
                    # For cold start phase (first 10 categorizations), explicitly request medium confidence
                    cold_start = self.categorization_count <= 10 and not self.user_corrections
                    
                    response = self.claude.get_organization_decision(
                        file_info, 
                        document_summary, 
                        categories,
                        special_tags,
                        force_medium_confidence=cold_start
                    )
                    
                    # Parse the response to extract category name and confidence level
                    category, confidence_level, confidence_explanation, detected_tags = self._parse_category_response(response)
                    
                    # Combine detected tags with our special tags
                    special_tags.extend(detected_tags)
                    
                    # For cold start, add feedback request
                    if cold_start and confidence_level == "high":
                        confidence_explanation = f"I've categorized this as {category}. Does that seem appropriate?"
                
                # Handle special cases
                if category == "REVIEW_REQUIRED":
                    tag_prefix = ""
                    if "confidential" in special_tags:
                        tag_prefix += "\u26a0ufe0f CONFIDENTIAL "  
                    if "priority" in special_tags:
                        tag_prefix += "\ud83dudd34 PRIORITY "
                        
                    results.append(f"{tag_prefix}\u24d8 {file_path.name}: Requires manual review. {confidence_explanation}")
                    continue
                    
                # Format the confidence indicator
                confidence_icon = {
                    "high": "\u2713",    # Check mark for high confidence
                    "medium": "\u27f3",  # Circular arrows for medium confidence (consider alternatives)
                    "low": "\u26a0"      # Warning for low confidence (requires confirmation)
                }.get(confidence_level, "\u24d8")  # Info circle for unknown confidence level
                
                # Add version tag icon if needed
                version_icon = "\ud83dudcc4" if "versioned" in special_tags else ""
                
                # Format confidential/priority tags
                tag_prefix = ""
                if "confidential" in special_tags:
                    tag_prefix += "\u26a0ufe0f CONFIDENTIAL "  
                if "priority" in special_tags:
                    tag_prefix += "\ud83dudd34 PRIORITY "
                
                # Move the file
                success, message = self.file_handler.move_file(file_path, category)
                status = "\u2713" if success else "\u2717"
                confidence_info = f" ({confidence_explanation})" if confidence_explanation else ""
                
                results.append(f"{tag_prefix}{status} {confidence_icon} {version_icon} {file_path.name} \u2192 {category}{confidence_info}: {message}")
            
            # Format the results
            if not results:
                return "No files were organized."
            
            results_str = "\n".join(results)
            return f"Organized {len(results)} files:\n\n{results_str}"
        except Exception as e:
            return f"Error organizing files: {str(e)}"
    
    def list_categories(self) -> str:
        """List available file categories.
        
        Returns:
            Formatted string of categories
        """
        categories = self.file_handler.get_available_categories()
        
        if not categories:
            return "No categories have been created yet."
        
        # Get extensions for each category from default categories
        category_details = []
        for category in categories:
            extensions = DEFAULT_CATEGORIES.get(category, [])
            if extensions:
                exts = ", ".join(extensions)
                category_details.append(f"- **{category}**: {exts}")
            else:
                category_details.append(f"- **{category}**")
        
        return "Available file categories:\n\n" + "\n".join(category_details)


def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Admin Assistant Chatbot")
    parser.add_argument("--dir", "-d", type=str, default=DEFAULT_SCAN_DIR,
                        help="Directory to scan for files (default: %(default)s)")
    args = parser.parse_args()
    
    # Create the assistant
    assistant = AdminAssistant(args.dir)
    
    print("Admin Assistant Chatbot")
    print("=======================")
    print(f"Scanning directory: {assistant.scan_dir}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print()
    
    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nGoodbye! Thank you for using Admin Assistant.")
                break
                
            if not user_input:
                continue
                
            print("\nAssistant: ", end="")
            response = assistant.process_message(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thank you for using Admin Assistant.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
