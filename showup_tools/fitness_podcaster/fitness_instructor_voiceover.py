from showup_core.core.log_utils import get_log_path
"""Fitness Instructor Voiceover - ShowupSquared Production Tool

This tool allows users to select fitness content files, specify a target audience,
generate fitness instruction scripts, and convert them to natural-sounding audio files.

Based on the podcast generator with customizations for fitness instruction.
"""
import os
import sys
import logging
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, List
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_panel.main_panel import ClaudeAIPanel
from claude_panel.podcast_integration import extend_claude_ai_panel
from core.text_processing import load_learner_profiles, read_file_content
from fitness_podcaster.text_processing import prepare_fitness_content_for_prompt
from fitness_podcaster.fitness_script_generator import generate_fitness_script
from fitness_podcaster.audio_processor import convert_fitness_script_to_audio, DEFAULT_TTS_CONFIG, enhance_fitness_script_with_ssml
from fitness_podcaster.gui_components import FitnessInputTab, FitnessScriptTab
from fitness_podcaster.batch_processing_tab import BatchProcessingTab
from core.gui_components import AudioTab
from core.editor_tab import EditorTab
ExtendedClaudeAIPanel = extend_claude_ai_panel(ClaudeAIPanel)
load_dotenv()
logging.basicConfig(level=logging.INFO, format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(get_log_path('fitness_podcaster')), logging.
    StreamHandler()])
logger = logging.getLogger('fitness_instructor_voiceover')


class FitnessInstructorGenerator:
    """Main class for fitness instruction generation functionality"""

    def __init__(self):
        self.selected_files = []
        self.target_audience = ''
        self.script_content = ''
        self.audio_file_path = ''
        self.audience_profiles: Dict[str, str] = {}
        self.tts_config = DEFAULT_TTS_CONFIG.copy()
        self.word_limit = 500
        self.load_audience_profiles()

    def load_audience_profiles(self) ->None:
        """Load available audience profiles from the profiles directory"""
        self.audience_profiles = load_learner_profiles()

    def get_profile_names(self) ->List[str]:
        """Get list of available profile names"""
        return sorted(list(self.audience_profiles.keys()))

    def get_profile_content(self, profile_name: str) ->str:
        """Get content for a specific profile"""
        return self.audience_profiles.get(profile_name, profile_name)

    def select_files(self) ->List[str]:
        """Allow user to select input content files"""
        from tkinter import filedialog
        return filedialog.askopenfilenames(title=
            'Select Fitness Content Files', filetypes=[('Text Files',
            '*.txt'), ('Markdown Files', '*.md'), ('All Files', '*.*')])

    def read_file_content(self, file_path: str) ->str:
        """Read content from a file"""
        return read_file_content(file_path)

    def prepare_content_for_prompt(self, file_paths: List[str]) ->str:
        """Process content files to extract key exercise details for fitness instruction script generation"""
        return prepare_fitness_content_for_prompt(file_paths)

    def generate_script(self, content: str, target_audience: str) ->str:
        """Generate fitness instruction script using OpenAI API with optimized prompt"""
        return generate_fitness_script(content, target_audience, self.
            word_limit)

    def convert_to_audio(self, script: str, output_dir: str=None) ->str:
        """Convert script to audio using Azure TTS with SSML enhancement"""
        return convert_fitness_script_to_audio(script, self.tts_config,
            output_dir)

    def enhance_with_ssml(self, script: str) ->str:
        """Transform script into SSML-enhanced output"""
        return enhance_fitness_script_with_ssml(script, self.tts_config)


