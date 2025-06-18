"""
Main Window for the 5 Whys Root Cause Analysis Chatbot

Integrates all UI components and manages interaction with the analysis engine.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import logging
import os
import threading

from .chat_panel import ChatPanel
from .thinking_panel import ThinkingPanel
from .diagram_panel import DiagramPanel
from ..five_whys_engine import FiveWhysEngine
from ..mermaid_generator import MermaidGenerator
from ..utils.file_manager import FileManager
from ..utils.config import Config

# Get logger
logger = logging.getLogger("main_window")

class MainWindow:
    """Main application window for the 5 Whys analyzer"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window
        
        Args:
            root (tk.Tk): Root Tkinter window
        """
        self.root = root
        self.root.title("5 Whys Root Cause Analysis")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure style
        self._configure_style()
        
        # Components
        self.engine = FiveWhysEngine()
        self.diagram_generator = MermaidGenerator()
        self.file_manager = FileManager()
        self.config = Config()
        
        # Create UI elements
        self._create_widgets()
        
        # Set up event handlers
        self._setup_events()
        
        # Analysis state
        self.analysis_running = False
        self.current_analysis_data = {}
        
        # Validate setup
        self._validate_setup()
    
    def _configure_style(self):
        """Configure application style"""
        style = ttk.Style()
        
        # Use a modern theme if available
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        
        # Configure styles for various elements
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("TLabel", font=("Segoe UI", 9), background="#f0f0f0")
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TNotebook.Tab", font=("Segoe UI", 9))
    
    def _create_widgets(self):
        """Create and arrange window widgets"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for input
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Problem input frame
        input_frame = ttk.LabelFrame(top_frame, text="Analysis Input")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Input grid
        input_grid = ttk.Frame(input_frame)
        input_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Job context
        ttk.Label(input_grid, text="Job Context:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.job_context_text = scrolledtext.ScrolledText(
            input_grid,
            wrap=tk.WORD,
            width=60,
            height=3,
            font=("Segoe UI", 9)
        )
        self.job_context_text.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Initial problem
        ttk.Label(input_grid, text="Initial Problem:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.problem_text = scrolledtext.ScrolledText(
            input_grid,
            wrap=tk.WORD,
            width=60,
            height=3,
            font=("Segoe UI", 9)
        )
        self.problem_text.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Controls
        control_frame = ttk.Frame(input_grid)
        control_frame.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.start_button = ttk.Button(
            control_frame,
            text="Start Analysis",
            command=self._start_analysis,
            width=15
        )
        self.start_button.pack(side=tk.RIGHT, padx=5)
        
        # Configure grid column weights
        input_grid.columnconfigure(1, weight=1)
        
        # Paned window for main content
        self.main_paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (conversation)
        self.left_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_panel, weight=1)
        
        # Chat panel
        self.chat_panel = ChatPanel(self.left_panel)
        self.chat_panel.pack(fill=tk.BOTH, expand=True)
        
        # Right panel (tabs for thinking and diagram)
        self.right_panel = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.right_panel, weight=1)
        
        # Thinking panel
        self.thinking_panel = ThinkingPanel(self.right_panel)
        self.right_panel.add(self.thinking_panel, text="Claude's Thinking")
        
        # Diagram panel
        self.diagram_panel = DiagramPanel(self.right_panel)
        self.right_panel.add(self.diagram_panel, text="Analysis Diagram")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_container, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Configure menu
        self._setup_menu()
    
    def _setup_menu(self):
        """Set up the application menu"""
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Analysis", command=self._new_analysis)
        file_menu.add_command(label="Open Analysis...", command=self._open_analysis)
        file_menu.add_command(label="Save Analysis...", command=self._save_analysis)
        file_menu.add_separator()
        file_menu.add_command(label="Export as Markdown...", command=self._export_markdown)
        file_menu.add_command(label="Export Diagram as HTML...", command=self._export_diagram)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy Diagram", command=lambda: self.diagram_panel._copy_to_clipboard())
        edit_menu.add_command(label="Clear Chat", command=lambda: self.chat_panel.clear_chat())
        edit_menu.add_command(label="Clear Thinking", command=lambda: self.thinking_panel.clear_content())
        
        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Chat Panel", command=lambda: self._focus_panel("chat"))
        view_menu.add_command(label="Thinking Panel", command=lambda: self._focus_panel("thinking"))
        view_menu.add_command(label="Diagram Panel", command=lambda: self._focus_panel("diagram"))
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _setup_events(self):
        """Set up event handlers"""
        # Set chat panel callback
        self.chat_panel.set_on_send_callback(self._on_answer_submitted)
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _validate_setup(self):
        """Validate application setup"""
        # Check if Claude API key is configured
        is_valid, message = self.engine.validate_setup()
        if not is_valid:
            self.status_var.set(message)
            messagebox.warning("Setup Warning", message)
    
    def _focus_panel(self, panel_name: str):
        """
        Focus on a specific panel
        
        Args:
            panel_name (str): Panel to focus ("chat", "thinking", "diagram")
        """
        if panel_name == "chat":
            self.chat_panel.focus_set()
        elif panel_name == "thinking":
            self.right_panel.select(0)  # Select thinking tab
            self.thinking_panel.focus_set()
        elif panel_name == "diagram":
            self.right_panel.select(1)  # Select diagram tab
            self.diagram_panel.focus_set()
    
    def _new_analysis(self):
        """Start a new analysis"""
        # Check if an analysis is running
        if self.analysis_running:
            if not messagebox.askyesno("New Analysis", 
                                       "An analysis is currently in progress. Are you sure you want to start a new one?"):
                return
        
        # Reset state
        self.analysis_running = False
        self.current_analysis_data = {}
        
        # Clear UI
        self.job_context_text.delete(1.0, tk.END)
        self.problem_text.delete(1.0, tk.END)
        self.chat_panel.clear_chat()
        self.thinking_panel.clear_content()
        self.diagram_panel.update_diagram("")
        
        # Enable input
        self.start_button.configure(state=tk.NORMAL)
        self.job_context_text.configure(state=tk.NORMAL)
        self.problem_text.configure(state=tk.NORMAL)
        
        self.status_var.set("Ready for new analysis")
    
    def _open_analysis(self):
        """Open a saved analysis"""
        # Show file dialog
        filepath = filedialog.askopenfilename(
            title="Open Analysis",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialdir=self.file_manager.history_dir
        )
        
        if not filepath:
            return
        
        # Load analysis
        analysis_data = self.file_manager.load_analysis(filepath)
        
        if not analysis_data:
            messagebox.showerror("Error", "Failed to load analysis file")
            return
        
        # Reset current state
        self._new_analysis()
        
        # Populate fields
        job_context = analysis_data.get("job_context", "")
        initial_problem = analysis_data.get("initial_problem", "")
        questions = analysis_data.get("questions", [])
        answers = analysis_data.get("answers", [])
        thinking_history = analysis_data.get("thinking_history", [])
        root_cause = analysis_data.get("root_cause", "")
        
        self.job_context_text.delete(1.0, tk.END)
        self.job_context_text.insert(tk.END, job_context)
        
        self.problem_text.delete(1.0, tk.END)
        self.problem_text.insert(tk.END, initial_problem)
        
        # Add messages to chat
        if job_context:
            self.chat_panel.add_message("job_context", job_context)
        if initial_problem:
            self.chat_panel.add_message("problem", initial_problem)
        
        # Add questions and answers
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            self.chat_panel.add_message("question", (i, question))
            self.chat_panel.add_message("answer", answer)
        
        # Add root cause if present
        if root_cause:
            self.chat_panel.add_message("root_cause", root_cause)
        
        # Update thinking panel
        if thinking_history and isinstance(thinking_history, list):
            self.thinking_panel.set_content("\n\n".join(thinking_history))
        
        # Update diagram
        self._update_diagram()
        
        # Store current analysis data
        self.current_analysis_data = analysis_data.copy()
        
        # Mark as complete if it has a root cause
        self.analysis_running = False if root_cause else True
        
        # Update status
        self.status_var.set(f"Loaded analysis from {os.path.basename(filepath)}")
    
    def _save_analysis(self):
        """Save the current analysis"""
        # Ensure we have data to save
        if not self.job_context_text.get(1.0, tk.END).strip() or not self.problem_text.get(1.0, tk.END).strip():
            messagebox.showinfo("Information", "No analysis data to save")
            return
        
        # Get all analysis data
        analysis_data = {
            "job_context": self.job_context_text.get(1.0, tk.END).strip(),
            "initial_problem": self.problem_text.get(1.0, tk.END).strip(),
            "questions": [q["content"] for q in self.chat_panel.get_messages() if q["type"] == "question"],
            "answers": [a["content"] for a in self.chat_panel.get_messages() if a["type"] == "answer"],
            "root_cause": self.current_analysis_data.get("root_cause", ""),
            "thinking_history": self.current_analysis_data.get("thinking_history", []),
            "mermaid_diagram": self.diagram_panel.get_current_diagram()
        }
        
        # Show file dialog
        filepath = filedialog.asksaveasfilename(
            title="Save Analysis",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialdir=self.file_manager.history_dir,
            defaultextension=".json"
        )
        
        if not filepath:
            return
        
        # Save analysis
        saved_path = self.file_manager.save_analysis(analysis_data, filepath)
        
        if saved_path:
            self.status_var.set(f"Analysis saved to {os.path.basename(saved_path)}")
        else:
            messagebox.showerror("Error", "Failed to save analysis")
    
    def _export_markdown(self):
        """Export analysis as Markdown"""
        # Ensure we have data to export
        if not self.job_context_text.get(1.0, tk.END).strip() or not self.problem_text.get(1.0, tk.END).strip():
            messagebox.showinfo("Information", "No analysis data to export")
            return
        
        # Get all analysis data
        analysis_data = {
            "job_context": self.job_context_text.get(1.0, tk.END).strip(),
            "initial_problem": self.problem_text.get(1.0, tk.END).strip(),
            "questions": [q["content"] for q in self.chat_panel.get_messages() if q["type"] == "question"],
            "answers": [a["content"] for a in self.chat_panel.get_messages() if a["type"] == "answer"],
            "root_cause": self.current_analysis_data.get("root_cause", ""),
            "mermaid_diagram": self.diagram_panel.get_current_diagram()
        }
        
        # Show file dialog
        filepath = filedialog.asksaveasfilename(
            title="Export as Markdown",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
            initialdir=self.file_manager.history_dir,
            defaultextension=".md"
        )
        
        if not filepath:
            return
        
        # Export
        exported_path = self.file_manager.export_markdown(analysis_data, filepath)
        
        if exported_path:
            self.status_var.set(f"Analysis exported to {os.path.basename(exported_path)}")
            messagebox.showinfo("Export Successful", f"Analysis exported to {exported_path}")
        else:
            messagebox.showerror("Error", "Failed to export analysis")
    
    def _export_diagram(self):
        """Export diagram as HTML"""
        # Ensure we have a diagram to export
        if not self.diagram_panel.get_current_diagram():
            messagebox.showinfo("Information", "No diagram to export")
            return
        
        # Show file dialog
        filepath = filedialog.asksaveasfilename(
            title="Export Diagram as HTML",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            initialdir=self.file_manager.history_dir,
            defaultextension=".html"
        )
        
        if not filepath:
            return
        
        # Export
        if self.diagram_panel.export_diagram_html(filepath):
            self.status_var.set(f"Diagram exported to {os.path.basename(filepath)}")
            messagebox.showinfo("Export Successful", f"Diagram exported to {filepath}")
        else:
            messagebox.showerror("Error", "Failed to export diagram")
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About 5 Whys Analyzer",
            "5 Whys Root Cause Analysis Tool\n\n"
            "This application helps identify the root cause of problems "
            "using the 5 Whys method with Claude 3.7's extended thinking.\n\n"
            "Created for ShowupSquared."
        )
    
    def _start_analysis(self):
        """Start a new 5 Whys analysis"""
        # Get input values
        job_context = self.job_context_text.get(1.0, tk.END).strip()
        initial_problem = self.problem_text.get(1.0, tk.END).strip()
        
        # Validate input
        if not job_context:
            messagebox.showinfo("Information", "Please enter the job context")
            self.job_context_text.focus_set()
            return
        
        if not initial_problem:
            messagebox.showinfo("Information", "Please enter the initial problem")
            self.problem_text.focus_set()
            return
        
        # Disable input during analysis
        self.start_button.configure(state=tk.DISABLED)
        self.job_context_text.configure(state=tk.DISABLED)
        self.problem_text.configure(state=tk.DISABLED)
        
        # Clear previous analysis
        self.chat_panel.clear_chat()
        self.thinking_panel.clear_content()
        
        # Update UI
        self.chat_panel.add_message("job_context", job_context)
        self.chat_panel.add_message("problem", initial_problem)
        
        # Set context in engine
        self.engine.set_context(job_context, initial_problem)
        
        # Start analysis in a separate thread
        self.analysis_running = True
        threading.Thread(target=self._run_analysis, daemon=True).start()
    
    def _run_analysis(self):
        """Run the analysis in a background thread"""
        try:
            # Update status
            self.root.after(0, lambda: self.status_var.set("Starting analysis..."))
            
            # Start analysis
            response = self.engine.start_analysis(
                on_thinking_update=self._on_thinking_update,
                on_question_ready=self._on_question_ready
            )
            
            # Check for errors
            if "error" in response:
                self.root.after(0, lambda: messagebox.showerror("Error", response["error"]))
                self.root.after(0, lambda: self.status_var.set("Analysis failed"))
                self.root.after(0, lambda: self._enable_input())
                self.analysis_running = False
                return
                
            # Store analysis data
            self.current_analysis_data = {
                "job_context": self.job_context_text.get(1.0, tk.END).strip(),
                "initial_problem": self.problem_text.get(1.0, tk.END).strip(),
                "questions": [response["question"]],
                "answers": [],
                "thinking_history": [response.get("thinking", "")],
                "root_cause": ""
            }
            
            # Update status
            self.root.after(0, lambda: self.status_var.set("Analysis started"))
            
        except Exception as e:
            logger.error(f"Error starting analysis: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to start analysis: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Analysis failed"))
            self.root.after(0, lambda: self._enable_input())
            self.analysis_running = False
    
    def _on_thinking_update(self, thinking_chunk: str):
        """
        Callback for thinking updates
        
        Args:
            thinking_chunk (str): New thinking content
        """
        # Update thinking panel
        self.root.after(0, lambda: self.thinking_panel.append_content(thinking_chunk))
    
    def _on_question_ready(self, question: str, question_number: int):
        """
        Callback for when a question is ready
        
        Args:
            question (str): The question
            question_number (int): Question number (1-5)
        """
        # Add question to chat
        self.root.after(0, lambda: self.chat_panel.add_message("question", (question_number, question)))
        
        # Focus on chat panel
        self.root.after(0, lambda: self._focus_panel("chat"))
        
        # Update status
        self.root.after(0, lambda: self.status_var.set(f"Question {question_number} of 5"))
    
    def _on_answer_submitted(self, answer: str):
        """
        Handle submitted answer
        
        Args:
            answer (str): User's answer
        """
        if not self.analysis_running:
            return
            
        # Disable input while processing
        self.chat_panel.set_input_state(False)
        
        # Update status
        self.status_var.set("Processing answer...")
        
        # Update current analysis data
        self.current_analysis_data["answers"].append(answer)
        
        # Process answer in a separate thread
        threading.Thread(target=self._process_answer, args=(answer,), daemon=True).start()
    
    def _process_answer(self, answer: str):
        """
        Process the user's answer in a background thread
        
        Args:
            answer (str): User's answer
        """
        try:
            # Process the answer
            response = self.engine.process_answer(
                answer,
                on_thinking_update=self._on_thinking_update,
                on_question_ready=self._on_question_ready
            )
            
            # Check for errors
            if "error" in response:
                self.root.after(0, lambda: messagebox.showerror("Error", response["error"]))
                self.root.after(0, lambda: self.status_var.set("Analysis failed"))
                self.root.after(0, lambda: self._enable_input())
                self.analysis_running = False
                return
            
            # Store thinking
            self.current_analysis_data["thinking_history"].append(response.get("thinking", ""))
            
            # Check if analysis is complete
            if response.get("complete", False):
                # Store root cause
                self.current_analysis_data["root_cause"] = response.get("root_cause", "")
                
                # Update chat
                self.root.after(0, lambda: self.chat_panel.add_message("root_cause", response.get("root_cause", "")))
                
                # Update status
                self.root.after(0, lambda: self.status_var.set("Analysis complete"))
                
                # Reenable input
                self.root.after(0, lambda: self._enable_input())
                
                # Set analysis as not running
                self.analysis_running = False
            else:
                # Store question
                self.current_analysis_data["questions"].append(response.get("question", ""))
                
                # Update status
                question_number = response.get("question_number", 0)
                self.root.after(0, lambda: self.status_var.set(f"Question {question_number} of 5"))
            
            # Update diagram
            self.root.after(0, lambda: self._update_diagram())
            
        except Exception as e:
            logger.error(f"Error processing answer: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process answer: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Analysis failed"))
            self.root.after(0, lambda: self._enable_input())
            self.analysis_running = False
    
    def _update_diagram(self):
        """Update the Mermaid diagram"""
        # Get diagram data
        diagram_data = self.engine.get_diagram_data()
        
        # If we don't have diagram data from the engine, use stored data
        if not diagram_data.get("questions"):
            diagram_data = {
                "initial_problem": self.current_analysis_data.get("initial_problem", ""),
                "questions": self.current_analysis_data.get("questions", []),
                "answers": self.current_analysis_data.get("answers", []),
                "root_cause": self.current_analysis_data.get("root_cause", ""),
                "complete": bool(self.current_analysis_data.get("root_cause", ""))
            }
        
        # Generate diagram
        diagram = self.diagram_generator.generate_diagram(diagram_data)
        
        # Update diagram panel
        self.diagram_panel.update_diagram(diagram)
        
        # Store diagram in analysis data
        self.current_analysis_data["mermaid_diagram"] = diagram
    
    def _enable_input(self):
        """Re-enable input fields"""
        self.start_button.configure(state=tk.NORMAL)
        self.job_context_text.configure(state=tk.NORMAL)
        self.problem_text.configure(state=tk.NORMAL)
    
    def _on_close(self):
        """Handle window close event"""
        # Check if we have unsaved data
        if (self.analysis_running or
            (self.current_analysis_data and not self.current_analysis_data.get("saved", False))):
            # Confirm exit
            if not messagebox.askyesno("Confirm Exit", 
                                      "You have unsaved analysis data. Are you sure you want to exit?"):
                return
        
        # Close window
        self.root.destroy()