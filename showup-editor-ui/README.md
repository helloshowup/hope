# Showup Editor UI

This repository contains the modular Claude Panel UI and supporting assets for ShowupSquaredV4.

## Launch Instructions

1. Ensure you have Python 3.8+ and pip installed.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install -e ../showup-core  # Editable install of showup-core
   ```
3. Launch the UI:
   ```sh
   python -m claude_panel.main
   ```

## Directory Structure
- claude_panel/: Main UI code
- assets/: Static assets (images, CSS, etc.)
- templates/: UI templates

## Development
- Ensure all changes follow PEP8 and modular code standards.
- UI tests should be placed in `tests/` if/when available.
