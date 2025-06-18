#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from ttkthemes import ThemedTk
from typing import Optional
from pathlib import Path
import threading
from datetime import datetime
import queue

# Import admin assistant components
from main import AdminAssistant
from config import DEFAULT_SCAN_DIR


class AdminAssistantGUI:
    """GUI for the Admin Assistant chatbot using Tkinter."""
    
    def __init__(self, root: ThemedTk) -> None:
        """Initialize the GUI.
        
        Args:
            root: ThemedTk root window
        """
        self.root = root
        self.root.title("Admin Assistant")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set up the message queue for thread-safe updates
        self.msg_queue: queue.Queue = queue.Queue()
        
        # Create the admin assistant
        self.scan_dir = Path(DEFAULT_SCAN_DIR)
        self.assistant: Optional[AdminAssistant] = None
        
        # Initialize UI
        self._init_ui()
        
        # Start message processing
        self.process_messages()
        
        # Initialize the assistant in the background
        self._init_assistant()
    
    def _init_assistant(self) -> None:
        """Initialize the admin assistant in a background thread."""
        def initialize() -> None:
            self.update_status("Initializing Admin Assistant...")
            try:
                self.assistant = AdminAssistant(self.scan_dir)
                self.update_status(f"Ready - Scanning directory: {self.scan_dir}")
                # Enable the input controls once initialized
                self.root.after(0, lambda: self.enable_controls(True))
            except Exception as e:
                error_msg = f"Error initializing Admin Assistant: {str(e)}"
                self.update_status(error_msg, "error")
                self.chat_display.configure(state="normal")
                self.chat_display.insert(tk.END, f"\n\nERROR: {error_msg}\n\n", "error")
                self.chat_display.configure(state="disabled")
                self.chat_display.see(tk.END)
        
        # Disable controls until initialization is complete
        self.enable_controls(False)
        
        # Start initialization in a background thread
        threading.Thread(target=initialize, daemon=True).start()
    
    def _init_ui(self) -> None:
        """Initialize the user interface components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top panel - directory selection and actions
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Directory selection
        dir_frame = ttk.LabelFrame(top_frame, text="Working Directory")
        dir_frame.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        self.dir_var = tk.StringVar(value=str(self.scan_dir))
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, width=40)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(top_frame)
        action_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        refresh_btn = ttk.Button(action_frame, text="Change Directory", command=self.change_directory)
        refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        organize_btn = ttk.Button(action_frame, text="Organize Files", command=self.organize_files)
        organize_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Chat display area
        chat_frame = ttk.LabelFrame(main_frame, text="Chat")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("TkDefaultFont", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.configure(state="disabled")
        
        # Chat input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        self.input_field = ttk.Entry(input_frame, font=("TkDefaultFont", 10))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", lambda event: self.send_message())
        
        send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Initializing...")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure text tags
        self.chat_display.tag_configure("user", foreground="#0000CC")
        self.chat_display.tag_configure("assistant", foreground="#006600")
        self.chat_display.tag_configure("system", foreground="#666666", font=("TkDefaultFont", 9, "italic"))
        self.chat_display.tag_configure("error", foreground="#CC0000")
        
        # Welcome message
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, "Welcome to Admin Assistant!\n", "system")
        self.chat_display.insert(tk.END, "I can help organize your files into appropriate folders.\n", "system")
        self.chat_display.insert(tk.END, "Type a message or click 'Organize Files' to begin.\n\n", "system")
        self.chat_display.configure(state="disabled")
    
    def enable_controls(self, enabled: bool = True) -> None:
        """Enable or disable input controls.
        
        Args:
            enabled: Whether to enable the controls
        """
        state = "normal" if enabled else "disabled"
        self.input_field.configure(state=state)
        
        # Find all buttons and update their state
        for widget in self.root.winfo_children():
            self._update_widget_state(widget, state)
    
    def _update_widget_state(self, widget: tk.Widget, state: str) -> None:
        """Recursively update the state of buttons in the widget hierarchy.
        
        Args:
            widget: The widget to update
            state: The state to set ("normal" or "disabled")
        """
        if isinstance(widget, ttk.Button):
            widget.configure(state=state)
        
        # Recursively process child widgets
        for child in widget.winfo_children():
            self._update_widget_state(child, state)
    
    def update_status(self, message: str, tag: str = "system") -> None:
        """Update the status bar with a message.
        
        Args:
            message: Status message to display
            tag: Text tag for styling
        """
        self.status_var.set(message)
        
        # Also log to chat if it's an important message
        if tag in ["error", "system"] and not message.startswith("Ready"):
            self.msg_queue.put((message, tag))
    
    def browse_directory(self) -> None:
        """Open a directory browser dialog."""
        directory = filedialog.askdirectory(initialdir=self.scan_dir)
        if directory:
            self.dir_var.set(directory)
    
    def change_directory(self) -> None:
        """Change the working directory for the assistant."""
        new_dir = Path(self.dir_var.get())
        if not new_dir.exists():
            self.update_status(f"Directory not found: {new_dir}", "error")
            return
        
        self.scan_dir = new_dir
        self.update_status(f"Changing directory to: {self.scan_dir}")
        
        # Reinitialize the assistant with the new directory
        self._init_assistant()
    
    def organize_files(self) -> None:
        """Organize files in the current directory."""
        if not self.assistant:
            self.update_status("Admin Assistant not ready yet. Please wait...", "error")
            return
        
        # Display user command
        self.display_message("Organize my files", "user")
        
        # Disable controls during processing
        self.enable_controls(False)
        
        # Run organization in a background thread
        def organize_task() -> None:
            try:
                response = self.assistant.process_message("Organize my files and folders")
                self.msg_queue.put((response, "assistant"))
                self.root.after(0, lambda: self.enable_controls(True))
            except Exception as e:
                error_msg = f"Error organizing files: {str(e)}"
                self.msg_queue.put((error_msg, "error"))
                self.root.after(0, lambda: self.enable_controls(True))
        
        threading.Thread(target=organize_task, daemon=True).start()
    
    def send_message(self) -> None:
        """Send a message to the assistant."""
        message = self.input_field.get().strip()
        if not message:
            return
        
        if not self.assistant:
            self.update_status("Admin Assistant not ready yet. Please wait...", "error")
            return
        
        # Clear the input field
        self.input_field.delete(0, tk.END)
        
        # Display user message
        self.display_message(message, "user")
        
        # Disable controls during processing
        self.enable_controls(False)
        
        # Process message in a background thread
        def process_message_task() -> None:
            try:
                response = self.assistant.process_message(message)
                self.msg_queue.put((response, "assistant"))
                self.root.after(0, lambda: self.enable_controls(True))
            except Exception as e:
                error_msg = f"Error processing message: {str(e)}"
                self.msg_queue.put((error_msg, "error"))
                self.root.after(0, lambda: self.enable_controls(True))
        
        threading.Thread(target=process_message_task, daemon=True).start()
    
    def display_message(self, message: str, sender: str) -> None:
        """Display a message in the chat area.
        
        Args:
            message: The message to display
            sender: Who sent the message ("user", "assistant", "system", "error")
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format the message based on sender
        if sender == "user":
            prefix = f"[{timestamp}] You: "
        elif sender == "assistant":
            prefix = f"[{timestamp}] Assistant: "
        elif sender == "error":
            prefix = f"[{timestamp}] ERROR: "
        else:  # system
            prefix = f"[{timestamp}] System: "
        
        # Add to the display
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, prefix, "system")
        self.chat_display.insert(tk.END, f"{message}\n\n", sender)
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)
    
    def process_messages(self) -> None:
        """Process messages from the queue and update the UI."""
        try:
            while not self.msg_queue.empty():
                message, tag = self.msg_queue.get_nowait()
                self.display_message(message, tag)
                self.msg_queue.task_done()
        except queue.Empty:
            pass
        finally:
            # Schedule to check again
            self.root.after(100, self.process_messages)


def main() -> None:
    """Main entry point for the GUI application."""
    # Use ThemedTk for better looking UI
    root = ThemedTk(theme="arc")  # Other good themes: 'breeze', 'equilux', 'arc'
    
    # Create the application
    app = AdminAssistantGUI(root)
    
    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
