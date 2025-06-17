from showup_core.core.log_utils import get_log_path
"""
RAG System Demo for ShowupSquared

Demonstrates how to use the RAG system with existing content generation workflow.
Provides a simple UI to select a handbook file and test content generation with RAG.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import asyncio
import logging
import time
import threading
logging.basicConfig(level=logging.INFO, format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(get_log_path('examples')), logging.StreamHandler()])
logger = logging.getLogger('rag_demo')
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.
    abspath(__file__)))))
try:
    from simplified_workflow.content_generator import generate_content
    logger.info('Successfully imported content generator with RAG support')
except ImportError as e:
    logger.error(f'Failed to import content generator: {e}')
    messagebox.showerror('Import Error',
        f'Could not import content generator: {e}')
    sys.exit(1)


class RAGDemoApp:
    """Simple demo application for the RAG system"""

    def __init__(self, root):
        self.root = root
        self.root.title('ShowupSquared RAG System Demo')
        self.root.geometry('800x700')
        self.root.minsize(800, 700)
        self.bg_color = '#fdf6d3'
        self.root.configure(bg=self.bg_color)
        self._create_styles()
        self.handbook_path_var = tk.StringVar()
        self.model_var = tk.StringVar(value='claude-3-5-sonnet-20240620')
        self.token_limit_var = tk.StringVar(value='4000')
        self.temperature_var = tk.StringVar(value='0.7')
        self.word_count_var = tk.StringVar(value='500')
        self._create_widgets()
        self.generation_running = False

    def _create_styles(self):
        """Create ttk styles for consistent background color"""
        style = ttk.Style()
        style.configure('BG.TFrame', background=self.bg_color)
        style.configure('BG.TLabel', background=self.bg_color)
        style.configure('BG.TLabelframe', background=self.bg_color)
        style.configure('BG.TLabelframe.Label', background=self.bg_color)
        border_color = '#e6dfc4'
        style.configure('BG.TLabelframe', bordercolor=border_color)

    def _create_widgets(self):
        """Create all UI widgets"""
        main_frame = ttk.Frame(self.root, style='BG.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        title_label = ttk.Label(main_frame, text=
            'ShowupSquared RAG System Demo', font=('Arial', 16, 'bold'),
            style='BG.TLabel')
        title_label.pack(pady=10)
        description_label = ttk.Label(main_frame, text=
            'This tool demonstrates how to use the RAG system to reduce token usage when generating content.'
            , font=('Arial', 10), style='BG.TLabel')
        description_label.pack(pady=(0, 10))
        handbook_frame = ttk.LabelFrame(main_frame, text='Student Handbook',
            style='BG.TLabelframe')
        handbook_frame.pack(fill=tk.X, pady=10, padx=5)
        handbook_file_frame = ttk.Frame(handbook_frame, style='BG.TFrame')
        handbook_file_frame.pack(fill=tk.X, pady=5)
        ttk.Label(handbook_file_frame, text='Handbook File:', style='BG.TLabel'
            ).pack(side=tk.LEFT, padx=5)
        ttk.Entry(handbook_file_frame, textvariable=self.handbook_path_var,
            width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(handbook_file_frame, text='Browse...', command=self.
            _browse_handbook).pack(side=tk.LEFT, padx=5)
        default_handbook = os.path.join(os.path.dirname(os.path.abspath(
            __file__)), 'EHS Student Catalog_Handbook from Canva.md')
        if os.path.exists(default_handbook):
            self.handbook_path_var.set(default_handbook)
            logger.info(f'Found default handbook at {default_handbook}')
        settings_frame = ttk.LabelFrame(main_frame, text=
            'Generation Settings', style='BG.TLabelframe')
        settings_frame.pack(fill=tk.X, pady=10, padx=5)
        model_frame = ttk.Frame(settings_frame, style='BG.TFrame')
        model_frame.pack(fill=tk.X, pady=5)
        ttk.Label(model_frame, text='Model:', style='BG.TLabel').pack(side=
            tk.LEFT, padx=5)
        models = ['claude-3-7-sonnet-20250219',
            'claude-3-5-sonnet-20240620', 'claude-3-haiku-20240307',
            'claude-3-opus-20240229']
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.
            model_var, values=models, width=25, state='readonly')
        model_dropdown.pack(side=tk.LEFT, padx=5)
        token_frame = ttk.Frame(settings_frame, style='BG.TFrame')
        token_frame.pack(fill=tk.X, pady=5)
        ttk.Label(token_frame, text='Token Limit:', style='BG.TLabel').pack(
            side=tk.LEFT, padx=5)
        ttk.Entry(token_frame, textvariable=self.token_limit_var, width=10
            ).pack(side=tk.LEFT, padx=5)
        temp_frame = ttk.Frame(settings_frame, style='BG.TFrame')
        temp_frame.pack(fill=tk.X, pady=5)
        ttk.Label(temp_frame, text='Temperature:', style='BG.TLabel').pack(side
            =tk.LEFT, padx=5)
        ttk.Entry(temp_frame, textvariable=self.temperature_var, width=10
            ).pack(side=tk.LEFT, padx=5)
        word_frame = ttk.Frame(settings_frame, style='BG.TFrame')
        word_frame.pack(fill=tk.X, pady=5)
        ttk.Label(word_frame, text='Word Count:', style='BG.TLabel').pack(side
            =tk.LEFT, padx=5)
        ttk.Entry(word_frame, textvariable=self.word_count_var, width=10).pack(
            side=tk.LEFT, padx=5)
        query_frame = ttk.LabelFrame(main_frame, text='Query', style=
            'BG.TLabelframe')
        query_frame.pack(fill=tk.X, pady=10, padx=5)
        step_title_frame = ttk.Frame(query_frame, style='BG.TFrame')
        step_title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(step_title_frame, text='Step Title:', style='BG.TLabel'
            ).pack(side=tk.LEFT, padx=5)
        self.step_title_var = tk.StringVar(value='Academic Integrity Policy')
        ttk.Entry(step_title_frame, textvariable=self.step_title_var, width=50
            ).pack(side=tk.LEFT, padx=5)
        outline_frame = ttk.Frame(query_frame, style='BG.TFrame')
        outline_frame.pack(fill=tk.X, pady=5)
        ttk.Label(outline_frame, text='Content Outline:', style='BG.TLabel'
            ).pack(anchor=tk.W, padx=5)
        self.outline_text = scrolledtext.ScrolledText(outline_frame, height=4)
        self.outline_text.pack(fill=tk.X, padx=5, pady=5)
        self.outline_text.insert(tk.END,
            'Explain the academic integrity policy, including what constitutes academic dishonesty and the consequences.'
            )
        results_frame = ttk.LabelFrame(main_frame, text='Results', style=
            'BG.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.
            progress_var, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5, padx=5)
        self.status_var = tk.StringVar(value='Ready')
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
            style='BG.TLabel')
        status_label.pack(pady=5)
        generate_button = ttk.Button(main_frame, text=
            'Generate Content with RAG', command=self._generate_content)
        generate_button.pack(pady=10)

    def _browse_handbook(self):
        """Browse for a handbook file"""
        handbook_path = filedialog.askopenfilename(title=
            'Select Handbook File', filetypes=[('Markdown files', '*.md'),
            ('Text files', '*.txt'), ('All files', '*.*')])
        if handbook_path:
            self.handbook_path_var.set(handbook_path)
            logger.info(f'Selected handbook file: {handbook_path}')

    def _update_status(self, message):
        """Update status label"""
        self.status_var.set(message)
        logger.info(message)
        self.root.update_idletasks()

    def _generate_content(self):
        """Generate content using the RAG system"""
        if self.generation_running:
            messagebox.showinfo('Generation in Progress',
                'Content generation is already running. Please wait for it to complete.'
                )
            return
        handbook_path = self.handbook_path_var.get()
        if not handbook_path or not os.path.exists(handbook_path):
            messagebox.showerror('Error', 'Please select a valid handbook file'
                )
            return
        try:
            token_limit = int(self.token_limit_var.get())
            temperature = float(self.temperature_var.get())
            word_count = int(self.word_count_var.get())
        except ValueError as e:
            messagebox.showerror('Invalid Settings',
                f'Please enter valid numbers for token limit, temperature, and word count: {e}'
                )
            return
        step_title = self.step_title_var.get()
        content_outline = self.outline_text.get('1.0', tk.END).strip()
        if not step_title or not content_outline:
            messagebox.showerror('Error',
                'Please enter a step title and content outline')
            return
        template = """
        Please create educational content about {step_title} based on the following outline:
        
        {content_outline}
        
        The content should be approximately {word_count} words.
        """
        variables = {'step_title': step_title, 'content_outline':
            content_outline, 'word_count': word_count, 'handbook_path':
            handbook_path}
        settings = {'token_limit': token_limit, 'temperature': temperature,
            'model': self.model_var.get()}
        self.generation_running = True
        self.progress.start(10)
        self._update_status('Generating content...')
        self.results_text.delete('1.0', tk.END)
        threading.Thread(target=self._run_generation, args=(variables,
            template, settings)).start()

    def _run_generation(self, variables, template, settings):
        """Run the content generation in a separate thread"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            start_time = time.time()
            content = loop.run_until_complete(generate_content(variables,
                template, settings))
            end_time = time.time()
            self.root.after(0, self._handle_results, content, end_time -
                start_time)
        except Exception as e:
            error_msg = f'Error during content generation: {e}'
            logger.exception(error_msg)
            self.root.after(0, self._handle_error, error_msg)
        finally:
            loop.close()

    def _handle_results(self, content, elapsed_time):
        """Handle successful generation results"""
        self.progress.stop()
        self.generation_running = False
        self._update_status(
            f'Generation completed in {elapsed_time:.2f} seconds')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, content)

    def _handle_error(self, error_msg):
        """Handle generation error"""
        self.progress.stop()
        self.generation_running = False
        self._update_status('Generation failed')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, f'ERROR: {error_msg}')
        messagebox.showerror('Generation Error', error_msg)


def main():
    """Run the RAG demo application"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    root = tk.Tk()
    app = RAGDemoApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
