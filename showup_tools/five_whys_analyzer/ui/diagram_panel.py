"""
Diagram Panel Component

Displays the Mermaid diagram visualizing the 5 Whys analysis.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
import tempfile
import os
import webbrowser
import threading

# Get logger
logger = logging.getLogger("diagram_panel")

class DiagramPanel(ttk.Frame):
    """
    Panel for displaying the Mermaid diagram of the 5 Whys analysis
    """
    
    def __init__(self, parent):
        """
        Initialize the diagram panel
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.configure(padding=10)
        
        # Current diagram content
        self.current_diagram = ""
        
        # Create and configure widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and arrange panel widgets"""
        # Panel title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        title_label = ttk.Label(
            title_frame, 
            text="Analysis Diagram", 
            font=("Arial", 11, "bold")
        )
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Button frame
        button_frame = ttk.Frame(title_frame)
        button_frame.pack(side=tk.RIGHT)
        
        # Open in browser button
        self.open_button = ttk.Button(
            button_frame,
            text="Open in Browser",
            command=self._open_in_browser,
            width=15,
            state=tk.DISABLED
        )
        self.open_button.pack(side=tk.RIGHT, padx=5)
        
        # Copy as text button
        self.copy_button = ttk.Button(
            button_frame,
            text="Copy Mermaid",
            command=self._copy_to_clipboard,
            width=15,
            state=tk.DISABLED
        )
        self.copy_button.pack(side=tk.RIGHT, padx=5)
        
        # Display area
        display_frame = ttk.Frame(self)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # We'll show the diagram using two different methods:
        # 1. Plain text representation for the Mermaid syntax
        # 2. HTML preview with placeholder for browser rendering
        
        # Create a notebook for the two views
        self.notebook = ttk.Notebook(display_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Text view
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="Text View")
        
        self.diagram_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            padx=5,
            pady=5
        )
        self.diagram_text.pack(fill=tk.BOTH, expand=True)
        
        # Preview label
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="Preview")
        
        # In a production app, we might embed a browser or use a library
        # to render Mermaid. For simplicity, we'll just show instructions
        # and provide a button to open in browser.
        self.preview_label = ttk.Label(
            preview_frame,
            text="Diagram will be shown in your browser when you click 'Open in Browser'",
            wraplength=400,
            justify=tk.CENTER
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def update_diagram(self, diagram_content: str):
        """
        Update the diagram with new content
        
        Args:
            diagram_content (str): Mermaid diagram content
        """
        if not diagram_content:
            return
        
        self.current_diagram = diagram_content
        
        # Update text view
        self.diagram_text.delete(1.0, tk.END)
        self.diagram_text.insert(tk.END, diagram_content)
        
        # Enable buttons
        self.open_button.configure(state=tk.NORMAL)
        self.copy_button.configure(state=tk.NORMAL)
        
        logger.debug("Diagram updated")
    
    def _copy_to_clipboard(self):
        """Copy the Mermaid syntax to clipboard"""
        self.clipboard_clear()
        self.clipboard_append(self.current_diagram)
        logger.debug("Diagram copied to clipboard")
    
    def _open_in_browser(self):
        """Open the diagram in a browser using Mermaid Live Editor"""
        if not self.current_diagram:
            return
        
        try:
            # Create a temporary HTML file with the Mermaid diagram
            # This gives a local preview without requiring internet
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
                html_content = self._create_mermaid_html(self.current_diagram)
                f.write(html_content)
                temp_path = f.name
            
            # Open the file in the default browser
            webbrowser.open('file://' + temp_path)
            
            # Schedule file cleanup for later (let browser load it first)
            threading.Timer(5.0, lambda: os.unlink(temp_path) if os.path.exists(temp_path) else None).start()
            
            logger.debug(f"Opened diagram in browser: {temp_path}")
        except Exception as e:
            logger.error(f"Error opening browser: {str(e)}")
    
    def _create_mermaid_html(self, mermaid_syntax: str) -> str:
        """
        Create HTML content with embedded Mermaid diagram
        
        Args:
            mermaid_syntax (str): Mermaid diagram syntax
            
        Returns:
            str: HTML content
        """
        # Escape any special characters for use in JavaScript
        escaped_syntax = mermaid_syntax.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5 Whys Analysis Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .mermaid {{ 
            margin: 20px auto;
            max-width: 1200px;
            overflow: auto;
        }}
        h1 {{ text-align: center; color: #333; }}
        .container {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            padding: 20px;
            margin: 20px auto;
            max-width: 1200px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 0.8em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>5 Whys Analysis Diagram</h1>
        <div class="mermaid">
{escaped_syntax}
        </div>
    </div>
    <div class="footer">
        Generated by 5 Whys Root Cause Analysis Tool
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>
"""
        return html
    
    def export_diagram_html(self, filepath: str) -> bool:
        """
        Export the current diagram as HTML
        
        Args:
            filepath (str): Path to save the HTML file
            
        Returns:
            bool: True if export succeeded, False otherwise
        """
        if not self.current_diagram:
            return False
            
        try:
            html_content = self._create_mermaid_html(self.current_diagram)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            logger.info(f"Exported diagram to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error exporting diagram: {str(e)}")
            return False
    
    def get_current_diagram(self) -> str:
        """
        Get the current diagram content
        
        Returns:
            str: Current diagram content
        """
        return self.current_diagram