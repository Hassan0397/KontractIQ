"""
KontractIQ - Helper Functions
Optimized with caching for performance
"""

import re
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from functools import lru_cache
from .constants import LIMITS, RISK_SEVERITIES


def generate_id(text: str) -> str:
    """
    Generate a unique ID from text - OPTIMIZED
    
    Args:
        text: Input text to hash
        
    Returns:
        str: 8-character hash
    """
    return hashlib.md5(text.encode()).hexdigest()[:8]


@lru_cache(maxsize=100)
def format_date(dt_str: Optional[str] = None) -> str:
    """
    Format datetime for display with caching - OPTIMIZED
    
    Args:
        dt_str: Optional ISO format datetime string
        
    Returns:
        str: Formatted date string
    """
    if dt_str:
        dt = datetime.fromisoformat(dt_str)
    else:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_file_size(size_in_bytes: int) -> str:
    """
    Format file size for human reading - OPTIMIZED
    
    Args:
        size_in_bytes: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.1f} GB"


@lru_cache(maxsize=1000)
def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from text with caching - OPTIMIZED
    
    Args:
        text: Input text
        
    Returns:
        List[float]: List of numbers found
    """
    return [float(x) for x in re.findall(r'[\d,]+\.?\d*', text.replace(',', ''))]


@lru_cache(maxsize=1000)
def extract_dollar_amounts(text: str) -> List[float]:
    """
    Extract dollar amounts from text with caching - OPTIMIZED
    
    Args:
        text: Input text
        
    Returns:
        List[float]: List of dollar amounts
    """
    pattern = r'\$\s*([\d,]+\.?\d*)\s*(?:million|billion|M|B)?'
    matches = re.findall(pattern, text, re.IGNORECASE)
    amounts = []
    for m in matches:
        try:
            amount = float(m.replace(',', ''))
            # Check if followed by million/billion in original text
            if 'million' in text.lower() or 'm' in text.lower():
                amount *= 1000000
            elif 'billion' in text.lower() or 'b' in text.lower():
                amount *= 1000000000
            amounts.append(amount)
        except:
            pass
    return amounts


def truncate_text(text: str, max_length: int = None) -> str:
    """
    Truncate text to max length with ellipsis - OPTIMIZED
    
    Args:
        text: Input text
        max_length: Maximum length (default from LIMITS)
        
    Returns:
        str: Truncated text
    """
    if max_length is None:
        max_length = LIMITS.get('max_preview_length', 200)
    
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def is_scanned_pdf(text: str, min_length: int = None) -> bool:
    """
    Check if PDF is likely scanned based on extracted text length - OPTIMIZED
    
    Args:
        text: Extracted text
        min_length: Minimum text length (default from LIMITS)
        
    Returns:
        bool: True if likely scanned
    """
    if min_length is None:
        min_length = LIMITS.get('min_text_length', 100)
    return len(text.strip()) < min_length


@lru_cache(maxsize=100)
def get_risk_severity_color(severity: str) -> str:
    """
    Get color for risk severity with caching - OPTIMIZED
    
    Args:
        severity: Risk severity level
        
    Returns:
        str: Hex color code
    """
    return RISK_SEVERITIES.get(severity, {}).get("color", "#475569")


@lru_cache(maxsize=100)
def get_risk_severity_bg(severity: str) -> str:
    """
    Get background color for risk severity with caching - OPTIMIZED
    
    Args:
        severity: Risk severity level
        
    Returns:
        str: Hex color code
    """
    return RISK_SEVERITIES.get(severity, {}).get("bg", "#F8FAFE")


@lru_cache(maxsize=100)
def get_risk_severity_icon(severity: str) -> str:
    """
    Get icon for risk severity with caching - OPTIMIZED
    
    Args:
        severity: Risk severity level
        
    Returns:
        str: Icon emoji
    """
    return RISK_SEVERITIES.get(severity, {}).get("icon", "⚠️")


