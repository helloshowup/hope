import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Union

from config import DEFAULT_CATEGORIES


class FileHandler:
    """Handles file operations for the admin assistant."""
    
    def __init__(self, base_dir: Union[str, Path]) -> None:
        """Initialize the file handler with a base directory.
        
        Args:
            base_dir: Directory to scan for files
        """
        self.base_dir = Path(base_dir)
        self.organized_dir = self.base_dir / 'Organized'
    
    def scan_directory(self, recursive: bool = True) -> List[Path]:
        """Scan a directory for files.
        
        Args:
            recursive: Whether to scan recursively
            
        Returns:
            List of file paths
        """
        if not self.base_dir.exists():
            raise FileNotFoundError(f"Directory {self.base_dir} not found")
        
        files = []
        if recursive:
            for path in self.base_dir.rglob('*'):
                if path.is_file() and not self._is_in_organized_dir(path):
                    files.append(path)
        else:
            for path in self.base_dir.glob('*'):
                if path.is_file():
                    files.append(path)
        
        return files
    
    def _is_in_organized_dir(self, path: Path) -> bool:
        """Check if a path is inside the organized directory.
        
        Args:
            path: Path to check
            
        Returns:
            True if path is in organized dir, False otherwise
        """
        try:
            # Convert to absolute paths for comparison
            organized_abs = self.organized_dir.resolve()
            path_abs = path.resolve()
            
            # Check if organized_dir is a parent of path
            return str(organized_abs) in str(path_abs)
        except Exception:
            # If any error occurs, assume not in organized dir
            return False
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        
        stats = file_path.stat()
        file_info = {
            "name": file_path.name,
            "extension": file_path.suffix,
            "size_bytes": stats.st_size,
            "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "path": str(file_path),
            "parent_dir": file_path.parent.name
        }
        
        # Try to get first few lines of text files for context
        if file_path.suffix.lower() in ['.txt', '.md', '.csv', '.py', '.js', '.html', '.css']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first_lines = []
                    for i, line in enumerate(f):
                        if i >= 5:  # Only get first 5 lines
                            break
                        first_lines.append(line.strip())
                    file_info["preview"] = "\n".join(first_lines)
            except Exception:
                pass  # Ignore errors in getting preview
        
        return file_info
    
    def read_text_file(self, file_path: Path) -> str:
        """Read the content of a text file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Content of the file as string
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}")
    
    def move_file(self, file_path: Path, category: str) -> Tuple[bool, str]:
        """Move a file to a category folder.
        
        Args:
            file_path: Path to the file
            category: Category folder name
            
        Returns:
            Tuple of (success, message)
        """
        if not file_path.exists():
            return False, f"File {file_path} not found"
        
        # Get the target directory for the category
        organized_base = self.organized_dir
        target_dir = organized_base / category
        
        # Create the target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create the target file path
        target_file = target_dir / file_path.name
        
        # Check if a file with the same name already exists
        if target_file.exists():
            # Add timestamp to filename to make it unique
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            name_parts = file_path.stem, file_path.suffix
            new_name = f"{name_parts[0]}_{timestamp}{name_parts[1]}"
            target_file = target_dir / new_name
        
        try:
            # Move the file
            shutil.move(str(file_path), str(target_file))
            return True, f"Moved to {category}"
        except Exception as e:
            return False, f"Error moving file: {e}"
    
    def get_available_categories(self) -> List[str]:
        """Get available category folders.
        
        Returns:
            List of category names
        """
        # Start with default categories
        categories = set(DEFAULT_CATEGORIES.keys())
        
        # Add any existing category folders
        if self.organized_dir.exists():
            for path in self.organized_dir.glob('*'):
                if path.is_dir():
                    categories.add(path.name)
        
        return sorted(list(categories))
