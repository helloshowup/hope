"""
Five Whys Analysis Engine

This module handles the core logic for conducting a 5 Whys root cause analysis
using Claude 3.7 with extended thinking capabilities.
"""

import logging
import re
from typing import Dict, Any, Optional, Tuple

from .claude_api_ext import ClaudeExtendedClient

# Set up logging
logger = logging.getLogger("five_whys_engine")

class FiveWhysEngine:
    """
    Engine for conducting a 5 Whys root cause analysis
    """
    
    def __init__(self):
        """Initialize the Five Whys Engine"""
        self.claude_client = ClaudeExtendedClient()
        self.job_context = ""
        self.initial_problem = ""
        self.questions = []
        self.answers = []
        self.current_question = 0
        self.thinking_history = []
        self.analysis_complete = False
        self.root_cause = ""
        
    def validate_setup(self) -> Tuple[bool, str]:
        """
        Validate that the engine is properly set up with API keys
        
        Returns:
            Tuple[bool, str]: Success status and message
        """
        if not self.claude_client.check_api_key():
            return False, "Claude API key not configured. Please add ANTHROPIC_API_KEY to .env file."
        return True, "Setup validated successfully."
    
    def reset_analysis(self):
        """Reset the analysis to start a new one"""
        self.questions = []
        self.answers = []
        self.current_question = 0
        self.thinking_history = []
        self.analysis_complete = False
        self.root_cause = ""
        
    def set_context(self, job_context: str, initial_problem: str):
        """
        Set the context for a new 5 Whys analysis
        
        Args:
            job_context (str): The job context for the analysis
            initial_problem (str): The initial problem statement
        """
        self.job_context = job_context
        self.initial_problem = initial_problem
        self.reset_analysis()
        
    def start_analysis(self, on_thinking_update=None, on_question_ready=None) -> Dict[str, Any]:
        """
        Start a new 5 Whys analysis and generate the first question
        
        Args:
            on_thinking_update: Callback for thinking updates
            on_question_ready: Callback when question is ready
            
        Returns:
            Dict containing the first question and analysis state
        """
        if not self.job_context or not self.initial_problem:
            return {
                "error": "Job context and initial problem must be set before starting analysis"
            }
            
        logger.info("Starting 5 Whys analysis")
        
        # Build the initial prompt
        initial_prompt = self._build_initial_prompt()
        
        # Call Claude with extended thinking
        def stream_callback(content_type, content):
            if content_type == "thinking" and on_thinking_update:
                on_thinking_update(content)
        
        response = self.claude_client.call_with_extended_thinking(
            prompt=initial_prompt,
            system_prompt="You are an AI assistant specializing in root cause analysis using the 5 Whys method.",
            thinking_budget=24000,
            max_tokens=4000,
            temperature=0.3,
            stream=True if on_thinking_update else False,
            stream_callback=stream_callback
        )
        
        if "error" in response:
            return {"error": response["error"]}
        
        # Store thinking history
        self.thinking_history.append(response.get("thinking", ""))
        
        # Extract the first question from the response
        question = self._extract_question(response["text"])
        
        if question:
            self.questions.append(question)
            self.current_question = 1
            
            if on_question_ready:
                on_question_ready(question, 1)
            
            return {
                "question": question,
                "question_number": 1,
                "total_questions": 5,
                "thinking": response.get("thinking", ""),
                "complete": False
            }
        else:
            return {
                "error": "Failed to extract first question from Claude's response",
                "raw_response": response["text"]
            }
    
    def process_answer(self, answer: str, on_thinking_update=None, on_question_ready=None) -> Dict[str, Any]:
        """
        Process the user's answer and generate the next question
        
        Args:
            answer (str): The user's answer to the current question
            on_thinking_update: Callback for thinking updates
            on_question_ready: Callback when question is ready
            
        Returns:
            Dict containing the next question or final analysis
        """
        if len(self.questions) == 0:
            return {"error": "No questions have been asked yet. Start the analysis first."}
            
        # Store the answer
        self.answers.append(answer)
        
        # If we've completed 5 questions, finalize the analysis
        if len(self.questions) >= 5:
            return self._finalize_analysis(on_thinking_update)
        
        # Build the prompt for the next question
        next_prompt = self._build_next_prompt(answer)
        
        # Call Claude with extended thinking
        def stream_callback(content_type, content):
            if content_type == "thinking" and on_thinking_update:
                on_thinking_update(content)
        
        response = self.claude_client.call_with_extended_thinking(
            prompt=next_prompt,
            system_prompt="You are an AI assistant specializing in root cause analysis using the 5 Whys method.",
            thinking_budget=24000,
            max_tokens=4000,
            temperature=0.3,
            stream=True if on_thinking_update else False,
            stream_callback=stream_callback
        )
        
        if "error" in response:
            return {"error": response["error"]}
        
        # Store thinking history
        self.thinking_history.append(response.get("thinking", ""))
        
        # Extract the next question from the response
        question = self._extract_question(response["text"])
        
        if question:
            self.questions.append(question)
            self.current_question += 1
            
            if on_question_ready:
                on_question_ready(question, self.current_question)
            
            return {
                "question": question,
                "question_number": self.current_question,
                "total_questions": 5,
                "thinking": response.get("thinking", ""),
                "complete": False
            }
        else:
            return {
                "error": "Failed to extract question from Claude's response",
                "raw_response": response["text"]
            }
    
    def _finalize_analysis(self, on_thinking_update=None) -> Dict[str, Any]:
        """
        Finalize the 5 Whys analysis after all questions have been answered
        
        Args:
            on_thinking_update: Callback for thinking updates
            
        Returns:
            Dict containing the final analysis
        """
        # Build the prompt for the final analysis
        final_prompt = self._build_final_prompt()
        
        # Call Claude with extended thinking
        def stream_callback(content_type, content):
            if content_type == "thinking" and on_thinking_update:
                on_thinking_update(content)
        
        response = self.claude_client.call_with_extended_thinking(
            prompt=final_prompt,
            system_prompt="You are an AI assistant specializing in root cause analysis using the 5 Whys method.",
            thinking_budget=24000,
            max_tokens=4000,
            temperature=0.3,
            stream=True if on_thinking_update else False,
            stream_callback=stream_callback
        )
        
        if "error" in response:
            return {"error": response["error"]}
        
        # Store thinking history
        self.thinking_history.append(response.get("thinking", ""))
        
        # Extract the root cause from the final response
        self.root_cause = self._extract_root_cause(response["text"])
        self.analysis_complete = True
        
        return {
            "root_cause": self.root_cause,
            "questions": self.questions,
            "answers": self.answers,
            "thinking": response.get("thinking", ""),
            "complete": True,
            "final_analysis": response["text"]
        }
    
    def get_diagram_data(self) -> Dict[str, Any]:
        """
        Get the data needed to generate a Mermaid diagram of the analysis
        
        Returns:
            Dict containing diagram data
        """
        return {
            "initial_problem": self.initial_problem,
            "questions": self.questions,
            "answers": self.answers,
            "root_cause": self.root_cause,
            "complete": self.analysis_complete
        }
    
    def _build_initial_prompt(self) -> str:
        """
        Build the initial prompt to start the 5 Whys analysis
        
        Returns:
            str: The prompt for the initial question
        """
        return f"""You are an AI assistant specializing in root cause analysis using the 5 Whys method. Your task is to help identify the root cause of a problem by asking a series of five "Why?" questions. You will be given a job context and an initial problem statement.

First, review the following information:

Job Context:
<job_context>
{self.job_context}
</job_context>

Initial Problem:
<problem>
{self.initial_problem}
</problem>

Your goal is to ask five sequential "Why?" questions, one at a time, to uncover the root cause of the problem. Each question should build upon the previous answer and dig deeper into the issue. Follow these guidelines:

1. Ask only one question at a time.
2. Number each question from 1 to 5.
3. Base each follow-up question on the user's previous answer.
4. Focus on the specific issue mentioned in the previous response.
5. Aim to uncover underlying causes rather than symptoms.

Before asking each question, wrap your analysis in <analysis> tags to:
1. Summarize the previous answer or initial problem
2. Identify key factors or potential causes
3. Formulate your next "Why?" question based on these factors

Consider how the previous response relates to the overall problem and what deeper issues it might reveal.

Format your questions using <question> tags with a number attribute, like this:
<question number="1">Why [insert your specific question here]?</question>

Do not provide any additional commentary or explanation outside of the <analysis> and <question> tags. After the fifth question, end the process without providing any analysis or conclusions.

Begin by formulating your first question based on the initial problem statement.

<analysis>
[Summarize the initial problem statement and how it relates to the job context. Identify key factors or potential causes. Formulate a question that addresses the most immediate cause of the problem.]
</analysis>"""

    def _build_next_prompt(self, answer: str) -> str:
        """
        Build the prompt for the next question based on the previous answer
        
        Args:
            answer (str): The user's answer to the previous question
            
        Returns:
            str: The prompt for the next question
        """
        # Build conversation history
        conversation = f"""Job Context:
<job_context>
{self.job_context}
</job_context>

Initial Problem:
<problem>
{self.initial_problem}
</problem>

"""
        
        # Add all previous questions and answers
        for i, (q, a) in enumerate(zip(self.questions, self.answers), 1):
            conversation += f"<question number=\"{i}\">{q}</question>\n\n"
            conversation += f"<answer>\n{a}\n</answer>\n\n"
        
        # Add the latest answer
        if len(self.questions) > len(self.answers):
            conversation += f"<question number=\"{len(self.questions)}\">{self.questions[-1]}</question>\n\n"
            conversation += f"<answer>\n{answer}\n</answer>\n\n"
        
        next_question_number = len(self.questions) + 1
        
        prompt = f"""You are an AI assistant specializing in root cause analysis using the 5 Whys method. You've been asking a series of "Why?" questions to understand the root cause of a problem. Here's the conversation so far:

{conversation}

Based on the answer provided, continue the 5 Whys process by asking the next "Why?" question.

Analyze the answer using <analysis> tags:
1. Summarize the key points from the answer
2. Identify potential causes or factors mentioned
3. Consider how these relate to the original problem
4. Determine what aspects need further exploration

Then formulate question #{next_question_number} (out of 5) that delves deeper into understanding the underlying cause.

Format your response using only:
<analysis>
[Your analysis here]
</analysis>

<question number="{next_question_number}">Why [your specific question here]?</question>

Do not provide any commentary outside these tags."""

        return prompt

    def _build_final_prompt(self) -> str:
        """
        Build the prompt for the final analysis after all 5 questions
        
        Returns:
            str: The prompt for the final analysis
        """
        # Build conversation history
        conversation = f"""Job Context:
<job_context>
{self.job_context}
</job_context>

Initial Problem:
<problem>
{self.initial_problem}
</problem>

"""
        
        # Add all questions and answers
        for i, (q, a) in enumerate(zip(self.questions, self.answers), 1):
            conversation += f"<question number=\"{i}\">{q}</question>\n\n"
            conversation += f"<answer>\n{a}\n</answer>\n\n"
        
        prompt = f"""You are an AI assistant specializing in root cause analysis using the 5 Whys method. You've completed asking five "Why?" questions to understand the root cause of a problem. Here's the complete conversation:

{conversation}

Now that we've completed the 5 Whys process, please provide a final analysis that:

1. Summarizes the initial problem
2. Reviews each of the five "Why?" questions and answers
3. Identifies the root cause based on this analysis
4. Suggests possible solutions or next steps based on addressing this root cause

Format your response with clear sections:

<summary>
[Summarize the initial problem and context]
</summary>

<analysis>
[Provide your detailed analysis of the 5 Whys progression]
</analysis>

<root_cause>
[Clearly state what you've identified as the root cause]
</root_cause>

<recommendations>
[Suggest solutions or next steps to address the root cause]
</recommendations>"""

        return prompt

    def _extract_question(self, text: str) -> Optional[str]:
        """
        Extract the question from Claude's response using regex
        
        Args:
            text (str): The response text from Claude
            
        Returns:
            Optional[str]: The extracted question or None if not found
        """
        # Try to match the XML format first
        pattern = r'<question\s+number="\d+">(.+?)</question>'
        matches = re.search(pattern, text, re.DOTALL)
        
        if matches:
            return matches.group(1).strip()
        
        # Alternative match for more flexible detection
        alt_pattern = r'Why\s+.+?\?'
        alt_matches = re.search(alt_pattern, text)
        
        if alt_matches:
            return alt_matches.group(0).strip()
        
        return None
    
    def _extract_root_cause(self, text: str) -> str:
        """
        Extract the root cause from the final analysis
        
        Args:
            text (str): The final analysis text from Claude
            
        Returns:
            str: The extracted root cause or empty string if not found
        """
        # Try to match the XML format first
        pattern = r'<root_cause>(.+?)</root_cause>'
        matches = re.search(pattern, text, re.DOTALL)
        
        if matches:
            return matches.group(1).strip()
        
        # Alternative pattern for more flexible detection
        alt_pattern = r'(?:Root\s+Cause|ROOT\s+CAUSE)[:\s]+(.+?)(?:\n\n|\n<|$)'
        alt_matches = re.search(alt_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if alt_matches:
            return alt_matches.group(1).strip()
        
        # If all else fails, return the whole final analysis
        return text.strip()