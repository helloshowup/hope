"""
Chat Panel Component

Displays the conversation between the user and Claude,
showing the 5 Whys questions and the user's answers.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
from typing import Callable, Dict, Any, List

# Get logger
logger = logging.getLogger("chat_panel")

class ChatPanel(ttk.Frame):
    """
    Panel for displaying the 5 Whys conversation
    """
    
    def __init__(self, parent):
        """
        Initialize the chat panel
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.configure(padding=10)
        
        # Track messages
        self.messages = []
        
        # Create and configure widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and arrange panel widgets"""
        # Panel title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        title_label = ttk.Label(
            title_frame, 
            text="5 Whys Analysis Conversation", 
            font=("Arial", 11, "bold")
        )
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Clear button
        clear_button = ttk.Button(
            title_frame,
            text="Clear",
            command=self.clear_chat,
            width=8
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            background="#ffffff",
            padx=10,
            pady=5,
            height=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.configure(state=tk.DISABLED)
        
        # Create tags for styling
        self.chat_display.tag_configure("job_context", foreground="#666666", font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_configure("problem", foreground="#990000", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("question", foreground="#000099", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("answer", foreground="#006600", font=("Segoe UI", 10))
        self.chat_display.tag_configure("system", foreground="#666666", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_configure("root_cause", foreground="#990000", font=("Segoe UI", 11, "bold"))
        
        # User input area
        input_frame = ttk.Frame(self)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Input label
        input_label = ttk.Label(
            input_frame,
            text="Your Answer:",
            font=("Segoe UI", 10, "bold")
        )
        input_label.pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        # Text input area
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height=3,
            padx=5,
            pady=5
        )
        self.input_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Add keyboard bindings
        self.input_text.bind("<Control-Return>", self._on_send)
        
        # Send button
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Create a variable to store the on_send callback
        self._on_send_callback = None
        
        self.send_button = ttk.Button(
            button_frame,
            text="Send",
            command=self._send_message,
            width=10
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Initially disable the input area and send button
        self.set_input_state(False)
    
    def _on_send(self, event=None):
        """Handle pressing Ctrl+Enter in the input field"""
        self._send_message()
    
    def _send_message(self):
        """Send the user's message"""
        # Get the message text
        message = self.input_text.get(1.0, tk.END).strip()
        
        # Don't send empty messages
        if not message:
            return
        
        # Clear the input field
        self.input_text.delete(1.0, tk.END)
        
        # Add the message to the chat
        self.add_message("answer", message)
        
        # Call the callback if set
        if self._on_send_callback:
            self._on_send_callback(message)
    
    def set_input_state(self, enabled: bool):
        """
        Enable or disable the input area
        
        Args:
            enabled (bool): Whether input should be enabled
        """
        state = tk.NORMAL if enabled else tk.DISABLED
        self.input_text.configure(state=state)
        self.send_button.configure(state=state)
    
    def set_on_send_callback(self, callback: Callable[[str], None]):
        """
        Set the callback function for when a message is sent
        
        Args:
            callback: Function to call with the message text
        """
        self._on_send_callback = callback
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.messages = []
        logger.debug("Chat panel cleared")
    
    def add_message(self, msg_type: str, content: str):
        """
        Add a message to the chat display
        
        Args:
            msg_type (str): Type of message ("job_context", "problem", "question", "answer", "system", "root_cause")
            content (str): Message content
        """
        self.chat_display.configure(state=tk.NORMAL)
        
        # Add a newline if there's already content
        if self.chat_display.index(tk.END) != "1.0":
            self.chat_display.insert(tk.END, "\n\n")
        
        # Format based on message type
        if msg_type == "job_context":
            self.chat_display.insert(tk.END, "Job Context:\n", "system")
            self.chat_display.insert(tk.END, content, "job_context")
        
        elif msg_type == "problem":
            self.chat_display.insert(tk.END, "Initial Problem:\n", "system")
            self.chat_display.insert(tk.END, content, "problem")
        
        elif msg_type == "question":
            # Extract question number if available
            if isinstance(content, tuple) and len(content) == 2:
                question_number, question_text = content
                prefix = f"Question {question_number}: "
            else:
                prefix = "Question: "
                question_text = content
            
            self.chat_display.insert(tk.END, prefix, "system")
            self.chat_display.insert(tk.END, question_text, "question")
            
            # Enable the input area after a question
            self.set_input_state(True)
            self.input_text.focus_set()
        
        elif msg_type == "answer":
            self.chat_display.insert(tk.END, "Your Answer:\n", "system")
            self.chat_display.insert(tk.END, content, "answer")
            
            # Disable the input area after sending an answer
            self.set_input_state(False)
        
        elif msg_type == "root_cause":
            self.chat_display.insert(tk.END, "Root Cause Identified:\n", "system")
            self.chat_display.insert(tk.END, content, "root_cause")
        
        else:  # System or other messages
            self.chat_display.insert(tk.END, content, "system")
        
        # Store the message
        self.messages.append({"type": msg_type, "content": content})
        
        # Scroll to the end
        self.chat_display.see(tk.END)
        self.chat_display.configure(state=tk.DISABLED)
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in the chat
        
        Returns:
            List[Dict[str, Any]]: List of message objects
        """
        return self.messages.copy()