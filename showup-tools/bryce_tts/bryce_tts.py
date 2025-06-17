#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bryce TTS Application

A simple GUI application that allows users to paste text, convert it to SSML,
and send it to Azure for Text-to-Speech conversion.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime
import logging
import re
import html

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('bryce_tts')

# Directly set the Azure Speech credentials
# These values are from the .env file at C:\Users\User\Desktop\ShowupSquaredV4 (2)\ShowupSquaredV4\ShowupSquaredV4\.env
os.environ['AZURE_SPEECH_KEY'] = '4zkciee4eTEj6oOojR2Xm2OCBcv7z70Qp3h8kTtGNbN2H9biOoclJQQJ99BDACYeBjFXJ3w3AAAYACOGYLsL'
os.environ['AZURE_SPEECH_REGION'] = 'eastus'
logger.info("Azure Speech credentials set directly in code")

# Default voice configuration
DEFAULT_VOICE = "en-US-Andrew:DragonHDLatestNeural"
DEFAULT_TEMPERATURE = "0.5"

# SSML limits for Azure Dragon models
# Dragon models have specific limitations with SSML tags
DRAGON_SSML_NOTES = "\n".join([
    "Note: Dragon HD models have specific SSML limitations:",
    "- Limited support for prosody tags",
    "- May not support all emphasis levels",
    "- Temperature parameter affects expressiveness",
    "- Some styles may not be available for all voices"
])


