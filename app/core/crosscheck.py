"""
KontractIQ - Cross-Contract Inconsistency Detection 
Finds numeric and date inconsistencies across contracts with advanced analytics
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from ..models.contract import Contract


@dataclass
class InconsistencyFinding:
    """Data class for inconsistency findings"""
    type: str
    values: List[str]
    most_common: Dict[str, Any]
    deviations: List[str]
    recommendation: str
    severity: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)


class CrossCheckEngine:
    """Detect inconsistencies across contracts with advanced analytics"""
    
    # State patterns for governing law detection
    US_STATES = r'(?:california|new york|delaware|texas|florida|illinois|pennsylvania|ohio|georgia|north carolina|michigan|new jersey|virginia|washington|massachusetts|arizona|tennessee|indiana|missouri|maryland|wisconsin|colorado|minnesota|south carolina|alabama|louisiana|kentucky|oregon|oklahoma|connecticut|iowa|mississippi|arkansas|kansas|utah|nevada|west virginia|nebraska|idaho|new mexico|maine|new hampshire|hawaii|rhode island|montana|south dakota|north dakota|alaska|vermont|wyoming)'
    
    # Severity weights for scoring
    SEVERITY_WEIGHTS = {
        'critical': 10,
        'high': 7,
        'medium': 4,
        'low': 1
    }
    
    @staticmethod
    def analyze(contracts: List[Contract]) -> Dict[str, Any]:
        """
        Analyze all contracts for inconsistencies with enhanced analytics
        
        Args:
            contracts: List of Contract objects
            
        Returns:
            Dict with analysis results including findings, statistics, and recommendations
        """
        if len(contracts) < 2:
            return {
                'error': 'Need at least 2 contracts for cross-check analysis',
                'findings': [],
                'statistics': {}
            }
        
        findings = []
        statistics = {
            'total_contracts': len(contracts),
            'total_clauses': sum(c.clause_count for c in contracts),
            'total_risks': sum(c.risk_count for c in contracts),
            'contracts_with_issues': 0,
            'severity_distribution': defaultdict(int)
        }
        
        # Check each inconsistency type
        checkers = [
            ('Payment Terms', CrossCheckEngine._check_payment_terms),
            ('Liability Cap', CrossCheckEngine._check_liability_caps),
            ('Termination Notice', CrossCheckEngine._check_termination_notice),
            ('Governing Law', CrossCheckEngine._check_governing_law),
            ('Confidentiality Period', CrossCheckEngine._check_confidentiality_period),
            ('Renewal Terms', CrossCheckEngine._check_renewal_terms)
        ]
        
        for check_name, checker_func in checkers:
            finding = checker_func(contracts)
            if finding:
                findings.append(finding)
                # Track contracts with issues
                statistics['contracts_with_issues'] += len(finding.get('deviations', []))
                # Track severity
                severity = finding.get('severity', 'medium')
                statistics['severity_distribution'][severity] += 1
        
        # Calculate overall severity
        overall_severity = CrossCheckEngine._calculate_overall_severity(findings)
        
        return {
            'findings': findings,
            'statistics': statistics,
            'total_contracts': len(contracts),
            'overall_severity': overall_severity,
            'recommendations': CrossCheckEngine._generate_global_recommendations(findings, contracts)
        }
    
    @staticmethod
    def _extract_values(text: str, pattern: str) -> List[str]:
        """Extract values from text using pattern with improved matching"""
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        return [m.strip() for m in matches if m and m.strip()]
    
    @staticmethod
    def _find_most_common(values: List[str]) -> Dict[str, Any]:
        """Find the most common value and its frequency with statistics"""
        if not values:
            return {'value': None, 'count': 0, 'percentage': 0, 'distribution': {}}
        
        counter = Counter(values)
        most_common = counter.most_common(1)[0]
        
        return {
            'value': most_common[0],
            'count': most_common[1],
            'percentage': (most_common[1] / len(values)) * 100,
            'distribution': dict(counter),
            'unique_count': len(counter),
            'total_count': len(values)
        }
    
    @staticmethod
    def _determine_severity(deviation_percentage: float, value_count: int) -> str:
        """Determine severity based on deviation percentage and value count"""
        if deviation_percentage > 50:
            return 'critical'
        elif deviation_percentage > 25:
            return 'high'
        elif deviation_percentage > 10:
            return 'medium'
        elif deviation_percentage > 0:
            return 'low'
        return 'none'
    
    @staticmethod
    def _check_payment_terms(contracts: List[Contract]) -> Optional[Dict[str, Any]]:
        """Check payment term inconsistencies with advanced analysis"""
        payment_terms = []
        contract_values = {}
        
        for contract in contracts:
            # Multiple patterns for payment terms
            patterns = [
                r'(\d+)\s*(?:days|day)\s*(?:of|from|after|following)?',
                r'net\s*(\d+)',
                r'payment\s*(?:terms|period|due)\s*(?:of|:)?\s*(\d+)\s*(?:days|day)',
                r'payable\s*(?:within|in)\s*(\d+)\s*(?:days|day)'
            ]
            
            terms = []
            for pattern in patterns:
                matches = CrossCheckEngine._extract_values(contract.text, pattern)
                terms.extend(matches)
            
            if terms:
                # Take the most reasonable payment term (first or most frequent)
                term = terms[0]
                payment_terms.append(term)
                contract_values[contract.name] = term
        
        if len(set(payment_terms)) > 1:
            most_common = CrossCheckEngine._find_most_common(payment_terms)
            deviations = [name for name, value in contract_values.items() if value != most_common['value']]
            deviation_percentage = (len(deviations) / len(contracts)) * 100 if contracts else 0
            
            return {
                'type': 'Payment Terms',
                'values': sorted(list(set(payment_terms))),
                'most_common': most_common,
                'deviations': deviations,
                'severity': CrossCheckEngine._determine_severity(deviation_percentage, len(set(payment_terms))),
                'recommendation': f"Standardize payment terms to {most_common['value']} days to ensure consistent cash flow. "
                                 f"{len(deviations)} contract(s) deviate from the norm.",
                'metadata': {
                    'deviation_percentage': deviation_percentage,
                    'total_contracts': len(contracts),
                    'deviating_count': len(deviations)
                }
            }
        return None
    
    @staticmethod
    def _check_liability_caps(contracts: List[Contract]) -> Optional[Dict[str, Any]]:
        """Check liability cap inconsistencies with enhanced analysis"""
        liability_caps = []
        contract_values = {}
        
        for contract in contracts:
            patterns = [
                r'(?:\$|USD|dollars)\s*([\d,]+\.?\d*)\s*(?:million|M|billion|B)?',
                r'liability\s*(?:cap|limit|is\s+limited\s+to)\s*(?:\$|USD|dollars)?\s*([\d,]+\.?\d*)\s*(?:million|M|billion|B)?',
                r'maximum\s+liability\s*(?:\$|USD|dollars)?\s*([\d,]+\.?\d*)\s*(?:million|M|billion|B)?',
                r'unlimited\s*liability'
            ]
            
            caps = []
            for pattern in patterns:
                matches = CrossCheckEngine._extract_values(contract.text, pattern)
                if matches:
                    # Check if it's unlimited
                    if 'unlimited' in str(matches[0]).lower():
                        caps.append('Unlimited')
                    else:
                        caps.append(matches[0])
            
            if caps:
                cap = caps[0]
                # Normalize value
                if 'Unlimited' in cap:
                    liability_caps.append('Unlimited')
                    contract_values[contract.name] = 'Unlimited'
                else:
                    try:
                        # Clean and format
                        cap_clean = cap.replace(',', '')
                        if 'million' in contract.text.lower() or 'm' in contract.text.lower():
                            value = float(cap_clean) * 1000000
                        elif 'billion' in contract.text.lower() or 'b' in contract.text.lower():
                            value = float(cap_clean) * 1000000000
                        else:
                            value = float(cap_clean)
                        
                        formatted = f"${value:,.0f}" if value < 1000000 else f"${value/1000000:.1f}M"
                        liability_caps.append(formatted)
                        contract_values[contract.name] = formatted
                    except:
                        liability_caps.append(cap)
                        contract_values[contract.name] = cap
        
        if len(set(liability_caps)) > 1:
            most_common = CrossCheckEngine._find_most_common(liability_caps)
            deviations = [name for name, value in contract_values.items() if value != most_common['value']]
            deviation_percentage = (len(deviations) / len(contracts)) * 100 if contracts else 0
            
            return {
                'type': 'Liability Cap',
                'values': sorted(list(set(liability_caps)), key=lambda x: (x == 'Unlimited', x)),
                'most_common': most_common,
                'deviations': deviations,
                'severity': CrossCheckEngine._determine_severity(deviation_percentage, len(set(liability_caps))),
                'recommendation': f"Consider standardizing liability caps to {most_common['value']}. "
                                 f"{len(deviations)} contract(s) have different caps that may create exposure.",
                'metadata': {
                    'deviation_percentage': deviation_percentage,
                    'total_contracts': len(contracts),
                    'deviating_count': len(deviations),
                    'has_unlimited': 'Unlimited' in liability_caps
                }
            }
        return None
    
    @staticmethod
    def _check_termination_notice(contracts: List[Contract]) -> Optional[Dict[str, Any]]:
        """Check termination notice inconsistencies"""
        notice_periods = []
        contract_values = {}
        
        for contract in contracts:
            patterns = [
                r'(\d+)\s*(?:days|day)\s*(?:notice|prior\s+notice|written\s+notice)',
                r'(?:termination|terminate)\s*(?:notice|period)\s*(?:of|:)?\s*(\d+)\s*(?:days|day)',
                r'notice\s+period\s*(?:of|:)?\s*(\d+)\s*(?:days|day)'
            ]
            
            for pattern in patterns:
                notices = CrossCheckEngine._extract_values(contract.text, pattern)
                if notices:
                    notice = notices[0]
                    notice_periods.append(notice)
                    contract_values[contract.name] = notice
                    break
        
        if len(set(notice_periods)) > 1:
            most_common = CrossCheckEngine._find_most_common(notice_periods)
            deviations = [name for name, value in contract_values.items() if value != most_common['value']]
            deviation_percentage = (len(deviations) / len(contracts)) * 100 if contracts else 0
            
            return {
                'type': 'Termination Notice',
                'values': sorted(list(set(notice_periods)), key=lambda x: int(x) if x.isdigit() else 0),
                'most_common': most_common,
                'deviations': deviations,
                'severity': CrossCheckEngine._determine_severity(deviation_percentage, len(set(notice_periods))),
                'recommendation': f"Standardize notice period to {most_common['value']} days for consistency. "
                                 f"Different notice periods may create confusion during termination.",
                'metadata': {
                    'deviation_percentage': deviation_percentage,
                    'total_contracts': len(contracts),
                    'deviating_count': len(deviations)
                }
            }
        return None
    
    @staticmethod
    def _check_governing_law(contracts: List[Contract]) -> Optional[Dict[str, Any]]:
        """Check governing law inconsistencies with 50-state coverage"""
        laws = []
        contract_values = {}
        
        for contract in contracts:
            pattern = f'(?:governing law|choice of law|governing jurisdiction)[\s\S]{{0,300}}?({CrossCheckEngine.US_STATES})'
            matches = CrossCheckEngine._extract_values(contract.text, pattern)
            
            if matches:
                law = matches[0].strip().title()
                laws.append(law)
                contract_values[contract.name] = law
        
        if len(set(laws)) > 1:
            most_common = CrossCheckEngine._find_most_common(laws)
            deviations = [name for name, value in contract_values.items() if value != most_common['value']]
            deviation_percentage = (len(deviations) / len(contracts)) * 100 if contracts else 0
            
            return {
                'type': 'Governing Law',
                'values': sorted(list(set(laws))),
                'most_common': most_common,
                'deviations': deviations,
                'severity': 'medium' if len(set(laws)) > 3 else 'low',
                'recommendation': f"Standardize governing law to {most_common['value']} to ensure consistent legal interpretation. "
                                 f"{len(deviations)} contract(s) have different governing laws.",
                'metadata': {
                    'deviation_percentage': deviation_percentage,
                    'total_contracts': len(contracts),
                    'deviating_count': len(deviations),
                    'unique_laws': len(set(laws))
                }
            }
        return None
    
    @staticmethod
    def _check_confidentiality_period(contracts: List[Contract]) -> Optional[Dict[str, Any]]:
        """Check confidentiality period inconsistencies"""
        periods = []
        contract_values = {}
        
        for contract in contracts:
            patterns = [
                r'confidentiality\s*(?:period|term|duration)\s*(?:of|:)?\s*(\d+)\s*(?:years|year)',
                r'confidential\s*(?:information|obligations)\s*(?:survive|remain)\s*(?:for)?\s*(\d+)\s*(?:years|year)',
                r'(\d+)\s*(?:years|year)\s*(?:confidentiality|confidential)'
            ]
            
            for pattern in patterns:
                matches = CrossCheckEngine._extract_values(contract.text, pattern)
                if matches:
                    period = matches[0]
                    periods.append(period)
                    contract_values[contract.name] = f"{period} years"
                    break
        
        if len(set(periods)) > 1:
            most_common = CrossCheckEngine._find_most_common(periods)
            deviations = [name for name, value in contract_values.items() if value != f"{most_common['value']} years"]
            deviation_percentage = (len(deviations) / len(contracts)) * 100 if contracts else 0
            
            return {
                'type': 'Confidentiality Period',
                'values': sorted(list(set(periods)), key=lambda x: int(x) if x.isdigit() else 0),
                'most_common': {'value': f"{most_common['value']} years", 'percentage': most_common['percentage']},
                'deviations': deviations,
                'severity': CrossCheckEngine._determine_severity(deviation_percentage, len(set(periods))),
                'recommendation': f"Standardize confidentiality period to {most_common['value']} years. "
                                 f"Different periods may create gaps in IP protection.",
                'metadata': {
                    'deviation_percentage': deviation_percentage,
                    'total_contracts': len(contracts),
                    'deviating_count': len(deviations)
                }
            }
        return None
    
    @staticmethod
    def _check_renewal_terms(contracts: List[Contract]) -> Optional[Dict[str, Any]]:
        """Check renewal term inconsistencies"""
        renewal_patterns = []
        contract_values = {}
        
        for contract in contracts:
            patterns = [
                r'(?:auto-?renew|automatic\s+renewal)\s*(?:for|after)?\s*(\d+)\s*(?:years|year)?',
                r'renewal\s*(?:term|period)\s*(?:of|:)?\s*(\d+)\s*(?:years|year)?'
            ]
            
            found = False
            for pattern in patterns:
                matches = CrossCheckEngine._extract_values(contract.text, pattern)
                if matches:
                    period = matches[0] if matches[0] else "1"
                    renewal_patterns.append(period)
                    contract_values[contract.name] = f"{period} years" if period.isdigit() else "Auto-renewal"
                    found = True
                    break
            
            if not found:
                # Check if auto-renewal exists without specific period
                if re.search(r'(?:auto-?renew|automatic\s+renewal)', contract.text, re.IGNORECASE):
                    renewal_patterns.append("Auto-renewal")
                    contract_values[contract.name] = "Auto-renewal"
        
        if len(set(renewal_patterns)) > 1:
            most_common = CrossCheckEngine._find_most_common(renewal_patterns)
            deviations = [name for name, value in contract_values.items() if value != (f"{most_common['value']} years" if most_common['value'].isdigit() else "Auto-renewal")]
            deviation_percentage = (len(deviations) / len(contracts)) * 100 if contracts else 0
            
            return {
                'type': 'Renewal Terms',
                'values': sorted(list(set(renewal_patterns))),
                'most_common': most_common,
                'deviations': deviations,
                'severity': 'high' if 'Auto-renewal' in renewal_patterns and len(set(renewal_patterns)) > 1 else 'medium',
                'recommendation': f"Standardize renewal terms to {most_common['value']} years. "
                                 f"Auto-renewal without clear terms can lead to unexpected commitments.",
                'metadata': {
                    'deviation_percentage': deviation_percentage,
                    'total_contracts': len(contracts),
                    'deviating_count': len(deviations),
                    'has_auto_renewal': 'Auto-renewal' in renewal_patterns
                }
            }
        return None
    
    @staticmethod
    def _calculate_overall_severity(findings: List[Dict[str, Any]]) -> str:
        """Calculate overall severity based on all findings"""
        if not findings:
            return 'none'
        
        severity_counts = defaultdict(int)
        for finding in findings:
            severity = finding.get('severity', 'medium')
            severity_counts[severity] += 1
        
        # Weighted scoring
        scores = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1
        }
        
        total_score = sum(scores.get(s, 0) * count for s, count in severity_counts.items())
        
        if total_score > 15:
            return 'critical'
        elif total_score > 8:
            return 'high'
        elif total_score > 3:
            return 'medium'
        elif total_score > 0:
            return 'low'
        return 'none'
    
    @staticmethod
    def _generate_global_recommendations(findings: List[Dict[str, Any]], contracts: List[Contract]) -> List[str]:
        """Generate global recommendations based on all findings"""
        recommendations = []
        
        if not findings:
            recommendations.append("✅ All contracts are consistent. No action required.")
            return recommendations
        
        # Group findings by severity
        critical_findings = [f for f in findings if f.get('severity') == 'critical']
        high_findings = [f for f in findings if f.get('severity') == 'high']
        
        if critical_findings:
            recommendations.append(f"🚨 Address {len(critical_findings)} critical inconsistency issue(s) immediately")
        
        if high_findings:
            recommendations.append(f"⚠️ Review {len(high_findings)} high-priority inconsistency issue(s)")
        
        # Add specific recommendations for each finding
        for finding in findings:
            if finding.get('severity') in ['critical', 'high']:
                deviation_count = len(finding.get('deviations', []))
                recommendations.append(
                    f"• {finding['type']}: {deviation_count} contract(s) deviate from standard "
                    f"({finding.get('most_common', {}).get('value', 'N/A')})"
                )
        
        # Add general recommendations
        total_deviations = sum(len(f.get('deviations', [])) for f in findings)
        if total_deviations > len(contracts):
            recommendations.append("📋 Consider creating standardized contract templates")
        
        if len(findings) > 3:
            recommendations.append("🔄 Schedule regular cross-check reviews for ongoing consistency")
        
        return recommendations[:5]  # Limit to top 5 recommendations