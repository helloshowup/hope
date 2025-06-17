"""
File Manager for the 5 Whys Root Cause Analysis Chatbot

Handles saving and loading analysis sessions, exporting results,
and managing history.
"""

import os
import json
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional

# Get logger
logger = logging.getLogger("file_manager")

class FileManager:
    """
    Manages file operations for the 5 Whys analysis tool
    """
    
    def __init__(self, history_dir: str = "history"):
        """
        Initialize the file manager
        
        Args:
            history_dir (str): Directory to store history files
        """
        self.history_dir = history_dir
        self._ensure_directory(history_dir)
    
    def _ensure_directory(self, directory: str) -> None:
        """
        Ensure that a directory exists
        
        Args:
            directory (str): Directory path
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
    
    def save_analysis(self, analysis_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save analysis data to a JSON file
        
        Args:
            analysis_data (Dict[str, Any]): Analysis data to save
            filename (str, optional): Custom filename. If None, a timestamp-based name is used.
            
        Returns:
            str: Path to the saved file
        """
        self._ensure_directory(self.history_dir)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Try to create a meaningful filename based on the problem
            problem = analysis_data.get("initial_problem", "")
            problem_slug = self._create_slug(problem)
            
            if problem_slug:
                filename = f"{timestamp}_{problem_slug}.json"
            else:
                filename = f"{timestamp}_analysis.json"
        
        # Ensure filename has .json extension
        if not filename.endswith(".json"):
            filename += ".json"
        
        # Create full file path
        filepath = os.path.join(self.history_dir, filename)
        
        # Add metadata to analysis data
        save_data = analysis_data.copy()
        save_data["saved_at"] = datetime.now().isoformat()
        
        # Save to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Analysis saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            return ""
    
    def load_analysis(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load analysis data from a JSON file
        
        Args:
            filepath (str): Path to the analysis file
            
        Returns:
            Optional[Dict[str, Any]]: Loaded analysis data or None if loading failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Analysis loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading analysis: {str(e)}")
            return None
    
    def export_markdown(self, analysis_data: Dict[str, Any], filepath: Optional[str] = None) -> str:
        """
        Export analysis data to a Markdown file
        
        Args:
            analysis_data (Dict[str, Any]): Analysis data to export
            filepath (str, optional): Path to export to. If None, a default path is used.
            
        Returns:
            str: Path to the exported file
        """
        # Extract relevant data
        initial_problem = analysis_data.get("initial_problem", "")
        job_context = analysis_data.get("job_context", "")
        questions = analysis_data.get("questions", [])
        answers = analysis_data.get("answers", [])
        root_cause = analysis_data.get("root_cause", "")
        mermaid_diagram = analysis_data.get("mermaid_diagram", "")
        
        # Generate filename if not provided
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            problem_slug = self._create_slug(initial_problem)
            
            if problem_slug:
                filename = f"{timestamp}_{problem_slug}.md"
            else:
                filename = f"{timestamp}_analysis.md"
            
            filepath = os.path.join(self.history_dir, filename)
        
        # Ensure filepath has .md extension
        if not filepath.endswith(".md"):
            filepath += ".md"
        
        # Build Markdown content
        md_content = [
            "# 5 Whys Root Cause Analysis",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Job Context",
            "",
            job_context,
            "",
            "## Initial Problem",
            "",
            initial_problem,
            "",
            "## Analysis Process"
        ]
        
        # Add questions and answers
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            md_content.extend([
                "",
                f"### Question {i}",
                "",
                question,
                "",
                f"### Answer {i}",
                "",
                answer
            ])
        
        # Add root cause
        if root_cause:
            md_content.extend([
                "",
                "## Root Cause",
                "",
                root_cause
            ])
        
        # Add Mermaid diagram
        if mermaid_diagram:
            md_content.extend([
                "",
                "## Analysis Diagram",
                "",
                "```mermaid",
                mermaid_diagram,
                "```"
            ])
        
        # Write to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_content))
            logger.info(f"Analysis exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error exporting to Markdown: {str(e)}")
            return ""
    
    def list_history(self) -> List[Dict[str, Any]]:
        """
        List all saved analysis files with metadata
        
        Returns:
            List[Dict[str, Any]]: List of analysis metadata
        """
        self._ensure_directory(self.history_dir)
        
        history_list = []
        
        # Get all JSON files in the history directory
        for filename in os.listdir(self.history_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.history_dir, filename)
                
                try:
                    # Get file stats
                    stats = os.stat(filepath)
                    
                    # Try to load basic metadata without loading entire file
                    metadata = {
                        "filename": filename,
                        "filepath": filepath,
                        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        "size": stats.st_size
                    }
                    
                    # Try to get the initial problem from the file
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            metadata["initial_problem"] = data.get("initial_problem", "")
                            metadata["saved_at"] = data.get("saved_at", metadata["modified"])
                    except:
                        # If we can't read the file, just use the filename
                        metadata["initial_problem"] = filename.replace(".json", "")
                    
                    history_list.append(metadata)
                except Exception as e:
                    logger.warning(f"Error reading history file {filename}: {str(e)}")
        
        # Sort by saved_at or modified date (newest first)
        history_list.sort(key=lambda x: x.get("saved_at", x["modified"]), reverse=True)
        
        return history_list
    
    def _create_slug(self, text: str, max_length: int = 30) -> str:
        """
        Create a URL-friendly slug from text
        
        Args:
            text (str): Text to convert to slug
            max_length (int): Maximum length of the slug
            
        Returns:
            str: The slug
        """
        if not text:
            return ""
        
        # Lowercase and replace spaces with underscores
        slug = text.lower().replace(" ", "_")
        
        # Remove special characters
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        
        # Truncate to max_length
        if len(slug) > max_length:
            slug = slug[:max_length]
        
        # Remove trailing underscores
        slug = slug.rstrip("_")
        
        return slug