class FitnessInstructorGUI:
    """GUI for the Fitness Instructor Voiceover Generator"""

    def __init__(self, root):
        self.root = root
        self.root.title('ShowupSquared Fitness Instructor Voiceover')
        self.root.geometry('900x700')
        self.root.minsize(800, 600)
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.
                path.abspath(__file__))), 'images', 'app_icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            logger.warning(f'Could not set app icon: {str(e)}')
        self.generator = FitnessInstructorGenerator()
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.main_frame = ttk.Frame(root, padding='10')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_tab = ttk.Frame(self.notebook)
        self.script_tab = ttk.Frame(self.notebook)
        self.audio_tab = ttk.Frame(self.notebook)
        self.batch_tab = ttk.Frame(self.notebook)
        self.editor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text='1. Input')
        self.notebook.add(self.script_tab, text='2. Script')
        self.notebook.add(self.audio_tab, text='3. Audio')
        self.notebook.add(self.batch_tab, text='4. Batch Processing')
        self.status_var = tk.StringVar()
        self.status_var.set('Ready')
        self.status_bar = ttk.Label(root, textvariable=self.status_var,
            relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_tab_obj = FitnessInputTab(self.input_tab, self)
        self.script_tab_obj = FitnessScriptTab(self.script_tab, self)
        self.audio_tab_obj = AudioTab(self.audio_tab, self)
        self.batch_tab_obj = BatchProcessingTab(self.batch_tab, self)
        self.editor_tab_obj = EditorTab(self.editor_tab, self,
            ExtendedClaudeAIPanel)
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

    def _on_tab_changed(self, event):
        """Handle tab change events"""
        current_tab = self.notebook.index('current')
        tab_names = ['Input', 'Script', 'Audio', 'Modular Editor',
            'Batch Processing']
        self.status_var.set(f'Viewing {tab_names[current_tab]} tab')

    def _generate_script(self):
        """Generate the fitness instruction script"""
        selected_files = self.input_tab_obj.get_selected_files()
        if not selected_files:
            messagebox.showwarning('No Files Selected',
                'Please select at least one content file.')
            return
        target_audience = self.input_tab_obj.get_target_learner()
        if not target_audience:
            messagebox.showwarning('No Target Specified',
                'Please specify a target audience.')
            return
        try:
            word_limit = int(self.input_tab_obj.get_word_limit())
            if word_limit <= 0:
                raise ValueError('Word limit must be a positive number')
            self.generator.word_limit = word_limit
        except (ValueError, TypeError) as e:
            messagebox.showwarning('Invalid Word Limit',
                f'Please enter a valid word limit: {str(e)}')
            return
        self.root.config(cursor='wait')
        self.status_var.set('Generating script...')
        generate_button = self.input_tab_obj.generate_button
        if generate_button:
            generate_button.config(state='disabled')
        thread = threading.Thread(target=self.generate_thread, args=(
            selected_files, target_audience))
        thread.daemon = True
        thread.start()

    def generate_thread(self, selected_files, target_audience):
        """Thread function for script generation"""
        try:
            content = self.generator.prepare_content_for_prompt(selected_files)
            if not content:
                self.root.after(0, lambda : messagebox.showerror(
                    'Processing Error',
                    'Failed to extract content from the selected files.'))
                return
            script = self.generator.generate_script(content, target_audience)
            if not script:
                self.root.after(0, lambda : messagebox.showerror(
                    'Generation Error',
                    'Failed to generate the script. Check the logs for details.'
                    ))
                return
            self.root.after(0, lambda : self._update_script(script))
        except Exception as e:
            error_msg = str(e)
            logger.error(f'Error generating script: {error_msg}')
            self.root.after(0, lambda : [messagebox.showerror('Error',
                f'An error occurred: {error_msg}'), self.status_var.set(
                'Error generating script'), self.root.config(cursor='')])
        finally:
            self.root.after(0, lambda : [self.input_tab_obj.generate_button
                .config(state='normal') if self.input_tab_obj.
                generate_button else None])

    def _update_script(self, script):
        """Update the script editor with generated content"""
        self.generator.script_content = script
        self.script_tab_obj.update_script(script)
        self.notebook.select(1)
        self.status_var.set('Script generated successfully')
        self.root.config(cursor='')

    def _convert_to_audio(self):
        """Convert the script to audio using Azure TTS with SSML enhancement"""
        script = self.generator.script_content
        if not script:
            script = self.script_tab_obj.get_script_content()
        if not script:
            messagebox.showwarning('No Script',
                'Please generate or enter a script first.')
            return
        self.root.config(cursor='wait')
        self.status_var.set('Converting to audio...')
        convert_button = self.script_tab_obj.convert_button
        if convert_button:
            convert_button.config(state='disabled')
        thread = threading.Thread(target=self.convert_thread, args=(script,))
        thread.daemon = True
        thread.start()

    def convert_thread(self, script):
        """Thread function for audio conversion"""
        try:
            self.generator.script_content = script
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.
                path.abspath(__file__))), 'generated_fitness_audio')
            os.makedirs(output_dir, exist_ok=True)
            audio_file = self.generator.convert_to_audio(script, output_dir)
            if not audio_file or not os.path.exists(audio_file):
                self.root.after(0, lambda : messagebox.showerror(
                    'Conversion Error',
                    'Failed to generate audio file. Check the logs for details.'
                    ))
                return
            self.root.after(0, lambda : self._update_audio(audio_file))
        except Exception as e:
            error_msg = str(e)
            logger.error(f'Error converting to audio: {error_msg}')
            self.root.after(0, lambda : [messagebox.showerror('Error',
                f'An error occurred: {error_msg}'), self.status_var.set(
                'Error converting to audio'), self.root.config(cursor='')])
        finally:
            self.root.after(0, lambda : [self.script_tab_obj.convert_button
                .config(state='normal') if self.script_tab_obj.
                convert_button else None])

    def _update_audio(self, result):
        """Update the audio tab with generated audio file"""
        self.generator.audio_file_path = result
        self.audio_tab_obj.update_audio(result)
        self.notebook.select(2)
        self.status_var.set('Audio generated successfully')
        self.root.config(cursor='')

    def _reset_all(self):
        """Reset the application for a new fitness voiceover"""
        if messagebox.askyesno('Confirm Reset',
            'Are you sure you want to start a new fitness voiceover? All unsaved data will be lost.'
            ):
            try:
                self.generator.selected_files = []
                self.generator.target_audience = ''
                self.generator.script_content = ''
                self.generator.audio_file_path = ''
                if hasattr(self.input_tab_obj, 'reset'):
                    self.input_tab_obj.reset()
                if hasattr(self.script_tab_obj, 'reset'):
                    self.script_tab_obj.reset()
                if hasattr(self.audio_tab_obj, 'reset'):
                    self.audio_tab_obj.reset()
                self.notebook.select(0)
                self.status_var.set('Ready for new fitness voiceover')
            except Exception as e:
                logger.error(f'Error resetting application: {str(e)}')
                messagebox.showerror('Error',
                    f'An error occurred while resetting: {str(e)}')

    def _send_files_to_editor(self):
        """Send selected files to the modular editor"""
        pass

    def _on_close(self):
        """Handle window close event"""
        if messagebox.askyesno('Confirm Exit',
            'Are you sure you want to exit? All unsaved data will be lost.'):
            self.root.destroy()


def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = FitnessInstructorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
