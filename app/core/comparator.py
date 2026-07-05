"""
KontractIQ - Version Comparator
smart diff highlighting and detailed change analysis
"""

import difflib
import re
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
from difflib import SequenceMatcher  # Added this import


class ContractComparator:
    """Enhanced compare two versions of a contract with smart analysis"""
    
    @staticmethod
    def compare(text_a: str, text_b: str, ignore_whitespace: bool = True) -> Dict[str, Any]:
        """
        Compare two contract texts with smart diff highlighting
        
        Args:
            text_a: Original text
            text_b: Revised text
            ignore_whitespace: Whether to ignore whitespace differences
            
        Returns:
            Dict with changes, stats, and metadata
        """
        # Preprocess texts
        if ignore_whitespace:
            text_a = ContractComparator._normalize_whitespace(text_a)
            text_b = ContractComparator._normalize_whitespace(text_b)
        
        # Split into lines
        lines_a = text_a.splitlines()
        lines_b = text_b.splitlines()
        
        # Create differ
        differ = difflib.Differ()
        diff = list(differ.compare(lines_a, lines_b))
        
        # Process differences with enhanced categorization
        changes = {
            'added': [],
            'removed': [],
            'modified': [],
            'unchanged': [],
            'context': []
        }
        
        # Track line positions for context
        position_a = 0
        position_b = 0
        
        i = 0
        while i < len(diff):
            line = diff[i]
            
            if line.startswith('+ '):
                changes['added'].append({
                    'line': line[2:],
                    'position': position_b,
                    'context': ContractComparator._get_context(diff, i, 'context')
                })
                position_b += 1
                
            elif line.startswith('- '):
                changes['removed'].append({
                    'line': line[2:],
                    'position': position_a,
                    'context': ContractComparator._get_context(diff, i, 'context')
                })
                position_a += 1
                
            elif line.startswith('? '):
                # Skip indicator lines
                pass
                
            else:
                changes['unchanged'].append({
                    'line': line[2:],
                    'position_a': position_a,
                    'position_b': position_b
                })
                position_a += 1
                position_b += 1
            
            i += 1
        
        # Find modified lines (same line with changes)
        modified = ContractComparator._find_modified_lines(diff)
        changes['modified'] = modified
        
        # Smart categorization of changes
        changes['categorized'] = ContractComparator._categorize_changes(changes)
        
        # Calculate advanced statistics
        stats = {
            'total_added': len(changes['added']),
            'total_removed': len(changes['removed']),
            'total_modified': len(changes['modified']),
            'total_changed': len(changes['added']) + len(changes['removed']) + len(changes['modified']),
            'total_unchanged': len(changes['unchanged']),
            'similarity': ContractComparator._calculate_similarity(text_a, text_b),
            'change_density': ContractComparator._calculate_change_density(changes, len(lines_a), len(lines_b)),
            'line_distribution': ContractComparator._calculate_line_distribution(changes),
            'change_impact': ContractComparator._calculate_change_impact(changes, text_a, text_b)
        }
        
        # Generate metadata
        metadata = {
            'lines_a': len(lines_a),
            'lines_b': len(lines_b),
            'char_count_a': len(text_a),
            'char_count_b': len(text_b),
            'significant_changes': stats['total_changed'] > 10,
            'version_difference': 'major' if stats['total_changed'] > 50 else 'moderate' if stats['total_changed'] > 10 else 'minor'
        }
        
        # Generate HTML diff
        diff_html = ContractComparator._generate_enhanced_diff_html(changes)
        
        # Generate smart insights
        insights = ContractComparator._generate_insights(stats, metadata)
        
        return {
            'changes': changes,
            'stats': stats,
            'metadata': metadata,
            'diff_html': diff_html,
            'insights': insights
        }
    
    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """Normalize whitespace for better comparison"""
        # Remove trailing whitespace
        lines = [line.rstrip() for line in text.splitlines()]
        # Remove empty lines at start and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        return '\n'.join(lines)
    
    @staticmethod
    def _get_context(diff: List[str], index: int, context_type: str) -> List[str]:
        """Get surrounding context lines"""
        context = []
        start = max(0, index - 3)
        end = min(len(diff), index + 4)
        
        for i in range(start, end):
            if i != index and not diff[i].startswith('? '):
                if diff[i].startswith('  '):
                    context.append(diff[i][2:])
                elif diff[i].startswith('+ ') or diff[i].startswith('- '):
                    context.append(diff[i][2:])
        
        return context[:3]  # Return up to 3 context lines
    
    @staticmethod
    def _find_modified_lines(diff: List[str]) -> List[Dict[str, str]]:
        """Find modified lines with smart detection"""
        modified = []
        i = 0
        
        while i < len(diff) - 1:
            if diff[i].startswith('- ') and i + 1 < len(diff) and diff[i+1].startswith('+ '):
                # Check if it's a true modification or just a move
                old_line = diff[i][2:]
                new_line = diff[i+1][2:]
                
                # Calculate similarity between old and new
                similarity = SequenceMatcher(None, old_line, new_line).ratio()
                
                modified.append({
                    'old': old_line,
                    'new': new_line,
                    'similarity': similarity,
                    'type': 'modified'
                })
                i += 2
                continue
            i += 1
        
        return modified
    
    @staticmethod
    def _categorize_changes(changes: Dict) -> Dict[str, List]:
        """Categorize changes by type and significance"""
        categorized = {
            'formatting': [],
            'minor': [],
            'significant': [],
            'major': []
        }
        
        # Categorize added lines
        for added in changes['added']:
            line = added['line']
            if len(line) < 10:
                categorized['formatting'].append(added)
            elif any(keyword in line.lower() for keyword in ['the', 'a', 'an', 'of', 'for']):
                categorized['minor'].append(added)
            else:
                categorized['significant'].append(added)
        
        # Categorize removed lines
        for removed in changes['removed']:
            line = removed['line']
            if len(line) < 10:
                categorized['formatting'].append(removed)
            elif any(keyword in line.lower() for keyword in ['the', 'a', 'an', 'of', 'for']):
                categorized['minor'].append(removed)
            else:
                categorized['significant'].append(removed)
        
        # Categorize modified lines
        for mod in changes['modified']:
            if mod['similarity'] > 0.9:
                categorized['minor'].append(mod)
            elif mod['similarity'] > 0.7:
                categorized['significant'].append(mod)
            else:
                categorized['major'].append(mod)
        
        return categorized
    
    @staticmethod
    def _calculate_similarity(text_a: str, text_b: str) -> float:
        """Calculate similarity between two texts with whitespace normalization"""
        # Remove extra whitespace for better similarity calculation
        text_a = ' '.join(text_a.split())
        text_b = ' '.join(text_b.split())
        sequence = difflib.SequenceMatcher(None, text_a, text_b)
        return sequence.ratio()
    
    @staticmethod
    def _calculate_change_density(changes: Dict, lines_a: int, lines_b: int) -> float:
        """Calculate change density (changes per 100 lines)"""
        total_lines = max(lines_a, lines_b, 1)
        total_changes = len(changes['added']) + len(changes['removed']) + len(changes['modified'])
        return (total_changes / total_lines) * 100
    
    @staticmethod
    def _calculate_line_distribution(changes: Dict) -> Dict[str, float]:
        """Calculate distribution of change types"""
        total = len(changes['added']) + len(changes['removed']) + len(changes['modified']) + len(changes['unchanged'])
        if total == 0:
            return {}
        
        return {
            'added': (len(changes['added']) / total) * 100,
            'removed': (len(changes['removed']) / total) * 100,
            'modified': (len(changes['modified']) / total) * 100,
            'unchanged': (len(changes['unchanged']) / total) * 100
        }
    
    @staticmethod
    def _calculate_change_impact(changes: Dict, text_a: str, text_b: str) -> Dict[str, Any]:
        """Calculate the impact of changes on the overall document"""
        total_lines_a = len(text_a.splitlines())
        total_lines_b = len(text_b.splitlines())
        
        # Calculate the percentage of the document that changed
        total_changed = len(changes['added']) + len(changes['removed']) + len(changes['modified'])
        max_lines = max(total_lines_a, total_lines_b, 1)
        
        impact_percent = (total_changed / max_lines) * 100
        
        return {
            'percent_changed': impact_percent,
            'level': 'low' if impact_percent < 10 else 'medium' if impact_percent < 30 else 'high',
            'description': f"{impact_percent:.1f}% of the document changed"
        }
    
    @staticmethod
    def _generate_enhanced_diff_html(changes: Dict) -> str:
        """Generate enhanced HTML for diff display with premium styling"""
        html = []
        
        # Header with stats
        html.append("""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        """)
        
        # Added lines
        if changes['added']:
            html.append('<div style="margin-bottom: 8px;"><strong style="color: #0D9488;">Added Lines</strong></div>')
            for added in changes['added'][:50]:
                html.append(f'''
                <div style="
                    background: #E6F7F5; 
                    padding: 2px 8px; 
                    margin: 1px 0; 
                    border-radius: 3px;
                    color: #0A7A70;
                    border-left: 3px solid #0D9488;
                    font-family: monospace;
                    font-size: 13px;
                ">
                    + {added['line']}
                </div>
                ''')
            if len(changes['added']) > 50:
                html.append(f'<div style="color: #94A3B8; font-size: 12px; margin: 4px 0;">... and {len(changes["added"]) - 50} more added lines</div>')
        
        # Removed lines
        if changes['removed']:
            html.append('<div style="margin: 12px 0 8px 0;"><strong style="color: #DC2626;">Removed Lines</strong></div>')
            for removed in changes['removed'][:50]:
                html.append(f'''
                <div style="
                    background: #FEE2E2; 
                    padding: 2px 8px; 
                    margin: 1px 0; 
                    border-radius: 3px;
                    color: #B91C1C;
                    text-decoration: line-through;
                    border-left: 3px solid #DC2626;
                    font-family: monospace;
                    font-size: 13px;
                ">
                    - {removed['line']}
                </div>
                ''')
            if len(changes['removed']) > 50:
                html.append(f'<div style="color: #94A3B8; font-size: 12px; margin: 4px 0;">... and {len(changes["removed"]) - 50} more removed lines</div>')
        
        # Modified lines
        if changes['modified']:
            html.append('<div style="margin: 12px 0 8px 0;"><strong style="color: #D97706;">Modified Lines</strong></div>')
            for mod in changes['modified'][:30]:
                html.append(f'''
                <div style="
                    background: #FEF3C7; 
                    padding: 4px 8px; 
                    margin: 2px 0; 
                    border-radius: 3px;
                    border-left: 3px solid #D97706;
                    font-family: monospace;
                    font-size: 13px;
                ">
                    <div style="color: #B91C1C; text-decoration: line-through;">- {mod['old']}</div>
                    <div style="color: #0A7A70;">+ {mod['new']}</div>
                    <div style="color: #94A3B8; font-size: 11px; margin-top: 2px;">
                        Similarity: {mod['similarity'] * 100:.0f}%
                    </div>
                </div>
                ''')
            if len(changes['modified']) > 30:
                html.append(f'<div style="color: #94A3B8; font-size: 12px; margin: 4px 0;">... and {len(changes["modified"]) - 30} more modified lines</div>')
        
        html.append('</div>')
        return '\n'.join(html)
    
    @staticmethod
    def _generate_insights(stats: Dict, metadata: Dict) -> List[str]:
        """Generate smart insights about the comparison"""
        insights = []
        
        # Change impact
        change_impact = stats.get('change_impact', {})
        if change_impact:
            insights.append(f"📊 {change_impact.get('description', 'Unknown impact')}")
        
        # Version difference
        version_diff = metadata.get('version_difference', 'unknown')
        diff_labels = {
            'minor': '🟢 Minor revisions detected - likely formatting or minor updates',
            'moderate': '🟡 Moderate revisions detected - substantive changes made',
            'major': '🔴 Major revisions detected - significant restructuring'
        }
        insights.append(diff_labels.get(version_diff, '📝 Revisions detected'))
        
        # Similarity
        similarity = stats.get('similarity', 0) * 100
        if similarity > 95:
            insights.append('✅ Very high similarity - contracts are nearly identical')
        elif similarity > 85:
            insights.append('✅ High similarity - minor differences only')
        elif similarity > 70:
            insights.append('⚠️ Moderate similarity - review differences carefully')
        else:
            insights.append('🔴 Low similarity - significant differences between versions')
        
        # Line distribution
        distribution = stats.get('line_distribution', {})
        if distribution:
            added_pct = distribution.get('added', 0)
            if added_pct > 30:
                insights.append(f'📝 High proportion of additions ({added_pct:.0f}% of lines)')
        
        return insights