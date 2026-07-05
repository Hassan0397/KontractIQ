"""
KontractIQ - Contract Data Model
Optimized with slots for memory efficiency
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Set, Tuple
import hashlib
import re
import uuid
from ..models.clause import Clause
from ..models.risk import Risk


@dataclass(slots=True)  # Memory optimization
class Contract:
    """
    Contract data model - PREMIUM ENHANCED with:
    - Memory optimization with slots
    - Comprehensive search capabilities
    - Health scoring and analytics
    - Vendor and value extraction
    - Full serialization support
    """
    
    # ========================================================================
    # CORE FIELDS
    # ========================================================================
    
    id: str
    name: str
    file_type: str
    file_size: int
    upload_date: datetime
    text: str = ""
    pages: int = 0
    file_hash: str = ""  # File hash for deduplication and integrity checking
    metadata: Dict[str, Any] = field(default_factory=dict)
    clauses: List[Clause] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)
    is_scanned: bool = False
    vendor: Optional[str] = None  # Extracted vendor name
    contract_value: Optional[float] = None  # Extracted contract value
    
    # ========================================================================
    # POST-INITIALIZATION
    # ========================================================================
    
    def __post_init__(self):
        """Initialize file_hash and extract metadata"""
        if not self.file_hash:
            if self.text:
                # Generate hash from text content
                self.file_hash = hashlib.md5(self.text.encode('utf-8')).hexdigest()
            else:
                # Generate hash from id and name as fallback
                hash_input = f"{self.id}_{self.name}".encode('utf-8')
                self.file_hash = hashlib.md5(hash_input).hexdigest()
        
        # Extract vendor if available
        if not self.vendor and self.text:
            self._extract_vendor()
        
        # Extract contract value if available
        if not self.contract_value and self.text:
            self._extract_contract_value()
    
    # ========================================================================
    # EXTRACTION METHODS
    # ========================================================================
    
    def _extract_vendor(self):
        """Extract vendor name from contract text"""
        patterns = [
            r'between\s+([A-Z][a-zA-Z\s]+?)(?:\s+and\s+|\s*\(|\s*$)',
            r'by and between\s+([A-Z][a-zA-Z\s]+?)(?:\s+and\s+|\s*\(|\s*$)',
            r'(?:Service Provider|Provider|Supplier|Vendor)\s*:?\s*([A-Z][a-zA-Z\s]+?)(?:\n|\,|\.)',
            r'(?:Party A|Party of the first part)\s*:?\s*([A-Z][a-zA-Z\s]+?)(?:\n|\,|\.)',
            r'(?:Client|Customer)\s*:?\s*([A-Z][a-zA-Z\s]+?)(?:\n|\,|\.)',
            r'([A-Z][a-zA-Z\s]+?)\s*(?:Corp|Corporation|Inc|LLC|Ltd|Limited|Company|Co)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE)
            if match:
                self.vendor = match.group(1).strip()
                break
        
        # If not found, try to extract from filename
        if not self.vendor:
            name_parts = self.name.replace('.pdf', '').replace('.docx', '').replace('.txt', '').split('_')
            if name_parts:
                self.vendor = name_parts[0]
    
    def _extract_contract_value(self):
        """Extract contract value from text"""
        from ..utils.helpers import extract_dollar_amounts
        amounts = extract_dollar_amounts(self.text)
        if amounts:
            self.contract_value = max(amounts)
    
    # ========================================================================
    # BASIC PROPERTIES
    # ========================================================================
    
    @property
    def has_text(self) -> bool:
        """Check if contract has text content - O(1)"""
        return len(self.text.strip()) > 0
    
    @property
    def clause_count(self) -> int:
        """Get number of clauses extracted - O(1)"""
        return len(self.clauses)
    
    @property
    def risk_count(self) -> int:
        """Get number of risks found - O(1)"""
        return len(self.risks)
    
    @property
    def has_clauses(self) -> bool:
        """Check if contract has any clauses - O(1)"""
        return len(self.clauses) > 0
    
    @property
    def has_risks(self) -> bool:
        """Check if contract has any risks - O(1)"""
        return len(self.risks) > 0
    
    @property
    def word_count(self) -> int:
        """Get approximate word count - O(1)"""
        return len(self.text.split())
    
    @property
    def character_count(self) -> int:
        """Get character count - O(1)"""
        return len(self.text)
    
    @property
    def sentence_count(self) -> int:
        """Get approximate sentence count - O(1)"""
        return len(re.findall(r'[.!?]+', self.text))
    
    @property
    def paragraph_count(self) -> int:
        """Get approximate paragraph count - O(1)"""
        return len([p for p in self.text.split('\n\n') if p.strip()])
    
    @property
    def line_count(self) -> int:
        """Get line count - O(1)"""
        return len(self.text.split('\n'))
    
    @property
    def average_word_length(self) -> float:
        """Get average word length - O(1)"""
        words = self.text.split()
        if not words:
            return 0
        return sum(len(w) for w in words) / len(words)
    
    # ========================================================================
    # CLAUSE PROPERTIES
    # ========================================================================
    
    @property
    def clause_types(self) -> List[str]:
        """Get unique clause types - OPTIMIZED"""
        return list({c.type for c in self.clauses})
    
    @property
    def clause_summary(self) -> Dict[str, int]:
        """Get clause type counts - OPTIMIZED"""
        summary = {}
        for clause in self.clauses:
            summary[clause.type] = summary.get(clause.type, 0) + 1
        return summary
    
    @property
    def clause_density(self) -> float:
        """Calculate clause density (clauses per 1000 words)"""
        if self.word_count == 0:
            return 0
        return (self.clause_count / self.word_count) * 1000
    
    @property
    def clause_type_coverage(self) -> float:
        """Get percentage of clause types present (out of 8)"""
        total_types = 8  # Total possible clause types
        present_types = len(self.clause_types)
        return (present_types / total_types) * 100 if total_types > 0 else 0
    
    @property
    def clause_type_coverage_score(self) -> int:
        """Get clause type coverage score (0-100)"""
        return int(self.clause_type_coverage)
    
    # Individual clause presence checks
    @property
    def has_governing_law(self) -> bool:
        return any(c.type == "Governing Law" for c in self.clauses)
    
    @property
    def has_payment_terms(self) -> bool:
        return any(c.type == "Payment Terms" for c in self.clauses)
    
    @property
    def has_liability_cap(self) -> bool:
        return any(c.type == "Liability Cap" for c in self.clauses)
    
    @property
    def has_termination_notice(self) -> bool:
        return any(c.type == "Termination Notice" for c in self.clauses)
    
    @property
    def has_confidentiality(self) -> bool:
        return any(c.type == "Confidentiality Period" for c in self.clauses)
    
    @property
    def has_renewal_terms(self) -> bool:
        return any(c.type == "Renewal Terms" for c in self.clauses)
    
    @property
    def has_indemnification(self) -> bool:
        return any(c.type == "Indemnification" for c in self.clauses)
    
    @property
    def has_force_majeure(self) -> bool:
        return any(c.type == "Force Majeure" for c in self.clauses)
    
    @property
    def clause_presence_summary(self) -> Dict[str, bool]:
        """Get summary of all clause presences"""
        return {
            "Governing Law": self.has_governing_law,
            "Payment Terms": self.has_payment_terms,
            "Liability Cap": self.has_liability_cap,
            "Termination Notice": self.has_termination_notice,
            "Confidentiality Period": self.has_confidentiality,
            "Renewal Terms": self.has_renewal_terms,
            "Indemnification": self.has_indemnification,
            "Force Majeure": self.has_force_majeure
        }
    
    # ========================================================================
    # RISK PROPERTIES
    # ========================================================================
    
    @property
    def risk_severity_summary(self) -> Dict[str, int]:
        """Get risk severity summary - OPTIMIZED"""
        summary = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for risk in self.risks:
            if risk.severity in summary:
                summary[risk.severity] += 1
        return summary
    
    @property
    def critical_risk_count(self) -> int:
        return self.risk_severity_summary.get('critical', 0)
    
    @property
    def high_risk_count(self) -> int:
        return self.risk_severity_summary.get('high', 0)
    
    @property
    def medium_risk_count(self) -> int:
        return self.risk_severity_summary.get('medium', 0)
    
    @property
    def low_risk_count(self) -> int:
        return self.risk_severity_summary.get('low', 0)
    
    @property
    def has_critical_risks(self) -> bool:
        return any(r.severity == 'critical' for r in self.risks)
    
    @property
    def has_high_risks(self) -> bool:
        return any(r.severity == 'high' for r in self.risks)
    
    @property
    def high_priority_risks(self) -> List[Risk]:
        return [r for r in self.risks if r.severity in ['critical', 'high']]
    
    @property
    def total_risk_score(self) -> int:
        """Calculate total risk score - weighted by severity"""
        weights = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
        return sum(weights.get(r.severity, 0) for r in self.risks)
    
    @property
    def risk_density(self) -> float:
        """Calculate risk density (risks per 1000 words)"""
        if self.word_count == 0:
            return 0
        return (self.risk_count / self.word_count) * 1000
    
    @property
    def risk_severity_distribution(self) -> Dict[str, float]:
        """Get risk severity distribution as percentages"""
        if not self.risks:
            return {}
        total = self.risk_count
        return {k: (v / total) * 100 for k, v in self.risk_severity_summary.items()}
    
    @property
    def risk_type_summary(self) -> Dict[str, int]:
        """Get risk type counts"""
        summary = {}
        for risk in self.risks:
            risk_type = risk.type.replace('_', ' ').title()
            summary[risk_type] = summary.get(risk_type, 0) + 1
        return summary
    
    # ========================================================================
    # HEALTH AND STATUS
    # ========================================================================
    
    @property
    def overall_health(self) -> str:
        """Determine overall health status"""
        if self.has_critical_risks:
            return 'critical'
        elif self.risk_count > 5:
            return 'warning'
        elif self.risk_count > 0:
            return 'scanned'
        else:
            return 'healthy'
    
    @property
    def health_score(self) -> int:
        """Calculate health score (0-100) - higher is better"""
        score = 100
        
        # Deduct for risks
        score -= self.critical_risk_count * 15
        score -= self.high_risk_count * 8
        score -= self.medium_risk_count * 4
        score -= self.low_risk_count * 2
        
        # Add for clause coverage
        score += self.clause_type_coverage * 0.2
        
        # Clamp to 0-100
        return max(0, min(100, int(score)))
    
    @property
    def health_label(self) -> str:
        """Get health status label"""
        labels = {
            'healthy': '✅ Healthy',
            'warning': '⚠️ Needs Review',
            'critical': '🔴 Critical Issues',
            'scanned': '📄 Scanned Document'
        }
        return labels.get(self.overall_health, 'Unknown')
    
    @property
    def health_color(self) -> str:
        """Get health status color"""
        from ..utils.constants import CONTRACT_STATUS_COLORS
        return CONTRACT_STATUS_COLORS.get(self.overall_health, '#94A3B8')
    
    @property
    def health_emoji(self) -> str:
        """Get health status emoji"""
        emojis = {
            'healthy': '✅',
            'warning': '⚠️',
            'critical': '🔴',
            'scanned': '📄'
        }
        return emojis.get(self.overall_health, '❓')
    
    @property
    def risk_burden(self) -> str:
        """Get risk burden description"""
        if self.total_risk_score == 0:
            return "No risks detected"
        elif self.total_risk_score < 5:
            return "Low risk burden"
        elif self.total_risk_score < 15:
            return "Moderate risk burden"
        elif self.total_risk_score < 30:
            return "High risk burden"
        else:
            return "Critical risk burden"
    
    # ========================================================================
    # SEARCH-SPECIFIC PROPERTIES
    # ========================================================================
    
    @property
    def searchable_text(self) -> str:
        """Get text optimized for search indexing"""
        # Remove common noise words and normalize
        text = self.text.lower()
        # Remove common contract boilerplate that might add noise
        text = re.sub(r'\b(whereas|hereinafter|whereby|thereof|thereto|therewith|herein|hereby|hereunder|hereinafter|hereinbefore)\b', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @property
    def search_keywords(self) -> List[str]:
        """Extract keywords for search optimization"""
        keywords = set()
        
        # Extract from clause types with synonyms
        clause_synonyms = {
            "Governing Law": ["jurisdiction", "law", "forum", "govern", "choice of law"],
            "Payment Terms": ["fee", "price", "cost", "invoice", "bill", "pay", "due", "net"],
            "Liability Cap": ["limit", "cap", "damages", "indemnity", "maximum", "exposure"],
            "Termination Notice": ["cancel", "end", "expire", "notice", "terminate", "period"],
            "Confidentiality Period": ["secret", "proprietary", "nondisclosure", "nda", "confidential"],
            "Renewal Terms": ["extend", "continue", "auto-renew", "rollover", "renew", "automatic"],
            "Indemnification": ["indemnify", "hold harmless", "defend", "protection"],
            "Force Majeure": ["act of god", "unforeseen", "excusable", "delay", "beyond control"]
        }
        
        for clause_type in self.clause_types:
            keywords.add(clause_type.lower())
            if clause_type in clause_synonyms:
                keywords.update(clause_synonyms[clause_type])
        
        # Add important terms from risk types
        for risk in self.risks:
            risk_type_lower = risk.type.replace('_', ' ').lower()
            keywords.add(risk_type_lower)
            
            # Add words from description
            if risk.description:
                words = risk.description.lower().split()
                keywords.update([w for w in words if len(w) > 3])
            
            # Add words from recommendation
            if risk.recommendation:
                words = risk.recommendation.lower().split()
                keywords.update([w for w in words if len(w) > 3])
        
        # Extract key terms from text (lightweight keyword extraction)
        text_words = self.text.lower().split()
        word_freq = {}
        for word in text_words:
            # Clean word
            word = re.sub(r'[^\w\s]', '', word)
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Add top frequency words as keywords
        stopwords = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'will', 'shall', 'any', 'all', 'our', 'its', 'may', 'but', 'not', 'are', 'was', 'were', 'has', 'have', 'been', 'being', 'can', 'could', 'would', 'should', 'must', 'such', 'each', 'other', 'among', 'within', 'without', 'upon', 'through'}
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:30]
        for word, _ in sorted_words:
            if word not in stopwords:
                keywords.add(word)
        
        return list(keywords)
    
    @property
    def search_metadata(self) -> Dict[str, Any]:
        """Get comprehensive metadata for search indexing"""
        return {
            'contract_id': self.id,
            'contract_name': self.name,
            'vendor': self.vendor,
            'file_type': self.file_type,
            'pages': self.pages,
            'clause_count': self.clause_count,
            'risk_count': self.risk_count,
            'health': self.overall_health,
            'health_score': self.health_score,
            'clause_types': self.clause_types,
            'risk_severity_summary': self.risk_severity_summary,
            'word_count': self.word_count,
            'upload_date': self.upload_date.isoformat(),
            'has_governing_law': self.has_governing_law,
            'has_payment_terms': self.has_payment_terms,
            'has_liability_cap': self.has_liability_cap,
            'has_termination_notice': self.has_termination_notice,
            'has_confidentiality': self.has_confidentiality,
            'has_renewal_terms': self.has_renewal_terms,
            'has_indemnification': self.has_indemnification,
            'has_force_majeure': self.has_force_majeure,
            'clause_type_coverage': self.clause_type_coverage,
            'total_risk_score': self.total_risk_score,
            'risk_density': self.risk_density,
            'clause_density': self.clause_density,
            'contract_value': self.contract_value,
            'is_scanned': self.is_scanned
        }
    
    @property
    def search_boost_score(self) -> float:
        """Calculate boost score for search ranking"""
        # Higher score = more relevant for search
        score = 1.0
        
        # Boost for clause coverage
        score += self.clause_type_coverage * 0.01
        
        # Boost for word count (more text = more searchable)
        if self.word_count > 1000:
            score += 0.1
        if self.word_count > 5000:
            score += 0.1
        
        # Boost for having many clauses
        if self.clause_count > 5:
            score += 0.1
        
        # Boost for health score
        if self.health_score > 80:
            score += 0.05
        
        return min(score, 2.0)  # Cap at 2.0
    
    # ========================================================================
    # QUERY METHODS
    # ========================================================================
    
    def get_clauses_by_type(self, clause_type: str) -> List[Clause]:
        """Get clauses by type - OPTIMIZED with list comprehension"""
        return [c for c in self.clauses if c.type == clause_type]
    
    def get_risks_by_severity(self, severity: str) -> List[Risk]:
        """Get risks by severity - OPTIMIZED with list comprehension"""
        return [r for r in self.risks if r.severity == severity]
    
    def get_high_priority_risks(self) -> List[Risk]:
        """Get high and critical risks - OPTIMIZED"""
        return [r for r in self.risks if r.severity in ['critical', 'high']]
    
    def has_clause_type(self, clause_type: str) -> bool:
        """Check if contract contains a specific clause type - O(n)"""
        return any(c.type == clause_type for c in self.clauses)
    
    def get_risk_severity_count(self, severity: str) -> int:
        """Get count of risks by severity - OPTIMIZED"""
        return len([r for r in self.risks if r.severity == severity])
    
    def get_clause_type_count(self, clause_type: str) -> int:
        """Get count of clauses by type - OPTIMIZED"""
        return len([c for c in self.clauses if c.type == clause_type])
    
    def search_in_contract(self, query: str) -> List[Tuple[int, str]]:
        """Search within the contract text and return matching lines with line numbers"""
        matches = []
        lines = self.text.split('\n')
        query_lower = query.lower()
        
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                matches.append((i + 1, line.strip()))
        
        return matches
    
    def get_clause_by_keyword(self, keyword: str) -> List[Clause]:
        """Find clauses containing a specific keyword"""
        return [c for c in self.clauses if keyword.lower() in c.text.lower()]
    
    def find_text_context(self, keyword: str, context_chars: int = 100) -> List[Dict[str, str]]:
        """Find keyword with surrounding context"""
        results = []
        text = self.text
        keyword_lower = keyword.lower()
        text_lower = text.lower()
        
        start = 0
        while True:
            pos = text_lower.find(keyword_lower, start)
            if pos == -1:
                break
            
            # Get context
            context_start = max(0, pos - context_chars)
            context_end = min(len(text), pos + len(keyword) + context_chars)
            
            results.append({
                'line_number': text[:pos].count('\n') + 1,
                'context': text[context_start:context_end],
                'match': text[pos:pos + len(keyword)],
                'start_pos': pos,
                'end_pos': pos + len(keyword)
            })
            
            start = pos + len(keyword)
        
        return results
    
    # ========================================================================
    # CONTRACT SUMMARY METHODS
    # ========================================================================
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the contract - OPTIMIZED"""
        return {
            'id': self.id,
            'name': self.name,
            'vendor': self.vendor,
            'file_type': self.file_type,
            'pages': self.pages,
            'word_count': self.word_count,
            'sentence_count': self.sentence_count,
            'paragraph_count': self.paragraph_count,
            'clause_count': self.clause_count,
            'risk_count': self.risk_count,
            'clause_types': self.clause_types,
            'clause_type_coverage': self.clause_type_coverage,
            'risk_severity_summary': self.risk_severity_summary,
            'total_risk_score': self.total_risk_score,
            'health_status': self.overall_health,
            'health_score': self.health_score,
            'health_label': self.health_label,
            'upload_date': self.upload_date.isoformat(),
            'contract_value': self.contract_value,
            'has_text': self.has_text,
            'is_scanned': self.is_scanned,
            'risk_density': self.risk_density,
            'clause_density': self.clause_density,
            'clause_presence': self.clause_presence_summary
        }
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get detailed analytics about the contract"""
        return {
            'basic_stats': {
                'word_count': self.word_count,
                'character_count': self.character_count,
                'sentence_count': self.sentence_count,
                'paragraph_count': self.paragraph_count,
                'line_count': self.line_count,
                'average_word_length': self.average_word_length
            },
            'clause_analytics': {
                'total_clauses': self.clause_count,
                'unique_types': len(self.clause_types),
                'clause_type_coverage': self.clause_type_coverage,
                'clause_density': self.clause_density,
                'clause_summary': self.clause_summary,
                'clause_presence': self.clause_presence_summary
            },
            'risk_analytics': {
                'total_risks': self.risk_count,
                'risk_severity_summary': self.risk_severity_summary,
                'total_risk_score': self.total_risk_score,
                'risk_density': self.risk_density,
                'risk_type_summary': self.risk_type_summary,
                'high_priority_count': len(self.high_priority_risks)
            },
            'health_analytics': {
                'overall_health': self.overall_health,
                'health_score': self.health_score,
                'health_label': self.health_label,
                'risk_burden': self.risk_burden
            }
        }
    
    # ========================================================================
    # MUTATION METHODS
    # ========================================================================
    
    def add_clause(self, clause: Clause) -> None:
        """Add a clause to the contract - O(1)"""
        self.clauses.append(clause)
    
    def add_risk(self, risk: Risk) -> None:
        """Add a risk to the contract - O(1)"""
        self.risks.append(risk)
    
    def add_clauses(self, clauses: List[Clause]) -> None:
        """Add multiple clauses at once - O(n)"""
        self.clauses.extend(clauses)
    
    def add_risks(self, risks: List[Risk]) -> None:
        """Add multiple risks at once - O(n)"""
        self.risks.extend(risks)
    
    def remove_clause(self, clause_id: str) -> bool:
        """Remove a clause by ID - O(n)"""
        for i, clause in enumerate(self.clauses):
            if clause.id == clause_id:
                self.clauses.pop(i)
                return True
        return False
    
    def remove_risk(self, risk_id: str) -> bool:
        """Remove a risk by ID - O(n)"""
        for i, risk in enumerate(self.risks):
            if risk.id == risk_id:
                self.risks.pop(i)
                return True
        return False
    
    def clear_clauses(self) -> None:
        """Remove all clauses - O(1)"""
        self.clauses.clear()
    
    def clear_risks(self) -> None:
        """Remove all risks - O(1)"""
        self.risks.clear()
    
    # ========================================================================
    # SERIALIZATION
    # ========================================================================
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization - OPTIMIZED"""
        return {
            "id": self.id,
            "name": self.name,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "upload_date": self.upload_date.isoformat(),
            "pages": self.pages,
            "file_hash": self.file_hash,
            "vendor": self.vendor,
            "contract_value": self.contract_value,
            "metadata": self.metadata,
            "clauses": [c.to_dict() for c in self.clauses],
            "risks": [r.to_dict() for r in self.risks],
            "is_scanned": self.is_scanned,
            "has_text": self.has_text,
            "clause_count": self.clause_count,
            "risk_count": self.risk_count,
            "clause_types": self.clause_types,
            "risk_severity_summary": self.risk_severity_summary,
            "total_risk_score": self.total_risk_score,
            "has_critical_risks": self.has_critical_risks,
            "overall_health": self.overall_health,
            "health_score": self.health_score,
            "health_label": self.health_label,
            "clause_summary": self.clause_summary,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "sentence_count": self.sentence_count,
            "paragraph_count": self.paragraph_count,
            "line_count": self.line_count,
            "average_word_length": self.average_word_length,
            "risk_density": self.risk_density,
            "clause_density": self.clause_density,
            "clause_type_coverage": self.clause_type_coverage,
            "has_governing_law": self.has_governing_law,
            "has_payment_terms": self.has_payment_terms,
            "has_liability_cap": self.has_liability_cap,
            "has_termination_notice": self.has_termination_notice,
            "has_confidentiality": self.has_confidentiality,
            "has_renewal_terms": self.has_renewal_terms,
            "has_indemnification": self.has_indemnification,
            "has_force_majeure": self.has_force_majeure,
            "clause_presence_summary": self.clause_presence_summary,
            "search_keywords": self.search_keywords,
            "search_metadata": self.search_metadata,
            "search_boost_score": self.search_boost_score,
            "analytics": self.get_analytics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contract':
        """Create contract from dictionary - OPTIMIZED"""
        # Handle upload_date conversion
        upload_date = data.get('upload_date')
        if isinstance(upload_date, str):
            upload_date = datetime.fromisoformat(upload_date)
        elif upload_date is None:
            upload_date = datetime.now()
            
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            file_type=data.get('file_type', ''),
            file_size=data.get('file_size', 0),
            upload_date=upload_date,
            text=data.get('text', ''),
            pages=data.get('pages', 0),
            file_hash=data.get('file_hash', ''),
            vendor=data.get('vendor', None),
            contract_value=data.get('contract_value', None),
            metadata=data.get('metadata', {}),
            is_scanned=data.get('is_scanned', False)
        )
    
    @classmethod
    def create_contract(cls, name: str, file_type: str, file_size: int, 
                       text: str = "", pages: int = 0,
                       vendor: Optional[str] = None) -> 'Contract':
        """Factory method to create a new contract with auto-generated ID"""
        return cls(
            id=f"contract_{uuid.uuid4().hex[:8]}",
            name=name,
            file_type=file_type,
            file_size=file_size,
            upload_date=datetime.now(),
            text=text,
            pages=pages,
            vendor=vendor
        )
    
    @classmethod
    def create_from_text(cls, name: str, text: str, 
                         file_type: str = "txt") -> 'Contract':
        """Create a contract from text content"""
        return cls(
            id=f"contract_{uuid.uuid4().hex[:8]}",
            name=name,
            file_type=file_type,
            file_size=len(text.encode('utf-8')),
            upload_date=datetime.now(),
            text=text,
            pages=len(text) // 2000 + 1,
            vendor=None
        )
    
    # ========================================================================
    # DUNDER METHODS
    # ========================================================================
    
    def __str__(self) -> str:
        """String representation - OPTIMIZED"""
        return f"Contract(name={self.name}, clauses={self.clause_count}, risks={self.risk_count}, health={self.overall_health})"
    
    def __repr__(self) -> str:
        """Repr representation - OPTIMIZED"""
        return f"Contract(id={self.id}, name={self.name}, file_type={self.file_type}, hash={self.file_hash[:8]}...)"
    
    def __eq__(self, other) -> bool:
        """Equality check based on id and file_hash - OPTIMIZED"""
        if not isinstance(other, Contract):
            return False
        return self.id == other.id and self.file_hash == other.file_hash
    
    def __hash__(self) -> int:
        """Hash based on id for use in sets/dicts - OPTIMIZED"""
        return hash(self.id)
    
    def __len__(self) -> int:
        """Return word count - OPTIMIZED"""
        return self.word_count
    
    def __bool__(self) -> bool:
        """Return True if contract has text - OPTIMIZED"""
        return self.has_text