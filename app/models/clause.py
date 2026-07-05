"""
KontractIQ - Clause Data Model
slots for memory efficiency 
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from ..utils.constants import CLAUSE_TYPE_COLORS, CLAUSE_TYPE_ICONS


@dataclass(slots=True)  # Memory optimization - reduces memory usage by ~40%
class Clause:
    """
    Clause data model - OPTIMIZED with slots
    
    Attributes:
        id: Unique identifier for the clause
        type: Clause type (e.g., "Governing Law", "Payment Terms")
        text: Full clause text content
        contract_id: ID of parent contract
        contract_name: Name of parent contract
        page: Page number where clause was found (optional)
        confidence: Confidence score (0-1) of extraction accuracy
        metadata: Additional metadata dictionary
    """
    
    id: str
    type: str
    text: str
    contract_id: str
    contract_name: str
    page: Optional[int] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_high_confidence(self) -> bool:
        """Check if clause has high confidence - O(1)"""
        return self.confidence >= 0.8
    
    @property
    def confidence_level(self) -> str:
        """Get confidence level as string - O(1)"""
        if self.confidence >= 0.9:
            return "High"
        elif self.confidence >= 0.7:
            return "Medium"
        else:
            return "Low"
    
    @property
    def confidence_color(self) -> str:
        """Get confidence level color - O(1)"""
        from ..utils.constants import COLORS
        if self.confidence >= 0.9:
            return COLORS['semantic']['success']
        elif self.confidence >= 0.7:
            return COLORS['semantic']['warning']
        else:
            return COLORS['semantic']['danger']
    
    @property
    def confidence_badge(self) -> str:
        """Get confidence badge HTML - O(1)"""
        from ..utils.constants import COLORS
        if self.confidence >= 0.8:
            return f'<span style="background: {COLORS["semantic"]["success_bg"]}; color: {COLORS["semantic"]["success"]}; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">High {self.confidence * 100:.0f}%</span>'
        elif self.confidence >= 0.6:
            return f'<span style="background: {COLORS["semantic"]["warning_bg"]}; color: {COLORS["semantic"]["warning"]}; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">Medium {self.confidence * 100:.0f}%</span>'
        else:
            return f'<span style="background: {COLORS["semantic"]["danger_bg"]}; color: {COLORS["semantic"]["danger"]}; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">Low {self.confidence * 100:.0f}%</span>'
    
    @property
    def type_icon(self) -> str:
        """Get icon for clause type - O(1)"""
        return CLAUSE_TYPE_ICONS.get(self.type, "📄")
    
    @property
    def type_color(self) -> str:
        """Get color for clause type - O(1)"""
        return CLAUSE_TYPE_COLORS.get(self.type, "#475569")
    
    @property
    def preview(self) -> str:
        """Get a preview of the clause text - O(1)"""
        from ..utils.constants import LIMITS
        max_length = LIMITS.get('max_preview_length', 200)
        if len(self.text) <= max_length:
            return self.text
        return self.text[:max_length] + "..."
    
    @property
    def preview_short(self) -> str:
        """Get a short preview (100 chars) - O(1)"""
        if len(self.text) <= 100:
            return self.text
        return self.text[:100] + "..."
    
    @property
    def word_count(self) -> int:
        """Get word count - O(1)"""
        return len(self.text.split())
    
    @property
    def char_count(self) -> int:
        """Get character count - O(1)"""
        return len(self.text)
    
    @property
    def line_count(self) -> int:
        """Get line count - O(1)"""
        return self.text.count('\n') + 1
    
    def contains_text(self, search_text: str) -> bool:
        """Check if clause contains search text - O(n)"""
        return search_text.lower() in self.text.lower()
    
    def contains_any(self, search_terms: list) -> bool:
        """Check if clause contains any of the search terms - O(n)"""
        text_lower = self.text.lower()
        return any(term.lower() in text_lower for term in search_terms)
    
    def extract_matches(self, search_text: str, context_chars: int = 50) -> list:
        """Extract matches with context - O(n)"""
        matches = []
        text_lower = self.text.lower()
        search_lower = search_text.lower()
        start = 0
        
        while True:
            pos = text_lower.find(search_lower, start)
            if pos == -1:
                break
            
            # Get context
            context_start = max(0, pos - context_chars)
            context_end = min(len(self.text), pos + len(search_text) + context_chars)
            
            match_text = self.text[context_start:context_end]
            matches.append({
                'text': match_text,
                'position': pos,
                'highlight': search_text
            })
            start = pos + 1
        
        return matches
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization - OPTIMIZED"""
        return {
            "id": self.id,
            "type": self.type,
            "type_icon": self.type_icon,
            "type_color": self.type_color,
            "text": self.text,
            "contract_id": self.contract_id,
            "contract_name": self.contract_name,
            "page": self.page,
            "confidence": self.confidence,
            "confidence_level": self.confidence_level,
            "confidence_color": self.confidence_color,
            "is_high_confidence": self.is_high_confidence,
            "metadata": self.metadata,
            "preview": self.preview,
            "preview_short": self.preview_short,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "line_count": self.line_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Clause':
        """Create clause from dictionary - OPTIMIZED"""
        return cls(
            id=data.get('id', ''),
            type=data.get('type', ''),
            text=data.get('text', ''),
            contract_id=data.get('contract_id', ''),
            contract_name=data.get('contract_name', ''),
            page=data.get('page'),
            confidence=data.get('confidence', 1.0),
            metadata=data.get('metadata', {})
        )
    
    def __str__(self) -> str:
        """String representation - OPTIMIZED"""
        return f"Clause(type={self.type}, contract={self.contract_name}, confidence={self.confidence:.2f})"
    
    def __repr__(self) -> str:
        """Repr representation - OPTIMIZED"""
        return f"Clause(id={self.id}, type={self.type}, contract_id={self.contract_id})"
    
    def __hash__(self) -> int:
        """Hash for set operations - OPTIMIZED"""
        return hash(self.id)
    
    def __eq__(self, other) -> bool:
        """Equality check - OPTIMIZED"""
        if not isinstance(other, Clause):
            return False
        return self.id == other.id