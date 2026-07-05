"""
KontractIQ - File Handling Utilities
"""

import os
import json
import csv
import io
from typing import List, Dict, Any, Optional
import streamlit as st
from ..models.contract import Contract
from ..models.clause import Clause
from ..models.risk import Risk

def save_uploaded_file(file) -> bytes:
    """
    Save uploaded file content to bytes
    
    Args:
        file: Uploaded file object
        
    Returns:
        bytes: File content
    """
    return file.read()


def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """
    Validate file type by extension
    
    Args:
        filename: Name of the file
        allowed_types: List of allowed extensions
        
    Returns:
        bool: True if valid
    """
    ext = os.path.splitext(filename)[1].lower().replace('.', '')
    return ext in allowed_types


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension without dot
    """
    return os.path.splitext(filename)[1].lower().replace('.', '')


def export_contracts_to_csv(contracts: List[Contract]) -> str:
    """
    Export contracts to CSV format
    
    Args:
        contracts: List of contract objects
        
    Returns:
        str: CSV data as string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Contract Name', 'File Type', 'Pages', 'Clauses', 'Risks', 'Upload Date'])
    
    # Write data
    for contract in contracts:
        writer.writerow([
            contract.name,
            contract.file_type.upper(),
            contract.pages,
            contract.clause_count,
            contract.risk_count,
            contract.upload_date.strftime('%Y-%m-%d %H:%M')
        ])
    
    return output.getvalue()


def export_clauses_to_csv(clauses: List[Clause]) -> str:
    """
    Export clauses to CSV format
    
    Args:
        clauses: List of clause objects
        
    Returns:
        str: CSV data as string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Contract Name', 'Clause Type', 'Clause Text', 'Confidence'])
    
    # Write data
    for clause in clauses:
        writer.writerow([
            clause.contract_name,
            clause.type,
            clause.text[:500] + '...' if len(clause.text) > 500 else clause.text,
            f"{clause.confidence * 100:.0f}%"
        ])
    
    return output.getvalue()


def export_risks_to_csv(risks: List[Risk]) -> str:
    """
    Export risks to CSV format
    
    Args:
        risks: List of risk objects
        
    Returns:
        str: CSV data as string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Contract Name', 'Risk Type', 'Severity', 'Description'])
    
    # Write data
    for risk in risks:
        writer.writerow([
            risk.contract_name,
            risk.type.replace('_', ' ').title(),
            risk.severity_label,
            risk.description
        ])
    
    return output.getvalue()


def export_session_data(contracts: List[Contract], clauses: List[Clause], risks: List[Risk]) -> Dict[str, Any]:
    """
    Export all session data as dictionary
    
    Args:
        contracts: List of contract objects
        clauses: List of clause objects
        risks: List of risk objects
        
    Returns:
        dict: Session data
    """
    return {
        'contracts': [c.to_dict() for c in contracts],
        'clauses': [c.to_dict() for c in clauses],
        'risks': [r.to_dict() for r in risks],
        'total_contracts': len(contracts),
        'total_clauses': len(clauses),
        'total_risks': len(risks)
    }


def import_contracts_from_json(json_data: str) -> List[Contract]:
    """
    Import contracts from JSON data
    
    Args:
        json_data: JSON string containing contract data
        
    Returns:
        List[Contract]: List of contract objects
    """
    try:
        data = json.loads(json_data)
        contracts = []
        
        for contract_data in data.get('contracts', []):
            contract = Contract(
                id=contract_data.get('id', ''),
                name=contract_data.get('name', ''),
                file_type=contract_data.get('file_type', ''),
                file_size=contract_data.get('file_size', 0),
                upload_date=contract_data.get('upload_date', ''),
                text=contract_data.get('text', ''),
                pages=contract_data.get('pages', 0),
                is_scanned=contract_data.get('is_scanned', False)
            )
            contracts.append(contract)
        
        return contracts
    except Exception as e:
        raise ValueError(f"Failed to import contracts: {str(e)}")


def get_file_size_str(file_size: int) -> str:
    """
    Get human-readable file size string
    
    Args:
        file_size: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if file_size < 1024.0:
            return f"{file_size:.1f} {unit}"
        file_size /= 1024.0
    return f"{file_size:.1f} GB"