class BryceTTSApp:
    """Main application class for Bryce TTS."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Bryce TTS")
        self.root.geometry("800x600")
        
        # Create output directory
        self.output_dir = "C:\\Users\\User\\Documents\\ShowUp\\TTS_Genereated_audio"
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"Output directory created/verified: {self.output_dir}")
        except Exception as e:
            logger.error(f"Error creating output directory: {str(e)}")
            # Fallback to a directory we know will work
            self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_audio")
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"Using fallback output directory: {self.output_dir}")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a note about Dragon SSML limitations
        note_frame = ttk.Frame(main_frame)
        note_frame.pack(fill=tk.X, pady=5)
        
        note_label = ttk.Label(note_frame, text=DRAGON_SSML_NOTES, foreground='blue', wraplength=780, justify='left')
        note_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Text input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Text", padding="5")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Voice settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Voice Settings", padding="5")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # Voice selection
        voice_frame = ttk.Frame(settings_frame)
        voice_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(voice_frame, text="Voice:").pack(side=tk.LEFT, padx=5)
        
        self.voice_var = tk.StringVar(value=DEFAULT_VOICE)
        self.voice_combo = ttk.Combobox(voice_frame, textvariable=self.voice_var)
        self.voice_combo['values'] = (
            # Dragon HD models
            "en-US-Andrew:DragonHDLatestNeural",
            "en-US-Andrew2:DragonHDLatestNeural",
            "en-US-Andrew3:DragonHDLatestNeural",
            "en-US-Aria:DragonHDLatestNeural",
            "en-US-Ava:DragonHDLatestNeural",
            "en-US-Ava3:DragonHDLatestNeural",
            "en-US-Brian:DragonHDLatestNeural",
            "en-US-Davis:DragonHDLatestNeural",
            "en-US-Emma:DragonHDLatestNeural",
            "en-US-Emma2:DragonHDLatestNeural",
            "en-US-Jenny:DragonHDLatestNeural",
            "en-US-Steffan:DragonHDLatestNeural"
        )
        self.voice_combo.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Temperature setting
        temp_frame = ttk.Frame(settings_frame)
        temp_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(temp_frame, text="Temperature:").pack(side=tk.LEFT, padx=5)
        
        self.temp_var = tk.StringVar(value=DEFAULT_TEMPERATURE)
        self.temp_entry = ttk.Entry(temp_frame, textvariable=self.temp_var, width=10)
        self.temp_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(temp_frame, text="(0.0 - 1.0)").pack(side=tk.LEFT, padx=5)
        
        # Output file settings
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="5")
        output_frame.pack(fill=tk.X, pady=5)
        
        file_frame = ttk.Frame(output_frame)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Output Directory:").pack(side=tk.LEFT, padx=5)
        
        self.output_path_var = tk.StringVar(value=self.output_dir)
        self.output_path_entry = ttk.Entry(file_frame, textvariable=self.output_path_var)
        self.output_path_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_output_dir)
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        # File prefix
        prefix_frame = ttk.Frame(output_frame)
        prefix_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(prefix_frame, text="File Prefix:").pack(side=tk.LEFT, padx=5)
        
        self.prefix_var = tk.StringVar(value="bryce_tts")
        self.prefix_entry = ttk.Entry(prefix_frame, textvariable=self.prefix_var)
        self.prefix_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # SSML preview section
        ssml_frame = ttk.LabelFrame(main_frame, text="SSML Preview", padding="5")
        ssml_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.ssml_preview = scrolledtext.ScrolledText(ssml_frame, wrap=tk.WORD, height=10)
        self.ssml_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.preview_btn = ttk.Button(button_frame, text="Generate SSML Preview", command=self.preview_ssml)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.generate_btn = ttk.Button(button_frame, text="Generate Audio", command=self.generate_audio)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.set_status("Ready")
    
    def set_status(self, message):
        """Update the status bar message."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def browse_output_dir(self):
        """Open a directory browser dialog to select the output directory."""
        dir_path = filedialog.askdirectory(initialdir=self.output_dir)
        if dir_path:
            self.output_path_var.set(dir_path)
    
    def clear_all(self):
        """Clear all input fields and reset to defaults."""
        self.text_input.delete(1.0, tk.END)
        self.ssml_preview.delete(1.0, tk.END)
        self.voice_var.set(DEFAULT_VOICE)
        self.temp_var.set(DEFAULT_TEMPERATURE)
        self.set_status("Ready")
    
    def preview_ssml(self):
        """Generate SSML preview from the input text."""
        text = self.text_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text to convert.")
            return
        
        try:
            ssml = self.enhance_text_with_ssml(text)
            self.ssml_preview.delete(1.0, tk.END)
            self.ssml_preview.insert(tk.END, ssml)
            self.set_status("SSML preview generated")
        except Exception as e:
            logger.error(f"Error generating SSML: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate SSML: {str(e)}")
    
    def generate_audio(self):
        """Generate audio from the input text using Azure TTS."""
        text = self.text_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text to convert.")
            return
        
        try:
            # Generate SSML
            ssml = self.enhance_text_with_ssml(text)
            self.ssml_preview.delete(1.0, tk.END)
            self.ssml_preview.insert(tk.END, ssml)
            
            # Generate audio
            self.set_status("Generating audio...")
            output_path = self.convert_text_to_audio(ssml)
            
            self.set_status(f"Audio generated: {output_path}")
            messagebox.showinfo("Success", f"Audio file generated:\n{output_path}")
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate audio: {str(e)}")
    
    def enhance_text_with_ssml(self, text):
        """Convert plain text to SSML with enhanced features."""
        # Check if text already contains SSML tags
        if '<speak' in text or '<voice' in text:
            logger.error("Text already contains SSML tags. Cannot process.")
            raise ValueError("Input text already contains SSML tags. Cannot process.")
            
        # Check if the selected voice is a Dragon HD model
        is_dragon = ":Dragon" in self.voice_var.get()
        
        # Escape XML special characters
        content = html.escape(text)
        
        # Process text for pauses and emphasis
        content = self.process_text_markers(content)
        
        # Create SSML document
        voice_name = self.voice_var.get()
        temperature = self.temp_var.get()
        
        ssml_output = '<?xml version="1.0"?>\n'
        ssml_output += '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        ssml_output += 'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n'
        ssml_output += f'<voice name="{voice_name}" parameters="temperature={temperature}">\n'
        
        # Add global prosody settings - more limited for Dragon models
        if ":Dragon" in voice_name:
            # Dragon models have more limited prosody support
            ssml_output += '<prosody volume="0%">\n'
        else:
            ssml_output += '<prosody rate="0%" pitch="0%" volume="0%">\n'
        
        # Process each paragraph
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Add paragraph tag around content
            ssml_output += f'<p>{paragraph}</p>\n'
        
        # Close tags
        ssml_output += '</prosody>\n'
        ssml_output += '</voice>\n'
        ssml_output += '</speak>'
        
        return ssml_output
    
    def process_text_markers(self, text):
        """Process text markers for pauses and emphasis."""
        # Add pauses at sentence boundaries
        text = re.sub(r'(\. |\.\n)([A-Z])', r'.<break time="350ms"/> \2', text)
        
        # Add slight pauses after commas
        text = re.sub(r'(, |,\n)([a-zA-Z])', r',<break time="150ms"/> \2', text)
        
        return text
    
    def convert_text_to_audio(self, ssml_text):
        """Convert SSML text to audio using Azure TTS."""
        # Get output directory
        output_dir = self.output_path_var.get()
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_prefix = self.prefix_var.get()
        output_filename = f"{file_prefix}_{timestamp}.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save SSML to file for reference
        ssml_filename = f"{file_prefix}_{timestamp}.ssml"
        ssml_path = os.path.join(output_dir, ssml_filename)
        with open(ssml_path, 'w', encoding='utf-8') as f:
            f.write(ssml_text)
        
        # Get Azure Speech credentials from environment variables
        speech_key = os.environ.get("AZURE_SPEECH_KEY")
        speech_region = os.environ.get("AZURE_SPEECH_REGION")
        
        logger.info(f"Using Azure Speech credentials - Key available: {bool(speech_key)}, Region: {speech_region}")
        
        if not speech_key or not speech_region:
            logger.error("Azure Speech credentials not found in environment variables")
            raise ValueError("Missing Azure Speech credentials. Please check the application code.")
        
        # Configure speech synthesizer
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        
        # Configure audio output
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Synthesize speech
        result = speech_synthesizer.speak_ssml_async(ssml_text).get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.info(f"Speech synthesis completed for {output_filename}")
            return output_path
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
            logger.error(f"Speech synthesis error details: {cancellation_details.error_details}")
            raise Exception(f"Speech synthesis failed: {cancellation_details.reason}\n{cancellation_details.error_details}")
        else:
            logger.warning(f"Speech synthesis result: {result.reason}")
            return output_path


def main():
    """Main entry point for the application."""
    # Print current working directory for debugging
    current_dir = os.getcwd()
    logger.info(f"Current working directory: {current_dir}")
    
    # Environment variables should already be loaded at this point
    root = tk.Tk()
    app = BryceTTSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
