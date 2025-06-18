#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI components for the fitness instructor voiceover application.

Contains classes for creating the GUI tabs and handling user interactions.
"""

import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import List
import re

# Import core components to extend/override
from core.gui_components import BaseTab

logger = logging.getLogger('fitness_podcaster')


class FitnessInputTab(BaseTab):
    """Input tab for selecting fitness content files and target audience."""
    
    def __init__(self, parent: ttk.Frame, main_gui):
        super().__init__(parent, main_gui)
        
        # Header
        header = ttk.Label(self.frame, text="Input Content and Settings", style="Header.TLabel")
        header.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        file_frame = ttk.LabelFrame(self.frame, text="Content Files")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.files_list = tk.Listbox(file_frame, selectmode=tk.EXTENDED, height=10)
        self.files_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.files_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.files_list.config(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Add Files", command=self.add_files)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_files)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Target learner
        target_frame = ttk.LabelFrame(self.frame, text="Target Audience")
        target_frame.pack(fill=tk.X, pady=10)
        
        self.target_var = tk.StringVar()
        
        # Get available profiles
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
            self.target_var.set("Adult learners at any fitness level")  # Fallback default
        
        # Create dropdown menu with learner profiles
        profile_label = ttk.Label(target_frame, text="Select target learner profile:")
        profile_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        profile_dropdown = ttk.Combobox(target_frame, textvariable=self.target_var, values=profile_names, width=40)
        profile_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Custom entry option
        custom_frame = ttk.Frame(target_frame)
        custom_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        custom_label = ttk.Label(custom_frame, text="Or enter custom target audience:")
        custom_label.pack(side=tk.LEFT, padx=5)
        
        self.custom_entry = ttk.Entry(custom_frame, width=40)
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        
        # Word limit setting
        limit_frame = ttk.Frame(target_frame)
        limit_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        limit_label = ttk.Label(limit_frame, text="Word limit for script:")
        limit_label.pack(side=tk.LEFT, padx=5)
        
        self.word_limit_var = tk.StringVar()
        self.word_limit_var.set(str(self.main_gui.generator.word_limit))  # Default from generator
        
        self.word_limit_entry = ttk.Entry(limit_frame, width=10, textvariable=self.word_limit_var)
        self.word_limit_entry.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # IMPORTANT: Store the button as an instance variable so we can access it later
        self.generate_button = ttk.Button(btn_frame, text="Generate Fitness Script", command=self.generate_script)
        self.generate_button.pack(side=tk.RIGHT, padx=5)
    
    def add_files(self):
        """Add files to the list."""
        files = self.main_gui.generator.select_files()
        if files:
            for file in files:
                self.files_list.insert(tk.END, file)
            self.main_gui.status_var.set(f"Added {len(files)} file(s)")
    
    def remove_files(self):
        """Remove selected files from the list."""
        selected = self.files_list.curselection()
        if not selected:
            return
        
        # Remove in reverse order to avoid index shifting
        for index in sorted(selected, reverse=True):
            self.files_list.delete(index)
        
        self.main_gui.status_var.set(f"Removed {len(selected)} file(s)")
    
    def generate_script(self):
        """Generate the fitness instruction script."""
        self.main_gui._generate_script()
        
    def get_selected_files(self) -> List[str]:
        """Get the list of selected files."""
        return [self.files_list.get(i) for i in range(self.files_list.size())]
    
    def get_target_learner(self) -> str:
        """Get the selected target learner profile or custom entry."""
        custom_entry = self.custom_entry.get().strip()
        if custom_entry:
            return custom_entry
        return self.target_var.get()
    
    def get_word_limit(self) -> int:
        """Get the word limit for script generation."""
        try:
            return int(self.word_limit_var.get())
        except ValueError:
            # If invalid input, return default
            return self.main_gui.generator.word_limit


class FitnessScriptTab(BaseTab):
    """Script tab for editing the generated fitness instruction script."""
    
    def __init__(self, parent: ttk.Frame, main_gui):
        super().__init__(parent, main_gui)
        
        # Header and instructions
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        header = ttk.Label(header_frame, text="Generated Fitness Instruction Script", style="Header.TLabel")
        header.pack(side=tk.LEFT, pady=(0, 5))
        
        # Instructions for editing
        instructions_frame = ttk.Frame(self.frame)
        instructions_frame.pack(fill=tk.X, pady=(0, 10))
        
        instructions = ttk.Label(instructions_frame, 
                               text="You can edit this script before converting it to audio. Add [pause] for breaks and [emphasis] for emphasis.",
                               wraplength=600)
        instructions.pack(side=tk.LEFT, pady=(0, 5), padx=5)
        
        # Script editor with line numbers and syntax highlighting
        editor_frame = ttk.LabelFrame(self.frame, text="Script Editor")
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.script_editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, width=80, height=20,
                                                     font=("Consolas", 10))
        self.script_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add some basic text formatting options
        format_frame = ttk.Frame(self.frame)
        format_frame.pack(fill=tk.X, pady=(5, 10))
        
        # Character counter
        self.char_count_var = tk.StringVar()
        self.char_count_var.set("Characters: 0 | Words: 0")
        char_count_label = ttk.Label(format_frame, textvariable=self.char_count_var)
        char_count_label.pack(side=tk.LEFT, padx=5)
        
        # Format tools for fitness instructions
        ttk.Button(format_frame, text="Add Rep Counter", 
                  command=self._insert_rep_counter).pack(side=tk.RIGHT, padx=5)
        ttk.Button(format_frame, text="Add [emphasis strong]", 
                  command=lambda: self._insert_emphasis("strong")).pack(side=tk.RIGHT, padx=5)
        ttk.Button(format_frame, text="Add [emphasis]", 
                  command=lambda: self._insert_emphasis()).pack(side=tk.RIGHT, padx=5)
        ttk.Button(format_frame, text="Add [pause 2s]", 
                  command=lambda: self._insert_pause("2s")).pack(side=tk.RIGHT, padx=5)
        ttk.Button(format_frame, text="Add [pause]", 
                  command=lambda: self._insert_pause()).pack(side=tk.RIGHT, padx=5)
        
        # Action buttons 
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="« Back to Input", 
                   command=lambda: self.main_gui.notebook.select(0)).pack(side=tk.LEFT)
                   
        # Save/load buttons
        ttk.Button(btn_frame, text="Save Script", 
                  command=self._save_script).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Load Script", 
                  command=self._load_script).pack(side=tk.LEFT, padx=5)
                  
        # Validate before generating audio
        ttk.Button(btn_frame, text="Validate Script", 
                  command=self._validate_script).pack(side=tk.RIGHT, padx=10)
        
        # IMPORTANT: Store the button as an instance variable so we can access it later
        self.convert_button = ttk.Button(btn_frame, text="Generate Audio »", 
                   command=self.convert_to_audio)
        self.convert_button.pack(side=tk.RIGHT)
                   
        # Bind events
        self.script_editor.bind("<KeyRelease>", self._update_counts)
    
    def update_script(self, script: str) -> None:
        """Update the script editor with generated content."""
        self.script_editor.delete(1.0, tk.END)
        self.script_editor.insert(tk.END, script)
        self._update_counts()
    
    def get_script(self) -> str:
        """Get the current script content."""
        return self.script_editor.get(1.0, tk.END)
    
    def convert_to_audio(self) -> None:
        """Convert the script to audio."""
        self.main_gui._convert_to_audio()
        
    def _update_counts(self, event=None) -> None:
        """Update character and word counts."""
        text = self.script_editor.get(1.0, tk.END)
        char_count = len(text) - 1  # Subtract 1 for the trailing newline
        word_count = len(text.split())
        self.char_count_var.set(f"Characters: {char_count} | Words: {word_count}")
    
    def _insert_rep_counter(self) -> None:
        """Insert rep counter at cursor position."""
        try:
            # Get current position
            current_pos = self.script_editor.index(tk.INSERT)
            line, col = map(int, current_pos.split('.'))
            
            # If not at the beginning of a line, insert a newline first
            if col > 0:
                self.script_editor.insert(tk.INSERT, "\n\n")
                
            # Insert rep counter template
            self.script_editor.insert(tk.INSERT, "One... Two... Three... Four... Five... Six... Seven... Eight...")
            self._update_counts()
        except Exception as e:
            logger.error(f"Error inserting rep counter: {str(e)}")
            
    def _insert_emphasis(self, level: str = "moderate") -> None:
        """Insert emphasis tags around selected text or at cursor."""
        try:
            # Check if there's a selection
            try:
                selected_text = self.script_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.script_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                if level != "moderate":
                    self.script_editor.insert(tk.INSERT, f"[emphasis {level}]{selected_text}[/emphasis]")
                else:
                    self.script_editor.insert(tk.INSERT, f"[emphasis]{selected_text}[/emphasis]")
            except tk.TclError:  # No selection
                if level != "moderate":
                    self.script_editor.insert(tk.INSERT, f"[emphasis {level}][/emphasis]")
                    # Move cursor back to between tags
                    current_pos = self.script_editor.index(tk.INSERT)
                    self.script_editor.mark_set(tk.INSERT, f"{current_pos}-11c")
                else:
                    self.script_editor.insert(tk.INSERT, "[emphasis][/emphasis]")
                    # Move cursor back to between tags
                    current_pos = self.script_editor.index(tk.INSERT)
                    self.script_editor.mark_set(tk.INSERT, f"{current_pos}-11c")
            self._update_counts()
        except Exception as e:
            logger.error(f"Error inserting emphasis: {str(e)}")
            
    def _insert_pause(self, duration: str = "") -> None:
        """Insert pause tag with optional duration at cursor position."""
        try:
            if duration:
                self.script_editor.insert(tk.INSERT, f"[pause {duration}]")
            else:
                self.script_editor.insert(tk.INSERT, "[pause]")
            self._update_counts()
        except Exception as e:
            logger.error(f"Error inserting pause: {str(e)}")
            
    def _save_script(self) -> None:
        """Save script to file."""
        try:
            from tkinter import filedialog
            script = self.get_script()
            if not script.strip():
                messagebox.showwarning("Empty Script", "There is no script to save.")
                return
                
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Fitness Instruction Script"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(script)
                messagebox.showinfo("Success", f"Script saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving script: {str(e)}")
            messagebox.showerror("Error", f"Could not save script: {str(e)}")
            
    def _load_script(self) -> None:
        """Load script from file."""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Load Fitness Instruction Script"
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    script = f.read()
                self.update_script(script)
                messagebox.showinfo("Success", f"Script loaded from {file_path}")
        except Exception as e:
            logger.error(f"Error loading script: {str(e)}")
            messagebox.showerror("Error", f"Could not load script: {str(e)}")
            
    def _validate_script(self) -> None:
        """Validate the fitness instruction script format."""
        try:
            script = self.get_script()
            
            # Basic validation
            if not script.strip():
                messagebox.showwarning("Empty Script", "The script is empty.")
                return
            
            # Check for pause markers
            pause_count = script.count("[pause]")
            variable_pause_count = len(re.findall(r"\[pause [^\]]+\]", script))
            total_pauses = pause_count + variable_pause_count
            
            # Check for emphasis markers
            emphasis_count = len(re.findall(r"\[emphasis\].*?\[\/emphasis\]|\[emphasis\].*?\]", script))
            strong_emphasis_count = len(re.findall(r"\[emphasis strong\].*?\[\/emphasis\]|\[emphasis strong\].*?\]", script))
            
            # Check for rep counting
            rep_count_patterns = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
            rep_counter_present = any(re.search(fr"\b{pattern}\b", script) for pattern in rep_count_patterns)
            
            # Word count check  
            words = re.findall(r'\b\w+\b', script)
            word_count = len(words)
            
            if word_count < 400 or word_count > 600:
                messagebox.showwarning("Word Count", 
                                    f"Script has {word_count} words. Recommended range is 400-600 words.")
                return
            
            # Check if the script has proper instruction formatting
            sections = re.split(r'\n\s*\n+', script)
            has_clear_sections = len(sections) >= 3
            
            if not has_clear_sections:
                messagebox.showwarning("Format Warning", 
                                     "Script should have clear sections separated by blank lines.")
                return
                
            if total_pauses < 3:
                messagebox.showwarning("Format Warning", 
                                     f"Script only has {total_pauses} pause markers. Consider adding more for better pacing.")
                return
                
            if not rep_counter_present:
                messagebox.showwarning("Format Warning", 
                                     "No rep counting detected. Fitness instructions typically include counted repetitions.")
                return
            
            # If all checks pass
            messagebox.showinfo("Validation Passed", 
                             f"Script format looks good! Word count: {word_count}\n" +
                             f"Pauses: {total_pauses} ({variable_pause_count} variable-length)\n" +
                             f"Emphasis markers: {emphasis_count} (plus {strong_emphasis_count} strong)")
                
        except Exception as e:
            logger.error(f"Error validating script: {str(e)}")
            messagebox.showerror("Error", f"Could not validate script: {str(e)}")
