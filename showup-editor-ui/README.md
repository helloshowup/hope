# Showup Editor UI

This repository contains the modular Claude Panel UI and supporting assets for ShowupSquaredV4.

## Launch Instructions

1. Ensure you have Python 3.8+ and pip installed.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install -e ../showup-core   # Editable install of showup-core
   pip install -e ../showup-tools  # Editable install of showup-tools
   ```
   RAG features rely on both `showup-core` and `showup-tools` being installed
   locally. When launching the UI your `PYTHONPATH` must include these
   directories in addition to the project root. The vector database powering
   RAG queries only functions on the local machine.
3. Build the handbook index:
   ```sh
   python ../scripts/index_handbook.py --file path/to/handbook.pdf
   ```
   Use `--force` to rebuild an existing index.
4. Verify imports using the provided sanity check script:
   ```sh
   python ../scripts/import_sanity_check.py
   ```
5. Launch the UI:
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
