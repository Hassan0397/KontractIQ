"""
KontractIQ - Premium Report Generator 
"""

import io
from datetime import datetime
from typing import List, Dict, Any, Optional
import jinja2


class UltraPremiumReportGenerator:
    """
    KontractIQ - Ultra-Premium Report Generator v6.0
    HTML ONLY - Responsive, Premium, Perfect Alignment
    """
    
    # Ultra-Premium Color Palette
    BRAND_COLORS = {
        'primary': '#0A1628',
        'primary_light': '#1B3A5C',
        'primary_lighter': '#2C5F8A',
        'secondary': '#4A7FA5',
        'accent': '#6B9FC7',
        'gold': '#C9A84C',
        'gold_light': '#F0D080',
        'gold_dark': '#A8893A',
        'success': '#0D9488',
        'success_light': '#E6F7F5',
        'warning': '#D97706',
        'warning_light': '#FFFBEB',
        'danger': '#DC2626',
        'danger_light': '#FEF2F2',
        'info': '#3B82F6',
        'info_light': '#EFF6FF',
        'dark_text': '#0A1628',
        'medium_text': '#475569',
        'light_text': '#94A3B8',
        'border': '#E2E8F0',
        'card_bg': '#F8FAFC',
        'white': '#FFFFFF',
    }
    
    def __init__(self):
        """Initialize ultra-premium report generator"""
        pass
    
    def generate_html_report(self, data: Dict[str, Any], report_type: str = 'full_analysis') -> str:
        """Generate responsive HTML report with perfect alignment"""
        
        total_contracts = data.get('total_contracts', 0)
        total_clauses = data.get('total_clauses', 0)
        total_risks = data.get('total_risks', 0)
        critical_risks = data.get('critical_risks', 0)
        
        # Calculate health metrics
        if total_contracts > 0:
            avg_risks_per_contract = total_risks / total_contracts
            if avg_risks_per_contract == 0:
                health_status = "Excellent"
                health_color = "#0D9488"
                health_icon = "🌟"
            elif avg_risks_per_contract < 1:
                health_status = "Good"
                health_color = "#3B82F6"
                health_icon = "✅"
            elif avg_risks_per_contract < 3:
                health_status = "Fair"
                health_color = "#D97706"
                health_icon = "⚠️"
            else:
                health_status = "Needs Attention"
                health_color = "#DC2626"
                health_icon = "🚨"
        else:
            health_status = "No Data"
            health_color = "#94A3B8"
            health_icon = "—"
        
        if total_contracts > 0 and total_clauses > 0:
            avg_clauses_per_contract = total_clauses / total_contracts
            clause_coverage = min(100, (total_clauses / (total_contracts * 8)) * 100)
        else:
            avg_clauses_per_contract = 0
            clause_coverage = 0
        
        risk_summary = data.get('risk_summary', {'critical': 0, 'high': 0, 'medium': 0, 'low': 0})
        
        clauses = data.get('clauses', [])
        clause_types = {}
        for clause in clauses:
            ctype = clause.get('type', 'Unknown')
            clause_types[ctype] = clause_types.get(ctype, 0) + 1
        
        most_common_clause = max(clause_types.items(), key=lambda x: x[1])[0] if clause_types else "None"
        unique_clause_types = len(clause_types)
        
        max_risk_count = max(risk_summary.values()) if risk_summary and any(risk_summary.values()) else 1
        
        # Title mapping
        title_map = {
            'full_analysis': 'Full Analysis Report',
            'risk_summary': 'Risk Summary Report',
            'clause_comparison': 'Clause Comparison Report',
            'executive_summary': 'Executive Summary Report'
        }
        report_title = title_map.get(report_type, 'Analysis Report')
        
        # Get current date/time
        now = datetime.now()
        generated_date = now.strftime('%B %d, %Y at %I:%M %p')
        report_id = f"KIQ-{now.strftime('%Y%m%d')}-{hash(str(total_contracts)) % 10000:04d}"
        
        template_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>KontractIQ — {{ report_title }}</title>
            <style>
                /* ============================================================
                   ULTRA PREMIUM STYLES - PERFECT ALIGNMENT
                   ============================================================ */
                
                /* CSS Variables */
                :root {
                    --primary: #0A1628;
                    --primary-light: #1B3A5C;
                    --primary-lighter: #2C5F8A;
                    --secondary: #4A7FA5;
                    --gold: #C9A84C;
                    --gold-light: #F0D080;
                    --gold-dark: #A8893A;
                    --success: #0D9488;
                    --warning: #D97706;
                    --danger: #DC2626;
                    --info: #3B82F6;
                    --dark-text: #0A1628;
                    --medium-text: #475569;
                    --light-text: #94A3B8;
                    --border: #E2E8F0;
                    --white: #FFFFFF;
                }
                
                * { margin: 0; padding: 0; box-sizing: border-box; }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: #F0F4F8;
                    padding: 30px 16px;
                    color: var(--dark-text);
                    line-height: 1.6;
                    min-height: 100vh;
                }
                
                /* ============================================================
                   CONTAINER
                   ============================================================ */
                .report-container {
                    max-width: 1100px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.92);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border-radius: 24px;
                    overflow: hidden;
                    box-shadow: 0 30px 80px rgba(10, 22, 40, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                
                /* ============================================================
                   HERO HEADER
                   ============================================================ */
                .hero-header {
                    background: linear-gradient(135deg, #0A1628 0%, #1B3A5C 40%, #2C5F8A 100%);
                    padding: 40px 48px 28px 48px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }
                
                .hero-header::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #C9A84C, #F0D080, #C9A84C);
                    box-shadow: 0 0 30px rgba(201, 168, 76, 0.3);
                }
                
                .brand-name {
                    font-size: 34px;
                    font-weight: 700;
                    color: #FFFFFF;
                    letter-spacing: 3px;
                    position: relative;
                    z-index: 1;
                }
                
                .brand-name .gold-dot { color: #C9A84C; }
                
                .brand-tagline {
                    font-size: 14px;
                    color: #D4E4F4;
                    margin-top: 2px;
                    font-weight: 300;
                    letter-spacing: 2px;
                    position: relative;
                    z-index: 1;
                }
                
                .report-meta {
                    color: #8CB5D4;
                    font-size: 11px;
                    margin-top: 10px;
                    display: flex;
                    justify-content: center;
                    gap: 16px;
                    flex-wrap: wrap;
                    position: relative;
                    z-index: 1;
                }
                
                .report-meta span {
                    background: rgba(255, 255, 255, 0.06);
                    padding: 4px 14px;
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }
                
                /* ============================================================
                   REPORT BODY
                   ============================================================ */
                .report-body {
                    padding: 32px 48px 36px 48px;
                }
                
                .report-title-section {
                    text-align: center;
                    margin-bottom: 28px;
                }
                
                .report-title {
                    font-size: 26px;
                    font-weight: 700;
                    color: var(--dark-text);
                    letter-spacing: -0.5px;
                    display: inline-block;
                    position: relative;
                }
                
                .report-title::after {
                    content: '';
                    position: absolute;
                    bottom: -4px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 50px;
                    height: 3px;
                    background: linear-gradient(90deg, #C9A84C, #F0D080);
                    border-radius: 2px;
                }
                
                .report-subtitle {
                    font-size: 13px;
                    color: var(--medium-text);
                    margin-top: 8px;
                    font-weight: 300;
                }
                
                /* ============================================================
                   METRIC GRID - PERFECT ALIGNMENT
                   ============================================================ */
                .metric-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 14px;
                    margin: 20px 0 28px 0;
                }
                
                .metric-card {
                    background: rgba(255, 255, 255, 0.7);
                    backdrop-filter: blur(10px);
                    border-radius: 14px;
                    padding: 18px 12px 16px 12px;
                    text-align: center;
                    border: 1px solid rgba(255, 255, 255, 0.5);
                    box-shadow: 0 4px 20px rgba(10, 22, 40, 0.04);
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 130px;
                }
                
                .metric-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3.5px;
                    background: linear-gradient(90deg, #2C5F8A, #4A7FA5);
                    opacity: 0.6;
                    transition: all 0.3s ease;
                }
                
                .metric-card:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 12px 40px rgba(10, 22, 40, 0.10);
                    border-color: rgba(201, 168, 76, 0.2);
                }
                
                .metric-card:hover::before {
                    background: linear-gradient(90deg, #C9A84C, #F0D080);
                    opacity: 1;
                }
                
                .metric-card .metric-icon {
                    font-size: 24px;
                    display: block;
                    margin-bottom: 4px;
                    line-height: 1.2;
                }
                
                .metric-card .metric-value {
                    font-size: 34px;
                    font-weight: 700;
                    color: var(--dark-text);
                    line-height: 1.2;
                    letter-spacing: -0.5px;
                }
                
                .metric-card .metric-label {
                    font-size: 11px;
                    color: var(--medium-text);
                    margin-top: 4px;
                    font-weight: 500;
                    line-height: 1.3;
                }
                
                .metric-card .metric-trend {
                    font-size: 9px;
                    font-weight: 600;
                    margin-top: 6px;
                    display: inline-block;
                    padding: 2px 10px;
                    border-radius: 12px;
                    line-height: 1.4;
                }
                
                .metric-card .metric-trend.up { background: #E6F7F5; color: #0D9488; }
                .metric-card .metric-trend.down { background: #FEF2F2; color: #DC2626; }
                .metric-card .metric-trend.neutral { background: #F0F4F8; color: var(--medium-text); }
                
                .metric-card.blue::before { background: linear-gradient(90deg, #2C5F8A, #4A7FA5); }
                .metric-card.green::before { background: linear-gradient(90deg, #0D9488, #4ADE80); }
                .metric-card.orange::before { background: linear-gradient(90deg, #D97706, #F59E0B); }
                .metric-card.red::before { background: linear-gradient(90deg, #DC2626, #F87171); }
                
                /* ============================================================
                   SECTIONS
                   ============================================================ */
                .section { margin: 24px 0 14px 0; }
                
                .section-heading {
                    font-size: 20px;
                    font-weight: 700;
                    color: var(--dark-text);
                    margin-bottom: 12px;
                    padding-bottom: 8px;
                    border-bottom: 2px solid var(--border);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    position: relative;
                    flex-wrap: wrap;
                }
                
                .section-heading::after {
                    content: '';
                    position: absolute;
                    bottom: -2px;
                    left: 0;
                    width: 50px;
                    height: 2px;
                    background: linear-gradient(90deg, #C9A84C, #F0D080);
                }
                
                .section-heading .section-badge {
                    font-size: 10px;
                    background: linear-gradient(135deg, #0A1628, #1B3A5C);
                    color: white;
                    padding: 2px 12px;
                    border-radius: 20px;
                    font-weight: 500;
                    margin-left: auto;
                    letter-spacing: 0.3px;
                    white-space: nowrap;
                }
                
                .section-heading .section-badge.gold {
                    background: linear-gradient(135deg, #C9A84C, #F0D080);
                    color: #0A1628;
                }
                
                .sub-section-heading {
                    font-size: 15px;
                    font-weight: 600;
                    color: #2C5F8A;
                    margin: 16px 0 8px 0;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }
                
                /* ============================================================
                   TABLES
                   ============================================================ */
                .table-wrapper {
                    overflow-x: auto;
                    margin: 10px 0 14px 0;
                    border-radius: 12px;
                    border: 1px solid var(--border);
                    background: white;
                    box-shadow: 0 2px 12px rgba(10, 22, 40, 0.04);
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 12px;
                }
                
                thead {
                    background: linear-gradient(135deg, #0A1628, #1B3A5C);
                    color: #FFFFFF;
                }
                
                th {
                    padding: 12px 16px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 10px;
                    letter-spacing: 0.6px;
                    text-transform: uppercase;
                }
                
                td {
                    padding: 10px 16px;
                    border-bottom: 1px solid var(--border);
                    color: var(--medium-text);
                }
                
                tr:last-child td { border-bottom: none; }
                tbody tr { transition: all 0.2s ease; }
                tbody tr:hover { background: #F8FAFC; }
                tbody tr:nth-child(even) { background: #FAFCFE; }
                
                /* ============================================================
                   BADGES
                   ============================================================ */
                .badge {
                    display: inline-block;
                    padding: 2px 12px;
                    border-radius: 20px;
                    font-size: 9px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    text-transform: uppercase;
                }
                
                .badge-critical { background: #FEE2E2; color: #DC2626; }
                .badge-high { background: #FEF3C7; color: #D97706; }
                .badge-medium { background: #FEF3C7; color: #D97706; }
                .badge-low { background: #EFF6FF; color: #3B82F6; }
                .badge-info { background: #EFF6FF; color: #3B82F6; }
                
                /* ============================================================
                   RISK CARDS
                   ============================================================ */
                .risk-card {
                    border-left: 4px solid var(--medium-text);
                    padding: 12px 16px;
                    margin: 8px 0;
                    background: rgba(255, 255, 255, 0.7);
                    border-radius: 0 10px 10px 0;
                    transition: all 0.3s ease;
                    border: 1px solid transparent;
                    border-left-width: 4px;
                }
                
                .risk-card:hover {
                    transform: translateX(4px);
                    box-shadow: 0 4px 20px rgba(10, 22, 40, 0.06);
                }
                
                .risk-critical { border-left-color: #DC2626; background: rgba(254, 226, 226, 0.4); }
                .risk-high { border-left-color: #D97706; background: rgba(254, 243, 199, 0.4); }
                .risk-medium { border-left-color: #D97706; background: rgba(254, 243, 199, 0.25); }
                .risk-low { border-left-color: #3B82F6; background: rgba(239, 246, 255, 0.4); }
                
                .risk-title {
                    font-weight: 600;
                    font-size: 12.5px;
                    color: var(--dark-text);
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    flex-wrap: wrap;
                }
                
                .risk-description {
                    font-size: 11px;
                    color: var(--medium-text);
                    margin-top: 3px;
                }
                
                .risk-recommendation {
                    font-size: 10px;
                    color: #2C5F8A;
                    margin-top: 5px;
                    padding: 3px 12px;
                    background: rgba(44, 95, 138, 0.08);
                    border-radius: 6px;
                    display: inline-block;
                    border: 1px solid rgba(44, 95, 138, 0.1);
                }
                
                /* ============================================================
                   RECOMMENDATIONS
                   ============================================================ */
                .recommendation-list { list-style: none; padding: 0; }
                
                .recommendation-item {
                    padding: 10px 16px;
                    background: rgba(255, 255, 255, 0.7);
                    border-radius: 10px;
                    margin: 6px 0;
                    border-left: 4px solid #C9A84C;
                    display: flex;
                    align-items: flex-start;
                    gap: 10px;
                    transition: all 0.3s ease;
                    border: 1px solid rgba(201, 168, 76, 0.1);
                    border-left-width: 4px;
                }
                
                .recommendation-item:hover {
                    transform: translateX(4px);
                    box-shadow: 0 4px 20px rgba(10, 22, 40, 0.06);
                    border-color: rgba(201, 168, 76, 0.2);
                }
                
                .recommendation-item .rec-number {
                    font-weight: 700;
                    color: #C9A84C;
                    min-width: 26px;
                    font-size: 13px;
                    text-align: center;
                    background: rgba(201, 168, 76, 0.1);
                    border-radius: 50%;
                    line-height: 22px;
                    height: 26px;
                    width: 26px;
                    flex-shrink: 0;
                }
                
                .recommendation-item .rec-text {
                    color: var(--medium-text);
                    font-size: 12px;
                    padding-top: 1px;
                }
                
                /* ============================================================
                   INSIGHT BOX
                   ============================================================ */
                .insight-box {
                    background: rgba(255, 255, 255, 0.7);
                    border-radius: 12px;
                    padding: 14px 20px;
                    margin: 10px 0;
                    border-left: 4px solid #C9A84C;
                    border: 1px solid rgba(201, 168, 76, 0.12);
                    border-left-width: 4px;
                    transition: all 0.3s ease;
                }
                
                .insight-box:hover {
                    box-shadow: 0 4px 20px rgba(10, 22, 40, 0.06);
                }
                
                .insight-box .insight-text {
                    color: var(--dark-text);
                    font-size: 12.5px;
                }
                
                .insight-box .insight-text strong {
                    color: var(--dark-text);
                }
                
                /* ============================================================
                   HEALTH METER
                   ============================================================ */
                .health-meter {
                    display: flex;
                    align-items: center;
                    gap: 18px;
                    padding: 14px 20px;
                    background: rgba(255, 255, 255, 0.7);
                    backdrop-filter: blur(10px);
                    border-radius: 12px;
                    margin: 8px 0;
                    border: 1px solid rgba(201, 168, 76, 0.1);
                    transition: all 0.3s ease;
                }
                
                .health-meter:hover {
                    box-shadow: 0 4px 20px rgba(10, 22, 40, 0.06);
                }
                
                .health-meter .health-icon { font-size: 26px; flex-shrink: 0; }
                .health-meter .health-info { flex: 1; }
                .health-meter .health-status { font-weight: 700; font-size: 17px; }
                .health-meter .health-detail { font-size: 11px; color: var(--medium-text); }
                
                /* ============================================================
                   VISUALIZATION BARS
                   ============================================================ */
                .viz-bar-container {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin: 3px 0;
                }
                
                .viz-bar-track {
                    flex: 1;
                    height: 5px;
                    background: var(--border);
                    border-radius: 4px;
                    overflow: hidden;
                }
                
                .viz-bar-fill {
                    height: 100%;
                    border-radius: 4px;
                    transition: width 1s ease;
                }
                
                .viz-bar-fill.gold { background: linear-gradient(90deg, #C9A84C, #F0D080); }
                .viz-bar-fill.blue { background: linear-gradient(90deg, #2C5F8A, #4A7FA5); }
                .viz-bar-fill.green { background: linear-gradient(90deg, #0D9488, #4ADE80); }
                .viz-bar-fill.red { background: linear-gradient(90deg, #DC2626, #F87171); }
                .viz-bar-fill.orange { background: linear-gradient(90deg, #D97706, #F59E0B); }
                
                .viz-bar-label {
                    font-size: 11px;
                    font-weight: 500;
                    min-width: 56px;
                }
                
                .viz-bar-value {
                    font-size: 11px;
                    font-weight: 600;
                    min-width: 36px;
                    text-align: right;
                }
                
                /* ============================================================
                   FOOTER
                   ============================================================ */
                .report-footer {
                    border-top: 2px solid rgba(201, 168, 76, 0.15);
                    padding: 24px 48px 26px 48px;
                    text-align: center;
                    background: rgba(248, 250, 252, 0.8);
                }
                
                .report-footer .footer-brand {
                    font-size: 15px;
                    font-weight: 700;
                    color: var(--dark-text);
                }
                
                .report-footer .footer-brand .gold { color: #C9A84C; }
                
                .report-footer .footer-credit {
                    font-size: 11px;
                    color: var(--medium-text);
                    margin-top: 3px;
                }
                
                .report-footer .footer-credit a {
                    color: #2C5F8A;
                    text-decoration: none;
                    font-weight: 500;
                }
                
                .report-footer .footer-credit a:hover { color: #C9A84C; }
                
                .report-footer .footer-disclaimer {
                    font-size: 9px;
                    color: var(--light-text);
                    margin-top: 4px;
                    letter-spacing: 0.3px;
                }
                
                /* ============================================================
                   RESPONSIVE DESIGN - 4 BREAKPOINTS
                   ============================================================ */
                
                /* Desktop Large */
                @media (max-width: 1024px) {
                    .report-body { padding: 28px 32px 32px 32px; }
                    .hero-header { padding: 36px 32px 24px 32px; }
                    .report-footer { padding: 20px 32px 22px 32px; }
                }
                
                /* Tablet */
                @media (max-width: 820px) {
                    body { padding: 20px 12px; }
                    .hero-header { padding: 28px 24px 20px 24px; }
                    .report-body { padding: 22px 24px 26px 24px; }
                    .report-footer { padding: 18px 24px 20px 24px; }
                    .metric-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
                    .brand-name { font-size: 28px; }
                    .report-title { font-size: 22px; }
                    .section-heading { font-size: 18px; }
                    .report-meta { flex-direction: column; gap: 5px; align-items: center; }
                    .report-title::after { width: 40px; }
                    .health-meter { flex-direction: column; text-align: center; gap: 6px; }
                    .recommendation-item { padding: 8px 12px; }
                    .metric-card { min-height: 110px; padding: 14px 10px 12px 10px; }
                    .metric-card .metric-value { font-size: 28px; }
                    .metric-card .metric-icon { font-size: 20px; }
                }
                
                /* Mobile Large */
                @media (max-width: 600px) {
                    body { padding: 12px 6px; }
                    .hero-header { padding: 20px 16px 16px 16px; }
                    .report-body { padding: 16px 16px 20px 16px; }
                    .report-footer { padding: 14px 16px 16px 16px; }
                    .metric-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
                    .brand-name { font-size: 22px; letter-spacing: 2px; }
                    .brand-tagline { font-size: 11px; letter-spacing: 1px; }
                    .report-title { font-size: 18px; }
                    .report-subtitle { font-size: 11px; }
                    .section-heading { font-size: 15px; flex-wrap: wrap; }
                    .section-heading .section-badge { font-size: 8px; padding: 2px 8px; }
                    .metric-card { min-height: 90px; padding: 10px 8px 8px 8px; border-radius: 10px; }
                    .metric-card .metric-value { font-size: 22px; }
                    .metric-card .metric-label { font-size: 9px; }
                    .metric-card .metric-icon { font-size: 18px; }
                    .metric-card .metric-trend { font-size: 7px; padding: 1px 6px; }
                    .health-meter { padding: 10px 14px; flex-direction: row; text-align: left; gap: 10px; }
                    .health-meter .health-icon { font-size: 20px; }
                    .health-meter .health-status { font-size: 14px; }
                    .health-meter .health-detail { font-size: 9px; }
                    .recommendation-item { padding: 6px 10px; gap: 8px; border-left-width: 3px; }
                    .recommendation-item .rec-number { min-width: 20px; height: 20px; width: 20px; font-size: 10px; line-height: 16px; }
                    .recommendation-item .rec-text { font-size: 10px; }
                    .risk-card { padding: 8px 10px; }
                    .risk-title { font-size: 10.5px; }
                    .risk-description { font-size: 9.5px; }
                    .insight-box { padding: 8px 12px; }
                    .insight-box .insight-text { font-size: 10px; }
                    .table-wrapper { border-radius: 8px; }
                    th, td { padding: 5px 8px; font-size: 9.5px; }
                    .report-meta { font-size: 9px; gap: 6px; }
                    .report-meta span { padding: 2px 8px; }
                    .viz-bar-label { font-size: 9px; min-width: 40px; }
                    .viz-bar-value { font-size: 9px; min-width: 28px; }
                    .report-footer .footer-brand { font-size: 12px; }
                    .report-footer .footer-credit { font-size: 9px; }
                    .report-footer .footer-disclaimer { font-size: 7px; }
                    .badge { font-size: 7px; padding: 1px 8px; }
                }
                
                /* Mobile Small */
                @media (max-width: 400px) {
                    body { padding: 8px 4px; }
                    .hero-header { padding: 16px 10px 12px 10px; }
                    .report-body { padding: 12px 10px 16px 10px; }
                    .report-footer { padding: 10px 10px 12px 10px; }
                    .metric-grid { grid-template-columns: 1fr; gap: 6px; }
                    .brand-name { font-size: 18px; letter-spacing: 1px; }
                    .brand-tagline { font-size: 10px; }
                    .report-title { font-size: 16px; }
                    .report-title::after { width: 30px; height: 2px; }
                    .section-heading { font-size: 13px; }
                    .section-heading::after { width: 30px; }
                    .report-container { border-radius: 12px; }
                    .metric-card { min-height: 80px; padding: 8px 6px 6px 6px; }
                    .metric-card .metric-value { font-size: 20px; }
                    .metric-card .metric-label { font-size: 8px; }
                    .health-meter { flex-direction: column; text-align: center; gap: 4px; padding: 8px 10px; }
                    .health-meter .health-icon { font-size: 18px; }
                    .health-meter .health-status { font-size: 13px; }
                    th, td { padding: 4px 6px; font-size: 8.5px; }
                    .recommendation-item .rec-text { font-size: 9px; }
                    .risk-title { font-size: 9.5px; }
                    .risk-description { font-size: 8.5px; }
                    .insight-box .insight-text { font-size: 9px; }
                    .report-meta { font-size: 8px; gap: 4px; }
                    .report-meta span { padding: 2px 6px; }
                }
                
                /* ============================================================
                   PRINT STYLES
                   ============================================================ */
                @media print {
                    body { background: white; padding: 0; }
                    .report-container { border-radius: 0; box-shadow: none; backdrop-filter: none; }
                    .hero-header { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                    .metric-card:hover { transform: none; }
                    .risk-card:hover { transform: none; }
                    .recommendation-item:hover { transform: none; }
                    .section { break-inside: avoid; }
                    .table-wrapper { break-inside: avoid; }
                }
                
                /* ============================================================
                   ANIMATIONS
                   ============================================================ */
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(16px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                .animate-in {
                    animation: fadeInUp 0.5s ease forwards;
                }
                
                .metric-card:nth-child(1) { animation-delay: 0.05s; }
                .metric-card:nth-child(2) { animation-delay: 0.1s; }
                .metric-card:nth-child(3) { animation-delay: 0.15s; }
                .metric-card:nth-child(4) { animation-delay: 0.2s; }
                
                /* Custom scrollbar */
                ::-webkit-scrollbar { width: 5px; height: 5px; }
                ::-webkit-scrollbar-track { background: #F0F4F8; border-radius: 4px; }
                ::-webkit-scrollbar-thumb { background: #C9A84C; border-radius: 4px; }
                ::-webkit-scrollbar-thumb:hover { background: #A8893A; }
            </style>
        </head>
        <body>
            <div class="report-container">
                <!-- HERO HEADER -->
                <div class="hero-header">
                    <h1 class="brand-name">KONTRACTIQ<span class="gold-dot">.</span></h1>
                    <p class="brand-tagline">Intelligence for every clause.</p>
                    <div class="report-meta">
                        <span>{{ generated_date }}</span>
                        <span>{{ report_id }}</span>
                        <span>{{ total_contracts }} Contracts</span>
                    </div>
                </div>
                
                <!-- REPORT BODY -->
                <div class="report-body">
                    <div class="report-title-section">
                        <h2 class="report-title">{{ report_title }}</h2>
                        <p class="report-subtitle">Comprehensive contract intelligence analysis</p>
                    </div>
                    
                    <!-- METRIC GRID -->
                    <div class="metric-grid">
                        <div class="metric-card blue animate-in">
                            <span class="metric-icon">📄</span>
                            <div class="metric-value">{{ total_contracts }}</div>
                            <div class="metric-label">Total Contracts</div>
                            <span class="metric-trend neutral">Active</span>
                        </div>
                        <div class="metric-card green animate-in">
                            <span class="metric-icon">📋</span>
                            <div class="metric-value">{{ total_clauses }}</div>
                            <div class="metric-label">Clauses Extracted</div>
                            <span class="metric-trend up">↑ {{ clause_coverage }}% coverage</span>
                        </div>
                        <div class="metric-card orange animate-in">
                            <span class="metric-icon">⚠️</span>
                            <div class="metric-value">{{ total_risks }}</div>
                            <div class="metric-label">Total Risks</div>
                            <span class="metric-trend neutral">Under review</span>
                        </div>
                        <div class="metric-card red animate-in">
                            <span class="metric-icon">🚨</span>
                            <div class="metric-value">{{ critical_risks }}</div>
                            <div class="metric-label">Critical Risks</div>
                            <span class="metric-trend down">{{ 'Action needed' if critical_risks > 0 else 'All clear' }}</span>
                        </div>
                    </div>
                    
                    <!-- PORTFOLIO HEALTH -->
                    <div class="section">
                        <h3 class="section-heading">
                            Portfolio Health Assessment
                            <span class="section-badge gold">{{ health_status }}</span>
                        </h3>
                        
                        <div class="health-meter">
                            <div class="health-icon">{{ health_icon }}</div>
                            <div class="health-info">
                                <div class="health-status" style="color: {{ health_color }};">{{ health_status }}</div>
                                <div class="health-detail">
                                    {{ avg_risks_per_contract }} risks per contract • 
                                    {{ avg_clauses_per_contract }} clauses per contract • 
                                    {{ clause_coverage }}% clause coverage
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- RISK FINDINGS -->
                    {% if risks %}
                    <div class="section">
                        <h3 class="section-heading">
                            Risk Findings
                            <span class="section-badge">{{ risks|length }} Total</span>
                        </h3>
                        
                        <div class="insight-box">
                            <div class="insight-text">
                                <strong>Critical:</strong> {{ risk_critical }} &nbsp;|&nbsp;
                                <strong>High:</strong> {{ risk_high }} &nbsp;|&nbsp;
                                <strong>Medium:</strong> {{ risk_medium }} &nbsp;|&nbsp;
                                <strong>Low:</strong> {{ risk_low }}
                            </div>
                        </div>
                        
                        <!-- Risk Distribution -->
                        <div style="margin: 10px 0 14px 0; padding: 14px 18px; background: rgba(255,255,255,0.5); border-radius: 10px; border: 1px solid var(--border);">
                            <div style="font-size: 11px; font-weight: 600; color: var(--medium-text); margin-bottom: 8px;">Risk Distribution</div>
                            <div class="viz-bar-container">
                                <span class="viz-bar-label">🔴 Critical</span>
                                <div class="viz-bar-track">
                                    <div class="viz-bar-fill red" style="width: {{ (risk_critical / max_risk_count * 100) if max_risk_count > 0 else 0 }}%;"></div>
                                </div>
                                <span class="viz-bar-value">{{ risk_critical }}</span>
                            </div>
                            <div class="viz-bar-container">
                                <span class="viz-bar-label">🟠 High</span>
                                <div class="viz-bar-track">
                                    <div class="viz-bar-fill orange" style="width: {{ (risk_high / max_risk_count * 100) if max_risk_count > 0 else 0 }}%;"></div>
                                </div>
                                <span class="viz-bar-value">{{ risk_high }}</span>
                            </div>
                            <div class="viz-bar-container">
                                <span class="viz-bar-label">🟡 Medium</span>
                                <div class="viz-bar-track">
                                    <div class="viz-bar-fill gold" style="width: {{ (risk_medium / max_risk_count * 100) if max_risk_count > 0 else 0 }}%;"></div>
                                </div>
                                <span class="viz-bar-value">{{ risk_medium }}</span>
                            </div>
                            <div class="viz-bar-container">
                                <span class="viz-bar-label">🟢 Low</span>
                                <div class="viz-bar-track">
                                    <div class="viz-bar-fill green" style="width: {{ (risk_low / max_risk_count * 100) if max_risk_count > 0 else 0 }}%;"></div>
                                </div>
                                <span class="viz-bar-value">{{ risk_low }}</span>
                            </div>
                        </div>
                        
                        {% for risk in risks[:25] %}
                        <div class="risk-card risk-{{ risk.severity }}">
                            <div class="risk-title">
                                <span class="badge badge-{{ risk.severity }}">{{ risk.severity|title }}</span>
                                {{ risk.type }}
                            </div>
                            <div class="risk-description">{{ risk.description }}</div>
                            {% if risk.recommendation %}
                            <div class="risk-recommendation">{{ risk.recommendation }}</div>
                            {% endif %}
                        </div>
                        {% endfor %}
                        
                        {% if risks|length > 25 %}
                        <p style="color: var(--light-text); font-size: 11px; margin-top: 8px; text-align: center;">
                            ... and {{ risks|length - 25 }} more risks
                        </p>
                        {% endif %}
                    </div>
                    {% endif %}
                    
                    <!-- CLAUSE EXTRACTION -->
                    {% if clauses %}
                    <div class="section">
                        <h3 class="section-heading">
                            Clause Extraction Summary
                            <span class="section-badge">{{ clauses|length }} Total</span>
                        </h3>
                        
                        <div class="insight-box">
                            <div class="insight-text">
                                <strong>Most Common:</strong> {{ most_common_clause }} &nbsp;|&nbsp;
                                <strong>Unique Types:</strong> {{ unique_clause_types }} &nbsp;|&nbsp;
                                <strong>Coverage:</strong> {{ clause_coverage }}%
                            </div>
                        </div>
                        
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Contract</th>
                                        <th>Clause Type</th>
                                        <th>Clause Text</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for clause in clauses[:25] %}
                                    <tr>
                                        <td><strong>{{ clause.contract_name }}</strong></td>
                                        <td><span class="badge badge-info">{{ clause.type }}</span></td>
                                        <td>{{ clause.text[:120] }}{% if clause.text|length > 120 %}...{% endif %}</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        {% if clauses|length > 25 %}
                        <p style="color: var(--light-text); font-size: 11px; margin-top: 6px; text-align: center;">
                            ... and {{ clauses|length - 25 }} more clauses
                        </p>
                        {% endif %}
                    </div>
                    {% endif %}
                    
                    <!-- RECOMMENDATIONS -->
                    {% if recommendations %}
                    <div class="section">
                        <h3 class="section-heading">
                            Strategic Recommendations
                            <span class="section-badge gold">{{ recommendations|length }} Actions</span>
                        </h3>
                        
                        <ul class="recommendation-list">
                            {% for rec in recommendations %}
                            <li class="recommendation-item">
                                <span class="rec-number">{{ loop.index }}</span>
                                <span class="rec-text">{{ rec }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </div>
                
                <!-- FOOTER -->
                <div class="report-footer">
                    <div class="footer-brand">KontractIQ <span class="gold">✦</span></div>
                    <div class="footer-credit">
                        Built with precision by <strong>Hassan Subhani</strong> • 
                        <a href="mailto:hassansubhani822@gmail.com">hassansubhani822@gmail.com</a>
                    </div>
                    <div class="footer-disclaimer">
                        &copy; 2026 KontractIQ — Intelligence for every clause.
                        <br>Confidential · For authorized use only
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        context = {
            'generated_date': generated_date,
            'report_id': report_id,
            'report_title': report_title,
            'total_contracts': total_contracts,
            'total_clauses': total_clauses,
            'total_risks': total_risks,
            'critical_risks': critical_risks,
            'health_status': health_status,
            'health_color': health_color,
            'health_icon': health_icon,
            'avg_risks_per_contract': f"{avg_risks_per_contract:.2f}",
            'avg_clauses_per_contract': f"{avg_clauses_per_contract:.1f}",
            'clause_coverage': f"{clause_coverage:.0f}",
            'most_common_clause': most_common_clause,
            'unique_clause_types': unique_clause_types,
            'risk_critical': risk_summary.get('critical', 0),
            'risk_high': risk_summary.get('high', 0),
            'risk_medium': risk_summary.get('medium', 0),
            'risk_low': risk_summary.get('low', 0),
            'max_risk_count': max_risk_count,
            'risks': data.get('risks', []),
            'clauses': data.get('clauses', []),
            'recommendations': data.get('recommendations', [])
        }
        
        template = jinja2.Template(template_str)
        return template.render(**context)


# ================================================================
# BACKWARD COMPATIBILITY
# ================================================================

class PremiumReportGenerator(UltraPremiumReportGenerator):
    """Legacy alias for UltraPremiumReportGenerator"""
    pass


# ================================================================
# USAGE EXAMPLE
# ================================================================

if __name__ == "__main__":
    sample_data = {
        'total_contracts': 2,
        'total_clauses': 10,
        'total_risks': 1,
        'critical_risks': 0,
        'risk_summary': {
            'critical': 0,
            'high': 0,
            'medium': 1,
            'low': 0,
        },
        'risks': [
            {
                'severity': 'medium',
                'type': 'broad_indemnification',
                'description': 'Broad indemnification - potential liability',
                'recommendation': '🟡 MEDIUM: Limit indemnification scope to negligence and cap the amount.'
            }
        ],
        'clauses': [
            {'type': 'Governing Law', 'text': 'Governing Law\nThis Agreement shall be governed by the laws of New York', 'contract_name': 'Contract_Beta_MSA.pdf'},
            {'type': 'Governing Law', 'text': 'laws of New York', 'contract_name': 'Contract_Beta_MSA.pdf'},
            {'type': 'Payment Terms', 'text': 'Payment Terms\nClient shall pay all undisputed invoices within 60 days', 'contract_name': 'Contract_Beta_MSA.pdf'},
            {'type': 'Indemnification', 'text': 'Indemnification\nProvider shall indemnify and hold harmless Client against', 'contract_name': 'Contract_Beta_MSA.pdf'},
            {'type': 'Indemnification', 'text': 'hold harmless Client against', 'contract_name': 'Contract_Beta_MSA.pdf'},
            {'type': 'Governing Law', 'text': 'Governing Law\nThis Agreement shall be governed by the laws of California', 'contract_name': 'Contract_Acme_MSA.pdf'},
            {'type': 'Governing Law', 'text': 'laws of California', 'contract_name': 'Contract_Acme_MSA.pdf'},
            {'type': 'Payment Terms', 'text': 'Payment Terms\nClient shall pay all undisputed invoices within 30 days', 'contract_name': 'Contract_Acme_MSA.pdf'},
            {'type': 'Liability Cap', 'text': 'Liability Cap\nThe total liability of either party shall not exceed USD 1,000,000,', 'contract_name': 'Contract_Acme_MSA.pdf'},
            {'type': 'Indemnification', 'text': 'Indemnification\nProvider shall indemnify Client against', 'contract_name': 'Contract_Acme_MSA.pdf'},
        ],
        'recommendations': [
            '📋 Schedule review for 1 medium-risk clause(s) within 1 week',
            '📊 Standardize Payment Terms - 1 contract(s) deviate from the norm',
            '📊 Standardize Termination Notice - 1 contract(s) deviate from the norm',
            '📊 Standardize Governing Law - 1 contract(s) deviate from the norm',
            '📊 Standardize Confidentiality Period - 1 contract(s) deviate from the norm',
            '🌟 Portfolio is healthy - maintain current contract management practices'
        ]
    }
    
    print("=" * 60)
    print("KONTRACTIQ - ULTRA PREMIUM REPORT GENERATOR v6.0")
    print("=" * 60)
    
    
    generator = UltraPremiumReportGenerator()
    
    # Generate HTML
    print("\n🌐 Generating HTML report...")
    html_content = generator.generate_html_report(sample_data, 'full_analysis')
    with open('KontractIQ_Ultra_Report_v6.0.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ HTML report saved as 'KontractIQ_Ultra_Report_v6.0.html'")
    
    print("\n" + "=" * 60)
    print("✨ FEATURES v6.0:")
    print("=" * 60)
   
    print("=" * 60)