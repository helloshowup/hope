"""
Mermaid Diagram Generator

This module generates Mermaid.js diagram syntax for visualizing the 5 Whys analysis.
It creates a directed graph showing the flow from initial problem to root cause.
"""

import logging
import re
from typing import Dict, Any

# Set up logging
logger = logging.getLogger("mermaid_generator")

class MermaidGenerator:
    """
    Generates Mermaid diagrams for the 5 Whys analysis process
    """
    
    def __init__(self):
        """Initialize the Mermaid diagram generator"""
        pass
    
    def generate_diagram(self, data: Dict[str, Any]) -> str:
        """
        Generate a Mermaid diagram from the 5 Whys analysis data
        
        Args:
            data (Dict[str, Any]): Data from the 5 Whys analysis
                {
                    "initial_problem": str,
                    "questions": List[str],
                    "answers": List[str],
                    "root_cause": str,
                    "complete": bool
                }
                
        Returns:
            str: Mermaid diagram syntax
        """
        # Extract data
        initial_problem = data.get("initial_problem", "")
        questions = data.get("questions", [])
        answers = data.get("answers", [])
        root_cause = data.get("root_cause", "")
        complete = data.get("complete", False)
        
        # Start building the diagram
        diagram = ["graph TD"]
        
        # Add the initial problem node
        problem_id = "problem"
        problem_text = self._clean_for_mermaid(initial_problem)
        diagram.append(f'    {problem_id}["{problem_text}"]')
        
        # Add question and answer nodes
        last_node_id = problem_id
        
        for i, question in enumerate(questions, 1):
            # Add the question node
            q_id = f"q{i}"
            q_text = self._clean_for_mermaid(question)
            diagram.append(f'    {q_id}["Why: {q_text}"]')
            
            # Connect previous node to this question
            diagram.append(f'    {last_node_id} --> {q_id}')
            
            # If we have a corresponding answer, add it
            if i <= len(answers):
                # Add the answer node
                a_id = f"a{i}"
                a_text = self._clean_for_mermaid(answers[i-1])
                diagram.append(f'    {a_id}["{a_text}"]')
                
                # Connect question to answer
                diagram.append(f'    {q_id} --> {a_id}')
                
                # Update last node
                last_node_id = a_id
            else:
                # No answer yet, question is the last node
                last_node_id = q_id
        
        # Add root cause if analysis is complete
        if complete and root_cause:
            root_id = "root"
            root_text = self._clean_for_mermaid(root_cause)
            diagram.append(f'    {root_id}["{root_text}"]')
            diagram.append(f'    {last_node_id} --> {root_id}')
        
        # Add styling
        diagram.append("")
        diagram.append("    %% Styling")
        diagram.append("    classDef problem fill:#ffcccc;")
        diagram.append("    classDef question fill:#ccccff;")
        diagram.append("    classDef answer fill:#ccffcc;")
        diagram.append("    classDef rootCause fill:#ffcc99;")
        
        diagram.append("")
        diagram.append("    %% Apply styles")
        diagram.append("    class problem problem;")
        
        # Create class assignments for questions
        q_ids = [f"q{i}" for i in range(1, len(questions) + 1)]
        if q_ids:
            diagram.append(f"    class {','.join(q_ids)} question;")
        
        # Create class assignments for answers
        a_ids = [f"a{i}" for i in range(1, len(answers) + 1)]
        if a_ids:
            diagram.append(f"    class {','.join(a_ids)} answer;")
        
        # Add root cause class if applicable
        if complete and root_cause:
            diagram.append("    class root rootCause;")
        
        # Join all lines
        return "\n".join(diagram)
    
    def _clean_for_mermaid(self, text: str) -> str:
        """
        Clean text for compatibility with Mermaid syntax
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: Cleaned text safe for Mermaid diagrams
        """
        if not text:
            return ""
            
        # Limit text length
        if len(text) > 100:
            text = text[:97] + "..."
            
        # Escape quotes
        text = text.replace('"', '\\"')
        
        # Replace newlines with spaces
        text = re.sub(r'\s*\n\s*', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()