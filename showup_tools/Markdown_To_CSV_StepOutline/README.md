# Markdown to CSV Converter for ShowUpSquared

A modular, user-friendly application for converting structured Markdown educational content into CSV format compatible with the ShowUpSquared system.

## Features

- Convert structured Markdown files to CSV format
- Optional AI enhancement using Anthropic Claude API
- User-friendly graphical interface
- Command-line interface for batch processing
- Seamless integration with the ShowUpSquared ecosystem

## Getting Started

### Prerequisites

- Python 3.7 or newer
- Required Python packages (installed automatically from parent project)

### Running the Application

Simply run the batch file to launch the application:

```
launch_md_to_csv_converter.bat
```

## Input Format

The converter expects Markdown files structured as follows:

```markdown
# Module Title

## Lesson Title

### Step Title
**Type:** Content/Activity/Assessment/Quiz
**Rationale:** Why this step is important for learning.

Step content goes here...

**Content Outline:**
- Key point 1
- Key point 2
- Key point 3
```

## Usage

1. Launch the application using the batch file
2. Select your Markdown input file
3. Choose your CSV output location
4. Select conversion options (AI enhancement if available)
5. Click "Convert" to process the file

## Command Line Usage

For batch processing or automation, you can use the command line interface:

```
python main.py input.md output.csv [--use-ai] [--method hybrid|ai_driven|rule_based]
```

## Project Structure

```
├── src/
│   ├── core/              # Core conversion functionality
│   │   ├── api_handler.py # AI integration
│   │   └── markdown_converter.py  # Main converter logic
│   ├── gui/               # User interface components
│   │   └── app_gui.py     # Tkinter GUI implementation
│   └── utils/             # Utility functions
│       ├── config.py      # Configuration management
│       └── logging_utils.py  # Logging setup
├── main.py                # Application entry point
└── launch_md_to_csv_converter.bat  # Launch script
```

## Notes

- Environment variables are read from the parent project's `.env` file
- Logs are saved to the `logs/` directory
