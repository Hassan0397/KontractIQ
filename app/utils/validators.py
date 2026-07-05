"""
KontractIQ - Input Validators
Optimized with caching for performance
"""

import os
import re
from typing import Tuple, Optional, Dict, Any, List
from functools import lru_cache
from .constants import LIMITS, SUPPORTED_FILE_TYPES


@lru_cache(maxsize=1000)
def validate_file_extension(filename: str) -> Tuple[bool, str]:
    """
    Validate file extension - OPTIMIZED with caching
    
    Args:
        filename: Name of the file
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if not filename:
        return False, "No filename provided"
    
    ext = os.path.splitext(filename)[1].lower().replace('.', '')
    
    if ext not in SUPPORTED_FILE_TYPES:
        return False, f"Unsupported file type: .{ext}. Supported: {', '.join(SUPPORTED_FILE_TYPES.keys())}"
    
    return True, f"Valid file type: .{ext}"


def validate_file_size(file_size: int) -> Tuple[bool, str]:
    """
    Validate file size - OPTIMIZED
    
    Args:
        file_size: Size in bytes
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    max_bytes = LIMITS["max_file_size_mb"] * 1024 * 1024
    
    if file_size <= 0:
        return False, "File is empty"
    
    if file_size > max_bytes:
        return False, f"File exceeds {LIMITS['max_file_size_mb']}MB limit"
    
    return True, f"{file_size / 1024:.1f} KB"


def validate_file_content(file_content: bytes) -> Tuple[bool, str]:
    """
    Validate file content - OPTIMIZED
    
    Args:
        file_content: File content as bytes
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if not file_content:
        return False, "File content is empty"
    
    # Check if content is readable text
    try:
        text_preview = file_content[:1000].decode('utf-8', errors='ignore')
        if len(text_preview.strip()) < 10:
            return False, "File appears to be binary or empty"
    except:
        pass
    
    return True, "File content appears valid"


def validate_file(file) -> Tuple[bool, str]:
    """
    Validate uploaded file - OPTIMIZED
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if file is None:
        return False, "No file provided"
    
    # Check file name
    if not file.name:
        return False, "File has no name"
    
    # Check file extension
    valid_ext, ext_msg = validate_file_extension(file.name)
    if not valid_ext:
        return False, ext_msg
    
    # Check file size
    try:
        valid_size, size_msg = validate_file_size(file.size)
        if not valid_size:
            return False, size_msg
    except AttributeError:
        # Some file objects don't have size attribute
        pass
    
    return True, "Valid file"


def validate_file_batch(files: List, current_count: int, max_contracts: int, max_file_size: int) -> Tuple[bool, str]:
    """
    Validate a batch of files - OPTIMIZED
    
    Args:
        files: List of uploaded files
        current_count: Current contract count
        max_contracts: Maximum allowed contracts
        max_file_size: Maximum file size in bytes
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if not files:
        return False, "No files provided"
    
    # Early validation for total count
    total_files = len(files)
    if current_count + total_files > max_contracts:
        return False, f"Cannot upload {total_files} files. Only {max_contracts - current_count} slots remaining."
    
    # Check each file
    for file in files:
        # Validate file
        valid, msg = validate_file(file)
        if not valid:
            return False, f"Invalid file '{file.name}': {msg}"
        
        # Check individual file size
        if hasattr(file, 'size') and file.size > max_file_size:
            size_mb = file.size / (1024 * 1024)
            max_mb = max_file_size / (1024 * 1024)
            return False, f"File '{file.name}' exceeds size limit ({size_mb:.1f}MB > {max_mb:.0f}MB)"
    
    return True, f"✅ {total_files} files ready for processing"


def validate_contract_count(current_count: int) -> Tuple[bool, str]:
    """
    Validate contract count limit - OPTIMIZED
    
    Args:
        current_count: Current number of contracts
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    max_contracts = LIMITS["max_contracts"]
    
    if current_count >= max_contracts:
        return False, f"Maximum {max_contracts} contracts per session reached"
    
    remaining = max_contracts - current_count
    return True, f"Can upload {remaining} more contract(s)"


def validate_search_query(query: str) -> Tuple[bool, str]:
    """
    Validate search query - OPTIMIZED
    
    Args:
        query: Search query string
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if not query:
        return False, "Search query is empty"
    
    clean_query = query.strip()
    
    if len(clean_query) < 2:
        return False, "Search query must be at least 2 characters"
    
    if len(clean_query) > 500:
        return False, "Search query is too long (max 500 characters)"
    
    return True, "Valid query"


def validate_template_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate template data - OPTIMIZED
    
    Args:
        data: Template data dictionary
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if not data:
        return False, "No template data provided"
    
    if "template_type" not in data:
        return False, "Missing template_type field"
    
    if "fields" not in data:
        return False, "Missing fields data"
    
    if not isinstance(data["fields"], dict):
        return False, "Fields must be a dictionary"
    
    # Check required fields
    template_type = data["template_type"]
    required_fields = _get_required_fields(template_type)
    
    for field in required_fields:
        if field not in data["fields"] or not data["fields"][field]:
            return False, f"Missing required field: {field}"
    
    return True, "Valid template data"


@lru_cache(maxsize=100)
def _get_required_fields(template_type: str) -> List[str]:
    """
    Get required fields for template type with caching - OPTIMIZED
    
    Args:
        template_type: Type of template
        
    Returns:
        List[str]: List of required field names
    """
    from ..core.templates import get_template_fields
    
    fields = get_template_fields(template_type)
    if not fields:
        return []
    
    return [name for name, config in fields.items() if config.get('required', False)]


def validate_email(email: str) -> bool:
    """
    Validate email address - OPTIMIZED
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number - OPTIMIZED
    
    Args:
        phone: Phone number to validate
        
    Returns:
        bool: True if valid
    """
    # Remove common formatting
    clean = re.sub(r'[\s\-\(\)\.]', '', phone)
    # Check if it's a valid phone number format
    return len(clean) >= 10 and len(clean) <= 15 and clean.isdigit()


def validate_date_format(date_str: str) -> bool:
    """
    Validate date format - OPTIMIZED
    
    Args:
        date_str: Date string to validate
        
    Returns:
        bool: True if valid
    """
    patterns = [
        r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
        r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
        r'^\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}$',  # D MMM YYYY
    ]
    for pattern in patterns:
        if re.match(pattern, date_str, re.IGNORECASE):
            return True
    return False


def validate_batch_size(file_count: int, max_batch_size: int = 10) -> Tuple[bool, str]:
    """
    Validate batch size limit - OPTIMIZED
    
    Args:
        file_count: Number of files in batch
        max_batch_size: Maximum allowed batch size
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if file_count <= 0:
        return False, "No files to process"
    
    if file_count > max_batch_size:
        return False, f"Batch size exceeds maximum of {max_batch_size} files"
    
    return True, f"Batch size of {file_count} files is valid"