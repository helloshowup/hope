# Admin Assistant Chatbot

A Python-based chatbot that acts as an administrative assistant to organize files into appropriate folders. The chatbot leverages:

- Claude 3.7 Sonnet for decision making about file organization
- Claude Haiku for cost-efficient document summarization
- Python for file handling operations

## Features

- Automatically categorizes and moves files to appropriate folders
- Generates document summaries using Claude Haiku (more cost-effective)
- Makes folder organization decisions using Claude 3.7
- Minimal token usage by offloading thinking to Claude's extended thinking capability

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
4. Run the assistant: `python main.py`

## Usage

Interact with the assistant by running the main script and following the prompts. You can:

- Ask the assistant to analyze and organize files in a specific directory
- Get summaries of documents
- Request organization recommendations

## Project Structure

- `main.py`: Entry point for the application
- `file_handler.py`: Contains file operation functions
- `claude_api.py`: Handles interactions with Claude API
- `config.py`: Configuration and environment settings
- `requirements.txt`: Project dependencies
