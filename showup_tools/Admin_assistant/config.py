import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Model configurations
CLAUDE_SONNET = "claude-3-7-sonnet-20250219"  # Updated to support thinking
CLAUDE_HAIKU = "claude-3-haiku-20240307"

# File organization settings
DEFAULT_SCAN_DIR = os.getenv('DEFAULT_SCAN_DIR', str(Path.home() / 'Documents'))
DEFAULT_CATEGORIES = {
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac'],
    'video': ['.mp4', '.avi', '.mov', '.wmv', '.mkv'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php'],
    'spreadsheets': ['.xlsx', '.xls', '.csv'],
    'presentations': ['.pptx', '.ppt'],
    'ebooks': ['.epub', '.mobi', '.azw'],
}

# Claude API settings
API_TIMEOUT = 30  # seconds
MAX_THINKING_TOKENS = 1024
MAX_OUTPUT_TOKENS = 4096

# Local paths for organized files
def get_organized_path(category: str) -> Path:
    """Get the path for a specific category of files."""
    base_dir = Path(DEFAULT_SCAN_DIR)
    return base_dir / 'Organized' / category