def get_risk_badge(severity: str) -> str:
    """
    Get HTML badge for risk severity - OPTIMIZED
    
    Args:
        severity: Risk severity level
        
    Returns:
        str: HTML badge string
    """
    data = RISK_SEVERITIES.get(severity, {})
    color = data.get("color", "#475569")
    bg = data.get("bg", "#F8FAFE")
    label = data.get("label", severity.capitalize())
    return f'<span style="background-color:{bg}; color:{color}; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:500;">{label}</span>'


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries - OPTIMIZED
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Dict[str, Any]: Merged dictionary
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def safe_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value using dot notation - OPTIMIZED
    
    Args:
        data: Dictionary to traverse
        path: Dot-separated path (e.g., 'user.profile.name')
        default: Default value if path not found
        
    Returns:
        Any: Value at path or default
    """
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


@lru_cache(maxsize=1000)
def extract_email_addresses(text: str) -> List[str]:
    """
    Extract email addresses from text with caching - OPTIMIZED
    
    Args:
        text: Input text
        
    Returns:
        List[str]: List of email addresses
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


@lru_cache(maxsize=1000)
def extract_dates(text: str) -> List[str]:
    """
    Extract dates from text with caching - OPTIMIZED
    
    Args:
        text: Input text
        
    Returns:
        List[str]: List of dates found
    """
    patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',  # Month DD, YYYY
    ]
    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    return list(set(dates))


@lru_cache(maxsize=1000)
def extract_contract_parties(text: str) -> Dict[str, str]:
    """
    Extract contract parties from text with caching - OPTIMIZED
    
    Args:
        text: Input text
        
    Returns:
        Dict[str, str]: Dictionary with party names
    """
    parties = {}
    
    # Look for "between X and Y" pattern
    between_match = re.search(r'between\s+([A-Z][a-zA-Z\s]+?)(?:\s+and\s+|\s*\(|\s*$)', text)
    if between_match:
        parties['party_a'] = between_match.group(1).strip()
    
    and_match = re.search(r'and\s+([A-Z][a-zA-Z\s]+?)(?:\s*\(|\s*$)', text)
    if and_match:
        parties['party_b'] = and_match.group(1).strip()
    
    return parties


@lru_cache(maxsize=1000)
def extract_contract_value(text: str) -> Optional[float]:
    """
    Extract contract value from text with caching - OPTIMIZED
    
    Args:
        text: Input text
        
    Returns:
        Optional[float]: Extracted value or None
    """
    amounts = extract_dollar_amounts(text)
    if amounts:
        return max(amounts)  # Return the largest amount
    return None


def generate_demo_id() -> str:
    """
    Generate a unique ID for demo data - OPTIMIZED
    
    Returns:
        str: Unique ID
    """
    from random import randint
    return f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{randint(1000, 9999)}"


def is_valid_uuid(uuid_str: str) -> bool:
    """
    Check if string is a valid UUID - OPTIMIZED
    
    Args:
        uuid_str: UUID string to validate
        
    Returns:
        bool: True if valid UUID
    """
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str.lower()))


def get_contract_health_color(health: str) -> str:
    """
    Get color for contract health status - OPTIMIZED
    
    Args:
        health: Health status
        
    Returns:
        str: Color code
    """
    from .constants import CONTRACT_STATUS_COLORS
    return CONTRACT_STATUS_COLORS.get(health, "#2C5F8A")


def get_contract_health_icon(health: str) -> str:
    """
    Get icon for contract health status - OPTIMIZED
    
    Args:
        health: Health status
        
    Returns:
        str: Icon emoji
    """
    from .constants import CONTRACT_STATUS_ICONS
    return CONTRACT_STATUS_ICONS.get(health, "📄")


def calculate_risk_score(risks: List) -> int:
    """
    Calculate weighted risk score for a list of risks - OPTIMIZED
    
    Args:
        risks: List of risk objects
        
    Returns:
        int: Weighted risk score
    """
    weights = {
        'critical': 10,
        'high': 7,
        'medium': 4,
        'low': 1
    }
    return sum(weights.get(r.severity, 0) for r in risks)