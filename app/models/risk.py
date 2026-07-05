"""
KontractIQ - Risk Data Model
Optimized with slots for memory efficiency
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from ..utils.constants import RISK_SEVERITIES


@dataclass(slots=True)  # Memory optimization
class Risk:
    """Risk data model - OPTIMIZED with slots"""
    
    id: str
    type: str
    severity: str  # critical, high, medium, low
    description: str
    contract_id: str
    contract_name: str
    clause_text: Optional[str] = None
    recommendation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def severity_label(self) -> str:
        """Get human-readable severity label - O(1)"""
        return RISK_SEVERITIES.get(self.severity, {}).get('label', self.severity.capitalize())
    
    @property
    def severity_color(self) -> str:
        """Get color for severity - O(1)"""
        return RISK_SEVERITIES.get(self.severity, {}).get('color', '#475569')
    
    @property
    def severity_bg(self) -> str:
        """Get background color for severity - O(1)"""
        return RISK_SEVERITIES.get(self.severity, {}).get('bg', '#F8FAFE')
    
    @property
    def severity_border(self) -> str:
        """Get border color for severity - O(1)"""
        return RISK_SEVERITIES.get(self.severity, {}).get('border', '#475569')
    
    @property
    def severity_icon(self) -> str:
        """Get icon for severity - O(1)"""
        return RISK_SEVERITIES.get(self.severity, {}).get('icon', '⚠️')
    
    @property
    def severity_priority(self) -> int:
        """Get priority number (higher = more severe) - O(1)"""
        priorities = {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1
        }
        return priorities.get(self.severity, 0)
    
    @property
    def is_critical(self) -> bool:
        """Check if risk is critical - O(1)"""
        return self.severity == 'critical'
    
    @property
    def is_high(self) -> bool:
        """Check if risk is high - O(1)"""
        return self.severity == 'high'
    
    @property
    def is_medium(self) -> bool:
        """Check if risk is medium - O(1)"""
        return self.severity == 'medium'
    
    @property
    def is_low(self) -> bool:
        """Check if risk is low - O(1)"""
        return self.severity == 'low'
    
    @property
    def needs_immediate_action(self) -> bool:
        """Check if risk needs immediate action - O(1)"""
        return self.severity in ['critical', 'high']
    
    @property
    def risk_score(self) -> int:
        """Calculate numeric risk score (higher = more severe) - O(1)"""
        scores = {
            'critical': 100,
            'high': 75,
            'medium': 50,
            'low': 25
        }
        return scores.get(self.severity, 0)
    
    @property
    def recommendation_default(self) -> str:
        """Get default recommendation if none provided - OPTIMIZED"""
        if self.recommendation:
            return self.recommendation
        
        default_recommendations = {
            'unlimited_liability': 'Limit liability to a reasonable cap (e.g., $1M)',
            'auto_renewal': 'Consider removing auto-renewal or adding termination option',
            'no_termination_convenience': 'Add termination for convenience clause',
            'broad_indemnification': 'Limit indemnification scope to negligence',
            'short_payment_terms': 'Extend payment terms to 30+ days',
            'missing_governing_law': 'Add governing law clause',
            'missing_confidentiality': 'Add confidentiality period duration'
        }
        return default_recommendations.get(self.type, 'Review this clause carefully')
    
    def get_html_badge(self) -> str:
        """Get HTML badge for severity - OPTIMIZED"""
        color = self.severity_color
        bg = self.severity_bg
        label = self.severity_label
        return f'<span style="background-color:{bg}; color:{color}; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:500; border:1px solid {color}33;">{label}</span>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization - OPTIMIZED"""
        return {
            "id": self.id,
            "type": self.type,
            "type_label": self.type.replace('_', ' ').title(),
            "severity": self.severity,
            "severity_label": self.severity_label,
            "severity_color": self.severity_color,
            "severity_icon": self.severity_icon,
            "severity_priority": self.severity_priority,
            "severity_score": self.risk_score,
            "description": self.description,
            "contract_id": self.contract_id,
            "contract_name": self.contract_name,
            "clause_text": self.clause_text,
            "recommendation": self.recommendation or self.recommendation_default,
            "needs_immediate_action": self.needs_immediate_action,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Risk':
        """Create risk from dictionary - OPTIMIZED"""
        return cls(
            id=data.get('id', ''),
            type=data.get('type', ''),
            severity=data.get('severity', 'low'),
            description=data.get('description', ''),
            contract_id=data.get('contract_id', ''),
            contract_name=data.get('contract_name', ''),
            clause_text=data.get('clause_text'),
            recommendation=data.get('recommendation'),  # Keep as None if not present
            metadata=data.get('metadata', {})
        )
    
    @classmethod
    def create_risk(cls, risk_type: str, severity: str, description: str, 
                   contract_id: str, contract_name: str, 
                   clause_text: Optional[str] = None,
                   recommendation: Optional[str] = None) -> 'Risk':
        """Factory method to create a new risk with auto-generated ID - OPTIMIZED"""
        import uuid
        return cls(
            id=f"risk_{uuid.uuid4().hex[:8]}",
            type=risk_type,
            severity=severity,
            description=description,
            contract_id=contract_id,
            contract_name=contract_name,
            clause_text=clause_text,
            recommendation=recommendation
        )
    
    def __str__(self) -> str:
        """String representation - OPTIMIZED"""
        return f"Risk(type={self.type}, severity={self.severity}, contract={self.contract_name})"
    
    def __repr__(self) -> str:
        """Repr representation - OPTIMIZED"""
        return f"Risk(id={self.id}, type={self.type}, severity={self.severity})"