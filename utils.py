"""
Utility functions for the quiz solver
"""
import os
import logging
import hashlib
from typing import Any, Dict, List, Optional
import json

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for the filesystem
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def hash_string(text: str) -> str:
    """
    Create a hash of a string
    
    Args:
        text: Text to hash
    
    Returns:
        Hex digest of hash
    """
    return hashlib.sha256(text.encode()).hexdigest()


def truncate_string(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate a string to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from text
    
    Args:
        text: Text to extract from
    
    Returns:
        List of numbers found
    """
    import re
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    return [float(m) for m in matches]


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def save_json(data: Any, filepath: str) -> None:
    """
    Save data as JSON file
    
    Args:
        data: Data to save
        filepath: Path to save to
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"JSON saved to: {filepath}")


def load_json(filepath: str) -> Any:
    """
    Load data from JSON file
    
    Args:
        filepath: Path to load from
    
    Returns:
        Loaded data
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    logger.info(f"JSON loaded from: {filepath}")
    return data


def ensure_dir(directory: str) -> None:
    """
    Ensure directory exists
    
    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    import re
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()


def parse_table_from_text(text: str) -> Optional[List[List[str]]]:
    """
    Try to parse a table from text
    
    Args:
        text: Text containing table
    
    Returns:
        List of rows or None
    """
    lines = text.strip().split('\n')
    
    # Check if it looks like a table (has consistent delimiters)
    if not lines:
        return None
    
    # Try different delimiters
    for delimiter in ['|', '\t', ',']:
        if delimiter in lines[0]:
            table = []
            for line in lines:
                row = [cell.strip() for cell in line.split(delimiter)]
                table.append(row)
            return table
    
    return None


class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        logger.info(f"{self.name} started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start_time
        logger.info(f"{self.name} completed in {elapsed:.2f}s")


def retry_on_failure(func, max_attempts: int = 3, delay: float = 1.0):
    """
    Retry a function on failure
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Delay between attempts (seconds)
    
    Returns:
        Function result
    """
    import time
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"All {max_attempts} attempts failed")
                raise
