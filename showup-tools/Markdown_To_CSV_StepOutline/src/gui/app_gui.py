#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tkinter GUI for Markdown to CSV Converter."""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import logging

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import ConfigManager
from src.utils.logging_utils import setup_logging
from src.core.api_handler import APIHandler
from src.core.markdown_converter import MarkdownToCSVConverter

logger = logging.getLogger("GUI")


class ConverterGUI:
    """GUI application for Markdown to CSV conversion.
    
    Provides a user-friendly interface for selecting input markdown files,
    output CSV destinations, and conversion options.
    """
    
    def __init__(self, root: tk.Tk):
        """Initialize the GUI application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Markdown to CSV Converter")
        self.root.geometry("700x600")
        self.root.minsize(650, 550)
        
        # Set application icon if available
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "resources", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            logger.warning(f"Could not set application icon: {str(e)}")
        
        # Load configuration
        self.config = ConfigManager()
        
        # Initialize API handler with better error reporting
        api_key = self.config.get_anthropic_api_key()
        self.api_handler = None
        self.ai_status_message = ""
        
        # Check for anthropic module availability first
        if not APIHandler.is_available_class():
            self.ai_status_message = "AI not available: anthropic module not installed"
            logger.warning(self.ai_status_message)
        elif not api_key:
            self.ai_status_message = "AI not available: No API key found"
            logger.warning(self.ai_status_message)
        else:
            # Try to initialize the API handler
            try:
                self.api_handler = APIHandler(api_key)
                if not self.api_handler.is_available():
                    self.ai_status_message = "AI not available: API client initialization failed"
                    logger.warning(self.ai_status_message)
                else:
                    self.ai_status_message = "AI enabled"
                    logger.info("AI client initialized successfully")
            except Exception as e:
                self.ai_status_message = f"AI not available: {str(e)}"
                logger.error(f"Error initializing API handler: {str(e)}")
        
        # Variables for file paths
        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()
        
        # Variables for options
        self.use_ai_var = tk.BooleanVar(value=bool(self.api_handler and self.api_handler.is_available()))
        self.conversion_method_var = tk.StringVar(value="hybrid")
        
        # Create the GUI layout
        self._create_widgets()
        
        # Status variables
        self.is_converting = False
        self.conversion_thread = None
    
    def _create_widgets(self) -> None:
        """Create and arrange GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
        self.style.configure('Subheader.TLabel', font=('Segoe UI', 12))
        
        # Header
        header = ttk.Label(main_frame, text="Markdown to CSV Converter", style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # Input file section
        input_frame = ttk.LabelFrame(main_frame, text="Input Markdown File", padding="10 10 10 10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_entry = ttk.Entry(input_frame, textvariable=self.input_file_var)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_input_btn = ttk.Button(input_frame, text="Browse", command=self._browse_input_file)
        browse_input_btn.pack(side=tk.RIGHT)
        
        # Output file section
        output_frame = ttk.LabelFrame(main_frame, text="Output CSV File", padding="10 10 10 10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_output_btn = ttk.Button(output_frame, text="Browse", command=self._browse_output_file)
        browse_output_btn.pack(side=tk.RIGHT)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options", padding="10 10 10 10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # AI options
        ai_frame = ttk.Frame(options_frame)
        ai_frame.pack(fill=tk.X, pady=(0, 5))
        
        ai_check = ttk.Checkbutton(ai_frame, text="Use AI for enhancement", variable=self.use_ai_var)
        ai_check.pack(side=tk.LEFT)
        
        # Disable AI checkbox if not available
        if not (self.api_handler and self.api_handler.is_available()):
            ai_check.state(['disabled'])
            # Show the specific reason why AI is not available
            status_color = "red" if "not available" in self.ai_status_message else "orange"
            ai_status = ttk.Label(ai_frame, text=self.ai_status_message, foreground=status_color)
            ai_status.pack(side=tk.LEFT, padx=(10, 0))
        else:
            ai_status = ttk.Label(ai_frame, text="AI enabled", foreground="green")
            ai_status.pack(side=tk.LEFT, padx=(10, 0))
        
        # Conversion method options
        method_frame = ttk.Frame(options_frame)
        method_frame.pack(fill=tk.X)
        
        ttk.Label(method_frame, text="Conversion Method:").pack(side=tk.LEFT)
        
        methods = [("Hybrid", "hybrid"), ("AI Driven", "ai_driven"), ("Rule Based", "rule_based")]
        for i, (text, value) in enumerate(methods):
            ttk.Radiobutton(method_frame, text=text, value=value, 
                            variable=self.conversion_method_var).pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10 10 10 10")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, wraplength=650)
        status_label.pack(fill=tk.X)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.convert_button = ttk.Button(buttons_frame, text="Convert", command=self._start_conversion)
        self.convert_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.root.destroy)
        cancel_button.pack(side=tk.RIGHT)
    
    def _browse_input_file(self) -> None:
        """Open a file dialog to select the input markdown file."""
        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_var.set(filename)
            
            # Auto-set output filename if not already set
            current_output = self.output_file_var.get()
            if not current_output:
                # Change extension to .csv
                base_path = os.path.splitext(filename)[0]
                self.output_file_var.set(f"{base_path}.csv")
    
    def _browse_output_file(self) -> None:
        """Open a file dialog to select the output CSV file."""
        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def _start_conversion(self) -> None:
        """Validate inputs and start the conversion process."""
        # Validate input file
        input_file = self.input_file_var.get()
        if not input_file or not os.path.isfile(input_file):
            messagebox.showerror("Error", "Please select a valid input markdown file.")
            return
        
        # Validate output file
        output_file = self.output_file_var.get()
        if not output_file:
            messagebox.showerror("Error", "Please specify an output CSV file.")
            return
        
        # Confirm if output file exists
        if os.path.exists(output_file):
            confirmed = messagebox.askyesno(
                "File Exists", 
                f"The file {output_file} already exists. Do you want to overwrite it?"
            )
            if not confirmed:
                return
        
        # Disable the convert button during conversion
        self.convert_button.state(['disabled'])
        self.is_converting = True
        self.progress_var.set(0)
        self.status_var.set("Starting conversion...")
        
        # Get conversion options
        use_ai = self.use_ai_var.get()
        conversion_method = self.conversion_method_var.get()
        
        # Start conversion in a separate thread to keep UI responsive
        self.conversion_thread = threading.Thread(
            target=self._run_conversion,
            args=(input_file, output_file, use_ai, conversion_method)
        )
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
    
    def _run_conversion(self, input_file: str, output_file: str, 
                        use_ai: bool, conversion_method: str) -> None:
        """Run the conversion process in a separate thread.
        
        Args:
            input_file: Path to the input markdown file
            output_file: Path where the output CSV file will be saved
            use_ai: Whether to use AI enhancement
            conversion_method: Conversion method to use
        """
        try:
            # Create converter
            converter = MarkdownToCSVConverter(
                input_file=input_file,
                output_file=output_file,
                api_handler=self.api_handler if use_ai else None
            )
            
            # Run conversion with progress updates
            result = converter.convert(progress_callback=self._update_progress)
            
            # Update UI with results
            if result:
                self.status_var.set("Conversion completed successfully!")
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success", "Markdown file has been successfully converted to CSV."
                ))
            else:
                self.status_var.set("Conversion failed. See log for details.")
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", "Failed to convert markdown file. Check the log for details."
                ))
                
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        finally:
            # Re-enable convert button
            self.is_converting = False
            self.root.after(0, lambda: self.convert_button.state(['!disabled']))
    
    def _update_progress(self, progress_value: float, message: str) -> None:
        """Update progress bar and status message from the worker thread.
        
        Args:
            progress_value: Progress value between 0 and 1
            message: Status message to display
        """
        # Schedule UI updates on the main thread
        self.root.after(0, lambda: self._update_progress_ui(progress_value, message))
    
    def _update_progress_ui(self, progress_value: float, message: str) -> None:
        """Update progress UI elements on the main thread.
        
        Args:
            progress_value: Progress value between 0 and 1
            message: Status message to display
        """
        self.progress_var.set(progress_value * 100)  # Convert to percentage
        self.status_var.set(message)


def run_gui() -> None:
    """Run the GUI application."""
    # Setup logging
    setup_logging()
    
    # Create root window
    root = tk.Tk()
    
    # Create and run application
    app = ConverterGUI(root)
    
    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    run_gui()
