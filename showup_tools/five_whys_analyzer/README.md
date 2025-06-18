# 5 Whys Root Cause Analysis Chatbot

A standalone Tkinter-based chatbot for conducting 5 Whys root cause analysis with Claude 3.7's extended thinking capabilities.

## Overview

This application helps identify the root cause of problems using the "5 Whys" analysis method. It leverages Claude 3.7's extended thinking capabilities to provide in-depth analysis and visualizes the process through an interactive Mermaid diagram.

## Features

- **5 Whys Analysis**: Guide users through the 5 Whys method to uncover root causes
- **Extended Thinking Visualization**: View Claude's thought process in real-time
- **Interactive Diagram**: Visualize the analysis chain with dynamic Mermaid diagrams
- **Save & Load Sessions**: Save your analysis sessions and resume them later
- **Export Options**: Export your analysis as Markdown or HTML
- **Intuitive UI**: User-friendly interface with separate panels for chat, thinking, and diagrams

## Setup

### Prerequisites

- Python 3.8 or higher
- Anthropic API key for Claude 3.7

### Installation

1. Ensure you have your Anthropic API key ready.

2. Install the required dependencies:
   ```
   pip install anthropic requests python-dotenv
   ```

3. Set up your API key in one of the following ways:
   - Create a `.env` file in the project root with:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ```
   - Set it as an environment variable:
     ```
     export ANTHROPIC_API_KEY=your_api_key_here  # Linux/macOS
     set ANTHROPIC_API_KEY=your_api_key_here     # Windows command prompt
     $env:ANTHROPIC_API_KEY="your_api_key_here"  # Windows PowerShell
     ```

### Running the Application

Run the application using:

```
python -m five_whys_analyzer.main
```

Optional command-line arguments:
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--log-file`: Specify custom log file path
- `--config`: Specify custom configuration file path

## Usage Guide

### Starting a New Analysis

1. Enter the job context - background information to help Claude understand the situation
2. Enter the initial problem statement - the issue you're trying to find the root cause for
3. Click "Start Analysis" to begin the process

### Conducting the Analysis

1. Claude will analyze the problem and ask the first "Why?" question
2. Answer the question in the input area at the bottom of the chat panel
3. Claude will think about your answer (visible in the "Claude's Thinking" tab)
4. Claude will ask the next question based on your answer
5. Continue this process for all 5 questions
6. After the fifth question, Claude will identify the root cause

### Using the Diagram

The "Analysis Diagram" tab shows a visual representation of the 5 Whys process:
- Click "Open in Browser" for a full-screen view of the diagram
- Click "Copy Mermaid" to copy the diagram code for use elsewhere

### Saving and Exporting

- Use File → Save Analysis to save your session as a JSON file
- Use File → Export as Markdown to create a Markdown document of your analysis
- Use File → Export Diagram as HTML to save the diagram as a standalone HTML file

## Troubleshooting

If the application fails to start or connect to Claude:
1. Check that your API key is correctly set
2. Ensure you have internet connectivity
3. Look at the log files in the `logs` directory for detailed error information

## License

This project is for personal use within the ShowupSquared toolset.