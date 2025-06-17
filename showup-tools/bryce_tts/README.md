# Bryce TTS Application

A simple GUI application that allows users to paste text, convert it to SSML, and send it to Azure for Text-to-Speech conversion using Dragon HD voice models.

## Features

- Paste text into the GUI
- Convert text to SSML with proper formatting
- Send SSML to Azure TTS for speech synthesis
- Save the resulting audio file
- Configure voice settings (Dragon HD model selection, temperature)
- Customize output directory and file prefix

## Requirements

- Python 3.6+
- Azure Speech Service subscription
- Environment variables set for Azure credentials:
  - `AZURE_SPEECH_KEY`
  - `AZURE_SPEECH_REGION`

## Usage

1. Run the application: `python bryce_tts.py`
2. Paste your text into the input field
3. Optionally adjust voice settings
4. Click "Generate SSML Preview" to see the SSML that will be sent to Azure
5. Click "Generate Audio" to create the audio file
6. The output file will be saved in C:\Users\User\Documents\ShowUp\TTS_Genereated_audio by default (can be changed in the UI)

## Notes

- The application automatically adds appropriate pauses at sentence boundaries and after commas
- Both the SSML and audio files are saved with timestamps for reference
- Error messages will be displayed if Azure credentials are missing or if there are issues with the TTS service

## Dragon HD Voice Model Limitations

- Dragon HD models have specific SSML limitations
- Limited support for prosody tags (primarily volume adjustments)
- May not support all emphasis levels
- Temperature parameter affects expressiveness
- Some styles may not be available for all voices
- The application automatically adjusts SSML generation based on the selected voice model
