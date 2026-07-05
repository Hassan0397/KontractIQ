"""
KontractIQ - Risk Scanner
Scans contracts for risk indicators with active learning 
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from ..models.risk import Risk
from ..models.contract import Contract
from ..utils.helpers import generate_id
from ..utils.constants import DEFAULT_RISK_RULES, RISK_SEVERITIES


class RiskScanner:
    """Scan contracts for risks with active learning"""
    
    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        """Initialize risk scanner with rules"""
        self.rules = rules or DEFAULT_RISK_RULES.copy()
        self._scan_stats = {
            'total_scanned': 0,
            'total_risks_found': 0,
            'last_scan_time': None,
            'rules_used': len(self.rules)
        }
    
    def scan_contract(self, contract: Contract) -> List[Risk]:
        """Scan a single contract for risks with enhanced detection"""
        risks = []
        text = contract.text.lower()
        text_length = len(text)
        
        for rule_key, rule in self.rules.items():
            pattern = rule.get('pattern', '')
            severity = rule.get('severity', 'low')
            description = rule.get('description', '')
            is_negative = rule.get('is_negative', False)
            
            if not pattern:
                continue
            
            try:
                if is_negative or pattern.startswith('(?i)(?!.*'):
                    # Negative lookahead - check if pattern is missing
                    if is_negative:
                        required_pattern = pattern
                    else:
                        required_pattern = pattern.replace('(?i)(?!.*', '').rstrip(')')
                    
                    if not re.search(required_pattern, text, re.IGNORECASE):
                        risk = self._create_risk(
                            contract, rule_key, severity, description
                        )
                        risks.append(risk)
                else:
                    # Positive match with context capture
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        clause_text = match.group(0)[:500]
                        # Get surrounding context for better analysis
                        start_pos = max(0, match.start() - 50)
                        end_pos = min(len(text), match.end() + 50)
                        context = text[start_pos:end_pos]
                        
                        risk = self._create_risk(
                            contract, rule_key, severity, description,
                            clause_text=clause_text,
                            context=context
                        )
                        risks.append(risk)
                        
            except re.error:
                # Skip invalid patterns
                continue
        
        # Update stats
        self._scan_stats['total_scanned'] += 1
        self._scan_stats['total_risks_found'] += len(risks)
        
        return risks
    
    def scan_all_contracts(self, contracts: List[Contract]) -> List[Risk]:
        """Scan all contracts for risks with progress tracking"""
        all_risks = []
        self._scan_stats['total_scanned'] = 0
        self._scan_stats['total_risks_found'] = 0
        
        for contract in contracts:
            risks = self.scan_contract(contract)
            all_risks.extend(risks)
        
        self._scan_stats['last_scan_time'] = datetime.now()
        self._scan_stats['rules_used'] = len(self.rules)
        
        return all_risks
    
    def _create_risk(
        self,
        contract: Contract,
        rule_key: str,
        severity: str,
        description: str,
        clause_text: Optional[str] = None,
        context: Optional[str] = None
    ) -> Risk:
        """Create a risk object with enhanced metadata"""
        risk_id = generate_id(f"{contract.id}_{rule_key}_{datetime.now().timestamp()}")
        
        return Risk(
            id=risk_id,
            type=rule_key,
            severity=severity,
            description=description,
            contract_id=contract.id,
            contract_name=contract.name,
            clause_text=clause_text or description,
            recommendation=self._get_recommendation(rule_key, severity),
            metadata={
                'scan_timestamp': datetime.now().isoformat(),
                'context': context,
                'rule_key': rule_key
            }
        )
    
    def _get_recommendation(self, rule_key: str, severity: str) -> str:
        """Get enhanced recommendation for a risk"""
        recommendations = {
            'unlimited_liability': (
                '🔴 CRITICAL: Cap liability to a reasonable amount (e.g., $1M-$5M) '
                'and consider adding a liability cap clause.'
            ),
            'auto_renewal': (
                '🟠 HIGH: Remove auto-renewal clause or add a 30-60 day '
                'termination notice period to maintain flexibility.'
            ),
            'no_termination_convenience': (
                '🟡 MEDIUM: Add termination for convenience clause with '
                'reasonable notice period (30-60 days).'
            ),
            'broad_indemnification': (
                '🟡 MEDIUM: Limit indemnification scope to negligence and '
                'cap the amount.'
            ),
            'short_payment_terms': (
                '🟡 MEDIUM: Extend payment terms to 30-45 days for better '
                'cash flow management.'
            ),
            'missing_governing_law': (
                '🔵 LOW: Add a governing law clause specifying the jurisdiction '
                'to avoid legal uncertainty.'
            ),
            'missing_confidentiality': (
                '🔵 LOW: Add a confidentiality period of at least 3-5 years '
                'to protect sensitive information.'
            )
        }
        
        default = f'📋 Review "{rule_key.replace("_", " ")}" clause for compliance.'
        return recommendations.get(rule_key, default)
    
    def add_custom_rule(
        self,
        rule_key: str,
        pattern: str,
        severity: str,
        description: str,
        is_negative: bool = False
    ):
        """Add a custom risk rule with validation"""
        if not rule_key or not pattern or not description:
            raise ValueError("All fields are required")
        
        # Validate regex pattern
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {str(e)}")
        
        # Validate severity
        if severity not in RISK_SEVERITIES:
            raise ValueError(f"Invalid severity: {severity}")
        
        self.rules[rule_key] = {
            'pattern': pattern,
            'severity': severity,
            'description': description,
            'is_negative': is_negative
        }
    
    def update_rule_severity(self, rule_key: str, new_severity: str):
        """Update severity of an existing rule"""
        if rule_key not in self.rules:
            raise KeyError(f"Rule '{rule_key}' not found")
        
        if new_severity not in RISK_SEVERITIES:
            raise ValueError(f"Invalid severity: {new_severity}")
        
        self.rules[rule_key]['severity'] = new_severity
    
    def remove_rule(self, rule_key: str):
        """Remove a risk rule"""
        if rule_key in self.rules:
            del self.rules[rule_key]
    
    def get_rule(self, rule_key: str) -> Optional[Dict[str, Any]]:
        """Get a specific rule"""
        return self.rules.get(rule_key)
    
    def export_rules(self) -> str:
        """Export rules as JSON with metadata"""
        export_data = {
            'version': '1.0',
            'exported_at': datetime.now().isoformat(),
            'total_rules': len(self.rules),
            'rules': self.rules
        }
        return json.dumps(export_data, indent=2)
    
    def import_rules(self, rules_json: str) -> bool:
        """Import rules from JSON with validation"""
        try:
            data = json.loads(rules_json)
            
            # Handle both formats (with or without wrapper)
            if 'rules' in data:
                rules = data['rules']
            else:
                rules = data
            
            if not isinstance(rules, dict):
                return False
            
            # Validate each rule
            for key, rule in rules.items():
                if not isinstance(rule, dict):
                    return False
                if 'pattern' not in rule or 'severity' not in rule:
                    return False
                if rule['severity'] not in RISK_SEVERITIES:
                    return False
                # Validate regex
                try:
                    re.compile(rule['pattern'])
                except re.error:
                    return False
            
            self.rules = rules
            self._scan_stats['rules_used'] = len(self.rules)
            return True
            
        except (json.JSONDecodeError, ValueError):
            return False
    
    def get_risk_summary(self, risks: List[Risk]) -> Dict[str, Any]:
        """Get comprehensive risk summary"""
        summary = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'total': len(risks)
        }
        
        for risk in risks:
            if risk.severity in summary:
                summary[risk.severity] += 1
        
        # Add additional metrics
        summary['critical_percentage'] = (summary['critical'] / summary['total'] * 100) if summary['total'] > 0 else 0
        summary['high_percentage'] = (summary['high'] / summary['total'] * 100) if summary['total'] > 0 else 0
        
        # Risk type distribution
        type_counts = {}
        for risk in risks:
            type_counts[risk.type] = type_counts.get(risk.type, 0) + 1
        summary['type_distribution'] = type_counts
        
        # Contracts affected
        summary['contracts_affected'] = len({r.contract_id for r in risks})
        
        return summary
    
    def get_scan_stats(self) -> Dict[str, Any]:
        """Get scanner statistics"""
        return self._scan_stats
    
    def reset_stats(self):
        """Reset scan statistics"""
        self._scan_stats = {
            'total_scanned': 0,
            'total_risks_found': 0,
            'last_scan_time': None,
            'rules_used': len(self.rules)
        }
    
    def get_risk_severity_distribution(self, risks: List[Risk]) -> Dict[str, float]:
        """Get severity distribution as percentages"""
        if not risks:
            return {}
        
        summary = self.get_risk_summary(risks)
        return {
            'critical': summary['critical_percentage'],
            'high': summary['high_percentage'],
            'medium': (summary['medium'] / summary['total'] * 100) if summary['total'] > 0 else 0,
            'low': (summary['low'] / summary['total'] * 100) if summary['total'] > 0 else 0
        }


