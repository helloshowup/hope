# Markdown to ODT Converter

A utility for converting Markdown documents to OpenDocument Text (ODT) format, enabling easy import into LibreOffice Writer and other ODT-compatible editors.

## Purpose

This tool streamlines the process of transforming structured Markdown files into ODT format for further editing, formatting, or sharing in word processors.

## Setup & Installation

- Requires Python 3.7 or newer
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

## Usage

1. Place your Markdown files in the `input/` directory.
2. Run the converter:
   ```sh
   python md_to_odt.py
   ```
3. Output ODT files will appear in the `output/` directory.

## Testing

- Run tests with:
  ```sh
  pytest tests/
  ```

## Documentation

- See `docs/` for detailed usage and format specifications.
