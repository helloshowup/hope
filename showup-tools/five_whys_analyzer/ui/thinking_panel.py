"""
Thinking Panel Component

Displays Claude's extended thinking process in real-time.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging

# Get logger
logger = logging.getLogger("thinking_panel")

class ThinkingPanel(ttk.Frame):
    """
    Panel for displaying Claude's extended thinking process
    """
    
    def __init__(self, parent):
        """
        Initialize the thinking panel
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.configure(padding=10)
        
        # Create and configure widgets
        self._create_widgets()
        
        # Auto-scroll flag (enabled by default)
        self.auto_scroll = True
    
    def _create_widgets(self):
        """Create and arrange panel widgets"""
        # Panel title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        title_label = ttk.Label(
            title_frame, 
            text="Claude's Thinking Process", 
            font=("Arial", 11, "bold")
        )
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Auto-scroll toggle
        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_check = ttk.Checkbutton(
            title_frame,
            text="Auto-scroll",
            variable=self.auto_scroll_var,
            command=self._toggle_auto_scroll
        )
        auto_scroll_check.pack(side=tk.RIGHT, padx=5)
        
        # Clear button
        clear_button = ttk.Button(
            title_frame,
            text="Clear",
            command=self.clear_content,
            width=8
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Text area for displaying thinking
        self.thinking_text = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Consolas", 10),
            background="#f8f8f8",
            padx=5,
            pady=5
        )
        self.thinking_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a tag for styling
        self.thinking_text.tag_configure("thinking", foreground="#333333")
    
    def _toggle_auto_scroll(self):
        """Toggle auto-scroll behavior"""
        self.auto_scroll = self.auto_scroll_var.get()
        logger.debug(f"Auto-scroll {'enabled' if self.auto_scroll else 'disabled'}")
    
    def clear_content(self):
        """Clear all content from the thinking panel"""
        self.thinking_text.configure(state=tk.NORMAL)
        self.thinking_text.delete(1.0, tk.END)
        self.thinking_text.configure(state=tk.DISABLED)
        logger.debug("Thinking panel content cleared")
    
    def set_content(self, content: str):
        """
        Set the content of the thinking panel
        
        Args:
            content (str): Content to display
        """
        self.thinking_text.configure(state=tk.NORMAL)
        self.thinking_text.delete(1.0, tk.END)
        self.thinking_text.insert(tk.END, content, "thinking")
        self.thinking_text.configure(state=tk.DISABLED)
        
        # Auto-scroll to the end if enabled
        if self.auto_scroll:
            self.thinking_text.see(tk.END)
    
    def append_content(self, content: str):
        """
        Append content to the thinking panel
        
        Args:
            content (str): Content to append
        """
        self.thinking_text.configure(state=tk.NORMAL)
        self.thinking_text.insert(tk.END, content, "thinking")
        self.thinking_text.configure(state=tk.DISABLED)
        
        # Auto-scroll to the end if enabled
        if self.auto_scroll:
            self.thinking_text.see(tk.END)
    
    def get_content(self) -> str:
        """
        Get the current content of the thinking panel
        
        Returns:
            str: Current content
        """
        return self.thinking_text.get(1.0, tk.END)