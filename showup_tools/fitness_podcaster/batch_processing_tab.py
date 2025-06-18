#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Batch processing tab module for the fitness instructor voiceover application.

Provides a GUI interface for batch processing multiple markdown files.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess

# Import core components
from core.gui_components import BaseTab

# Import the markdown processor
from fitness_podcaster.markdown_processor import batch_process_directory, pause_processing, resume_processing, cancel_processing


class BatchProcessingTab(BaseTab):
    """Tab for batch processing of markdown files."""
    
    def __init__(self, parent: ttk.Frame, main_gui):
        super().__init__(parent, main_gui)
        
        # Header
        header = ttk.Label(self.frame, text="Batch Processing", style="Header.TLabel")
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Directory selection section
        # Input directory
        input_dir_frame = ttk.LabelFrame(self.frame, text="Input Directory (Markdown Files)")
        input_dir_frame.pack(fill=tk.X, pady=10)
        
        self.input_dir_var = tk.StringVar()
        input_dir_entry = ttk.Entry(input_dir_frame, textvariable=self.input_dir_var, width=50)
        input_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        browse_input_btn = ttk.Button(input_dir_frame, text="Browse...", command=self.browse_input_dir)
        browse_input_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Output directory
        output_dir_frame = ttk.LabelFrame(self.frame, text="Output Directory (Audio Files)")
        output_dir_frame.pack(fill=tk.X, pady=10)
        
        self.output_dir_var = tk.StringVar()
        # Default to the standard output directory
        default_output = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "generated_fitness_audio")
        self.output_dir_var.set(default_output)
        
        output_dir_entry = ttk.Entry(output_dir_frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        browse_output_btn = ttk.Button(output_dir_frame, text="Browse...", command=self.browse_output_dir)
        browse_output_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Target audience & word limit
        settings_frame = ttk.LabelFrame(self.frame, text="Processing Settings")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Target audience - using the same profiles as the input tab
        audience_frame = ttk.Frame(settings_frame)
        audience_frame.pack(fill=tk.X, padx=5, pady=5)
        
        audience_label = ttk.Label(audience_frame, text="Select target learner profile:")
        audience_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.target_var = tk.StringVar()
        
        # Get available profiles from the generator
        profile_names = self.main_gui.generator.get_profile_names()
        
        # Set default to Physical Education if available
        physical_ed_profile_name = None
        for profile_name in profile_names:
            if "Physical Education" in profile_name or "Fitness" in profile_name:
                physical_ed_profile_name = profile_name
                break
        
        if physical_ed_profile_name:
            self.target_var.set(physical_ed_profile_name)  # Default to Physical Education profile
        elif profile_names:
            self.target_var.set(profile_names[0])  # Default to first profile
        else:
            self.target_var.set("Adult fitness enthusiasts")  # Fallback default
        
        # Create dropdown menu with learner profiles
        profile_dropdown = ttk.Combobox(audience_frame, textvariable=self.target_var, values=profile_names, width=40)
        profile_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Custom entry option
        custom_frame = ttk.Frame(audience_frame)
        custom_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        custom_label = ttk.Label(custom_frame, text="Or enter custom target audience:")
        custom_label.pack(side=tk.LEFT, padx=5)
        
        self.custom_entry = ttk.Entry(custom_frame, width=40)
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        
        # Word limit
        word_limit_frame = ttk.Frame(settings_frame)
        word_limit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        word_limit_label = ttk.Label(word_limit_frame, text="Word Limit:")
        word_limit_label.pack(side=tk.LEFT, padx=5)
        
        self.word_limit_var = tk.StringVar()
        self.word_limit_var.set(str(self.main_gui.generator.word_limit))
        word_limit_entry = ttk.Entry(word_limit_frame, textvariable=self.word_limit_var, width=10)
        word_limit_entry.pack(side=tk.LEFT, padx=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.frame, text="Processing Progress")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, 
                                          length=100, mode='determinate', 
                                          variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Status display
        self.status_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=15)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Left side - navigation
        nav_frame = ttk.Frame(btn_frame)
        nav_frame.pack(side=tk.LEFT)
        
        ttk.Button(nav_frame, text="« Back to Audio", 
                  command=lambda: self.main_gui.notebook.select(2)).pack(side=tk.LEFT, padx=5)
        
        # Open output directory button
        ttk.Button(nav_frame, text="Open Output Directory", 
                  command=self.open_output_directory).pack(side=tk.LEFT, padx=5)
        
        # Right side - processing controls
        control_frame = ttk.Frame(btn_frame)
        control_frame.pack(side=tk.RIGHT)
        
        # Process button
        self.process_button = ttk.Button(control_frame, text="Start Processing", 
                                       command=self.start_batch_processing)
        self.process_button.pack(side=tk.RIGHT, padx=5)
        
        # Pause/Resume buttons
        self.pause_button = ttk.Button(control_frame, text="Pause", 
                                     command=self.pause_processing, state="disabled")
        self.pause_button.pack(side=tk.RIGHT, padx=5)
        
        self.resume_button = ttk.Button(control_frame, text="Resume", 
                                      command=self.resume_processing, state="disabled")
        self.resume_button.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        self.cancel_button = ttk.Button(control_frame, text="Cancel", 
                                      command=self.cancel_processing, state="disabled")
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Processing state flags
        self.is_processing = False
        self.is_paused = False
    
    def browse_input_dir(self):
        """Browse for input directory containing markdown files."""
        directory = filedialog.askdirectory(title="Select Input Directory (Markdown Files)")
        if directory:
            self.input_dir_var.set(directory)
            self.update_status(f"Input directory set to: {directory}")
    
    def browse_output_dir(self):
        """Browse for output directory for audio files."""
        directory = filedialog.askdirectory(title="Select Output Directory (Audio Files)")
        if directory:
            self.output_dir_var.set(directory)
            self.update_status(f"Output directory set to: {directory}")
    
    def open_output_directory(self):
        """Open the output directory in file explorer."""
        output_dir = self.output_dir_var.get()
        if not output_dir:
            messagebox.showwarning("No Directory", "Please specify an output directory first.")
            return
            
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {str(e)}")
                return
        
        # Open the directory using appropriate platform command
        try:
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':
                subprocess.call(['open', output_dir])
            else:  # Assume Linux or other Unix
                subprocess.call(['xdg-open', output_dir])
            
            self.update_status(f"Opened output directory: {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open output directory: {str(e)}")
    
    def update_status(self, message):
        """Update the status text display."""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)  # Scroll to the end
    
    def update_file_status(self, file_path, success, message):
        """Update the status display for a specific file."""
        if file_path is None:
            # This is a general status message, not a file-specific one
            self.update_status(message)
            return
            
        basename = os.path.basename(file_path)
        status = "✅ Success" if success else "❌ Failed"
        self.update_status(f"{basename}: {status} - {message}")
    
    def update_progress(self, current, total):
        """Update the progress bar."""
        if total > 0:
            progress = (current / total) * 100
            self.progress_var.set(progress)
            self.main_gui.status_var.set(f"Batch processing: {current}/{total} files")
    
    def get_target_learner(self) -> str:
        """Get the selected target learner profile or custom entry."""
        custom_entry = self.custom_entry.get().strip()
        if custom_entry:
            return custom_entry
        return self.target_var.get()
    
    def start_batch_processing(self):
        """Start batch processing in a separate thread."""
        # Check if directories are specified
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        
        if not input_dir:
            messagebox.showwarning("Input Directory", "Please select an input directory containing markdown files.")
            return
            
        if not os.path.exists(input_dir):
            messagebox.showwarning("Input Directory", f"The input directory does not exist: {input_dir}")
            return
            
        if not output_dir:
            messagebox.showwarning("Output Directory", "Please specify an output directory for the generated audio files.")
            return
        
        # Get the word limit
        try:
            word_limit = int(self.word_limit_var.get())
            if word_limit <= 0:
                raise ValueError("Word limit must be positive")
        except ValueError:
            messagebox.showwarning("Word Limit", "Please enter a valid positive number for the word limit.")
            return
        
        # Target audience - use the same method as the input tab
        target_audience = self.get_target_learner()
        if not target_audience:
            target_audience = "Adult fitness enthusiasts"  # Fallback default
        
        # Reset progress and status
        self.progress_var.set(0)
        self.status_text.delete(1.0, tk.END)
        self.update_status(f"Starting batch processing:\n- Input: {input_dir}\n- Output: {output_dir}\n- Target audience: {target_audience}\n- Word limit: {word_limit}\n")
        
        # Update button states
        self.process_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        
        # Set processing flags
        self.is_processing = True
        self.is_paused = False
        
        # Start processing in a separate thread
        thread = threading.Thread(
            target=self.batch_process_thread,
            args=(input_dir, output_dir, target_audience, word_limit)
        )
        thread.daemon = True
        thread.start()
    
    def batch_process_thread(self, input_dir, output_dir, target_audience, word_limit):
        """Thread function for batch processing."""
        try:
            # Process the directory
            results = batch_process_directory(
                input_dir, 
                output_dir, 
                target_audience, 
                word_limit,
                progress_callback=lambda current, total: self.main_gui.root.after(0, lambda: self.update_progress(current, total)),
                status_callback=lambda file_path, success, message: self.main_gui.root.after(0, lambda: self.update_file_status(file_path, success, message))
            )
            
            # Update UI with results in the main thread
            self.main_gui.root.after(0, lambda: self.update_results(results))
            
        except Exception as e:
            error_msg = str(e)
            self.main_gui.root.after(0, lambda: self.update_status(f"Error during batch processing: {error_msg}"))
        finally:
            # Reset button states in the main thread
            self.main_gui.root.after(0, lambda: self.reset_controls())
    
    def update_results(self, results):
        """Update the UI with batch processing results."""
        successful_count = len(results.get("successful", []))
        failed_count = len(results.get("failed", []))
        total = successful_count + failed_count
        
        summary = f"\nBatch processing complete:\n- Total files: {total}\n- Successful: {successful_count}\n- Failed: {failed_count}\n"
        self.update_status(summary)
        
        if failed_count > 0:
            self.update_status("\nFailed files:")
            for file_path in results.get("failed", []):
                self.update_status(f"- {os.path.basename(file_path)}")
        
        self.main_gui.status_var.set(f"Batch processing complete: {successful_count}/{total} files successful")
    
    def pause_processing(self):
        """Pause batch processing."""
        pause_processing()
        self.is_paused = True
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="normal")
        self.update_status("Processing paused. Click Resume to continue.")
    
    def resume_processing(self):
        """Resume batch processing."""
        resume_processing()
        self.is_paused = False
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.update_status("Processing resumed.")
    
    def cancel_processing(self):
        """Cancel batch processing."""
        if messagebox.askyesno("Cancel Processing", "Are you sure you want to cancel the current batch processing?"):
            cancel_processing()
            self.update_status("Processing canceled.")
            self.pause_button.config(state="disabled")
            self.resume_button.config(state="disabled")
            self.cancel_button.config(state="disabled")
    
    def reset_controls(self):
        """Reset control buttons after processing."""
        self.is_processing = False
        self.is_paused = False
        self.process_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
