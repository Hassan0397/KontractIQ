"""
KontractIQ - Clause Extraction Engine
Identifies and extracts 8 clause types from contract text
OPTIMIZED for speed and performance
"""

import re
from typing import List, Dict, Any, Optional
import time
from ..models.clause import Clause
from ..utils.helpers import generate_id
from ..utils.constants import CLAUSE_TYPES

class ClauseExtractor:
    """Extract clauses from contract text - OPTIMIZED version"""
    
    def __init__(self):
        """Initialize the clause extractor - lazy loading"""
        self.nlp = None
        self._loaded = False
    
    def _load_nlp(self):
        """Lazy load SpaCy model only when needed"""
        if not self._loaded:
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
                self._loaded = True
            except:
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
                self._loaded = True
    
    def extract_all_clauses(self, text: str, contract_id: str, contract_name: str) -> List[Clause]:
        """Extract all clause types from text - OPTIMIZED"""
        clauses = []
        
        # Limit text length for performance
        if len(text) > 100000:  # 100k chars max
            text = text[:100000]
        
        # Extract each clause type with optimized patterns
        for clause_type in CLAUSE_TYPES:
            extracted = self._extract_clause_type(text, clause_type, contract_id, contract_name)
            if extracted:
                clauses.extend(extracted)
        
        # Only use SpaCy if we have less than 5 clauses and text is short
        if len(clauses) < 5 and len(text) < 50000:
            try:
                self._load_nlp()
                if self.nlp:
                    doc = self.nlp(text[:50000])  # Only process first 50k chars
                    # Add any additional clauses found by SpaCy
                    for ent in doc.ents:
                        if ent.label_ in ["LAW", "ORG", "GPE"] and len(ent.text) > 10:
                            # Check if this entity might be a clause
                            existing_types = [c.type for c in clauses]
                            if "Governing Law" not in existing_types and "law" in ent.text.lower():
                                clause = Clause(
                                    id=generate_id(f"{contract_id}_nlp_{ent.text[:30]}"),
                                    type="Governing Law",
                                    text=ent.text[:500],
                                    contract_id=contract_id,
                                    contract_name=contract_name,
                                    confidence=0.6
                                )
                                clauses.append(clause)
            except:
                pass  # Ignore SpaCy errors
        
        return clauses
    
    def _extract_clause_type(self, text: str, clause_type: str, contract_id: str, contract_name: str) -> List[Clause]:
        """Extract a specific clause type - OPTIMIZED with compiled patterns"""
        clauses = []
        patterns = self._get_patterns(clause_type)
        
        # Compile patterns for speed
        compiled_patterns = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in patterns]
        
        for pattern in compiled_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                clause_text = match.group(0).strip()
                if clause_text and len(clause_text) > 10:  # Minimum meaningful text
                    # Limit clause text length
                    if len(clause_text) > 1000:
                        clause_text = clause_text[:1000]
                    
                    clause = Clause(
                        id=generate_id(f"{contract_id}_{clause_type}_{clause_text[:50]}"),
                        type=clause_type,
                        text=clause_text,
                        contract_id=contract_id,
                        contract_name=contract_name,
                        confidence=0.85
                    )
                    clauses.append(clause)
                    break  # Only take first match per pattern to avoid duplicates
        
        return clauses
    
    def _get_patterns(self, clause_type: str) -> List[str]:
        """Get regex patterns for each clause type - OPTIMIZED patterns"""
        patterns = {
            "Governing Law": [
                r"(?:governing law|choice of law|governing jurisdiction)[\s\S]{0,200}?(?:california|new york|delaware|texas|florida|illinois|pennsylvania|ohio|georgia|north carolina|michigan|new jersey|virginia|washington|massachusetts|arizona|tennessee|indiana|missouri|maryland|wisconsin|colorado|minnesota|south carolina|alabama|louisiana|kentucky|oregon|oklahoma|connecticut|iowa|mississippi|arkansas|kansas|utah|nevada)",
                r"(?:laws of|under the laws of)[\s\S]{0,100}?(?:california|new york|delaware)",
            ],
            "Payment Terms": [
                r"(?:payment terms|payment period|payment due|payable within)[\s\S]{0,100}?(\d+)\s*(?:days|day)",
                r"(?:net|NET)\s*(\d+)\s*(?:days|day)",
                r"(?:due upon|payable upon)[\s\S]{0,100}?(\d+)\s*(?:days|day)",
            ],
            "Liability Cap": [
                r"(?:liability cap|liability limit|maximum liability|limit of liability)[\s\S]{0,150}?(?:\$|USD)\s*([\d,]+\.?\d*)\s*(?:million|M|billion|B)?",
                r"(?:liability shall not exceed|liability is limited to)[\s\S]{0,150}?(?:\$|USD)\s*([\d,]+\.?\d*)\s*(?:million|M|billion|B)?",
                r"unlimited liability",
            ],
            "Termination Notice": [
                r"(?:termination notice|notice of termination|termination period)[\s\S]{0,100}?(\d+)\s*(?:days|day)",
                r"(?:notice period|period of notice)[\s\S]{0,100}?(\d+)\s*(?:days|day)",
            ],
            "Confidentiality Period": [
                r"(?:confidentiality period|confidentiality term)[\s\S]{0,100}?(\d+)\s*(?:years|year|months|month)",
                r"(?:confidential information).{0,50}?(\d+)\s*(?:years|year)",
            ],
            "Renewal Terms": [
                r"(?:auto-?renew|automatic renewal)[\s\S]{0,150}?(?:renew|renewal)",
                r"(?:renewal term|renewal period)[\s\S]{0,100}?(\d+)\s*(?:years|year)",
                r"(?:shall renew|will renew|renews automatically)",
            ],
            "Indemnification": [
                r"(?:indemnify|indemnification|indemnity)[\s\S]{0,200}?(?:against|for|from)",
                r"(?:hold harmless|defend).{0,100}?(?:against|from)",
            ],
            "Force Majeure": [
                r"(?:force majeure|act of god|unforeseeable event)[\s\S]{0,200}?(?:beyond control|unforeseen)",
            ]
        }
        return patterns.get(clause_type, [])