"""
KontractIQ - Premium Reports Page
comprehensive report 
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from ..core.report_generator import UltraPremiumReportGenerator
from ..utils.constants import COLORS
from ..core.crosscheck import CrossCheckEngine


def render_reports():
    """Render the reports page - HTML-Report """
    
    # ========================================================================
    # HERO SECTION
    # ========================================================================
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
                padding: 32px 40px;
                border-radius: 20px;
                color: white;
                margin-bottom: 28px;
                box-shadow: 0 8px 32px rgba(10, 38, 71, 0.15);">
        <div style="display: flex; align-items: center; gap: 16px;">
            <span style="font-size: 40px;">📊</span>
            <div>
                <h1 style="font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">Premium Report</h1>
                <p style="font-size: 15px; opacity: 0.9; margin: 4px 0 0 0;">
                    Generate a comprehensive HTML report with premium branding and deep analysis
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHECK CONTRACTS
    # ========================================================================
    if not st.session_state.contracts:
        st.info("📭 No contracts uploaded yet. Upload contracts first to generate reports!")
        return
    
    # ========================================================================
    # STATS CARDS - Premium Dashboard Style
    # ========================================================================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: {COLORS['neutrals']['white']};
                    border-radius: 16px;
                    padding: 18px 20px;
                    box-shadow: 0 4px 12px rgba(10, 38, 71, 0.06);
                    border-left: 4px solid {COLORS['primary']['corporate_blue']};
                    text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{len(st.session_state.contracts)}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">📄 Total Contracts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {COLORS['neutrals']['white']};
                    border-radius: 16px;
                    padding: 18px 20px;
                    box-shadow: 0 4px 12px rgba(10, 38, 71, 0.06);
                    border-left: 4px solid {COLORS['semantic']['success']};
                    text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{len(st.session_state.clauses)}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">📋 Clauses Extracted</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk_count = len(st.session_state.risks)
        risk_color = COLORS['semantic']['danger'] if risk_count > 0 else COLORS['semantic']['success']
        st.markdown(f"""
        <div style="background: {COLORS['neutrals']['white']};
                    border-radius: 16px;
                    padding: 18px 20px;
                    box-shadow: 0 4px 12px rgba(10, 38, 71, 0.06);
                    border-left: 4px solid {risk_color};
                    text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{risk_count}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">⚠️ Total Risks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        critical_risks = sum(1 for r in st.session_state.risks if r.severity == 'critical')
        critical_color = COLORS['semantic']['danger'] if critical_risks > 0 else COLORS['semantic']['success']
        st.markdown(f"""
        <div style="background: {COLORS['neutrals']['white']};
                    border-radius: 16px;
                    padding: 18px 20px;
                    box-shadow: 0 4px 12px rgba(10, 38, 71, 0.06);
                    border-left: 4px solid {critical_color};
                    text-align: center;">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{critical_risks}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">🔴 Critical Risks</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========================================================================
    # REPORT CONFIGURATION
    # ========================================================================
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h2 style="font-size: 20px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">📋 Report Configuration</h2>
        <p style="color: {COLORS['neutrals']['dark_gray']}; margin: 4px 0 0 0;">
            Generate a comprehensive full analysis report
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # REPORT PREVIEW - What's included
    # ========================================================================
    with st.expander("👁️ What's Included in This Report", expanded=False):
        show_report_preview()
    
    st.divider()
    
    # ========================================================================
    # GENERATE REPORT BUTTON
    # ========================================================================
    if st.button(
        "🚀 Generate Premium HTML Report",
        key="generate_report_btn",
        use_container_width=True,
        type="primary"
    ):
        with st.spinner("📊 Generating premium HTML report with deep analysis..."):
            # Collect data
            report_data = collect_report_data()
            
            # Initialize premium report generator (HTML only)
            report_gen = UltraPremiumReportGenerator()
            
            # Generate HTML - always full_analysis
            html_content = report_gen.generate_html_report(report_data, 'full_analysis')
            
            st.balloons()
            st.success("✅ Premium HTML Report generated successfully!")
            
            # Download button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download HTML Report",
                    data=html_content,
                    file_name=f"kontractiq_full_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                    mime="text/html",
                    key="download_html_btn",
                    use_container_width=True
                )
            
            # Preview HTML using components.html for proper rendering
            with st.expander("👁️ Preview HTML Report", expanded=True):
                st.caption(f"📄 Report contains: {report_data.get('total_contracts', 0)} contracts, {report_data.get('total_clauses', 0)} clauses, {report_data.get('total_risks', 0)} risks")
                st.components.v1.html(
                    html_content,
                    height=700,
                    scrolling=True
                )


def collect_report_data() -> dict:
    """Collect comprehensive data for the report"""
    data = {
        'total_contracts': len(st.session_state.contracts),
        'total_clauses': len(st.session_state.clauses),
        'total_risks': len(st.session_state.risks),
        'clauses': [c.to_dict() for c in st.session_state.clauses],
        'risks': [r.to_dict() for r in st.session_state.risks],
        'contracts': [c.to_dict() for c in st.session_state.contracts],
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'report_type': 'full_analysis'
    }
    
    # Risk summary
    risk_summary = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for risk in st.session_state.risks:
        if risk.severity in risk_summary:
            risk_summary[risk.severity] += 1
    
    data['risk_summary'] = risk_summary
    data['critical_risks'] = risk_summary.get('critical', 0)
    
    # Generate strategic recommendations
    recommendations = []
    
    # Risk-based recommendations
    if risk_summary.get('critical', 0) > 0:
        recommendations.append(f"🚨 Address {risk_summary['critical']} critical risk(s) immediately - they pose significant exposure")
    if risk_summary.get('high', 0) > 0:
        recommendations.append(f"⚠️ Review {risk_summary['high']} high-risk clause(s) within the next 3 days")
    if risk_summary.get('medium', 0) > 0:
        recommendations.append(f"📋 Schedule review for {risk_summary['medium']} medium-risk clause(s) within 1 week")
    
    # Cross-check findings
    engine = CrossCheckEngine()
    crosscheck_result = engine.analyze(st.session_state.contracts)
    
    if crosscheck_result and 'findings' in crosscheck_result:
        for finding in crosscheck_result['findings']:
            if finding.get('deviations') and len(finding.get('deviations', [])) > 0:
                recommendations.append(
                    f"📊 Standardize {finding['type']} - {len(finding['deviations'])} contract(s) deviate from the norm"
                )
    
    # Portfolio-level recommendations
    total_contracts = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    
    if total_contracts > 0 and total_clauses == 0:
        recommendations.append("📝 No clauses extracted - consider uploading more detailed contracts")
    
    if total_contracts > 10:
        recommendations.append("🔄 Implement regular contract review cycles for ongoing consistency")
    
    if risk_summary.get('critical', 0) == 0 and risk_summary.get('high', 0) == 0:
        recommendations.append("🌟 Portfolio is healthy - maintain current contract management practices")
    
    # Add general recommendations if needed
    if len(recommendations) < 3:
        recommendations.append("📈 Schedule periodic contract audits to maintain compliance")
        recommendations.append("📊 Consider using contract templates for standardization")
    
    data['recommendations'] = recommendations[:6]  # Limit to top 6
    
    # Metrics for display
    data['metrics'] = [
        {'label': '📄 Total Contracts', 'value': data['total_contracts']},
        {'label': '📋 Total Clauses', 'value': data['total_clauses']},
        {'label': '⚠️ Total Risks', 'value': data['total_risks']},
        {'label': '🔴 Critical Risks', 'value': data['critical_risks']}
    ]
    
    return data


def show_report_preview():
    """Show what's included in the report"""
    
    st.markdown(f"""
    <div style="background: {COLORS['neutrals']['off_white']};
                border-radius: 12px;
                padding: 16px 20px;
                border-left: 4px solid {COLORS['primary']['corporate_blue']};">
        <h4 style="margin: 0 0 8px 0; color: {COLORS['primary']['deepest_navy']};">📊 Full Analysis Report</h4>
        <ul style="margin: 0; padding-left: 20px; color: {COLORS['neutrals']['dark_gray']};">
            <li>✅ Executive Summary with key metrics</li>
            <li>✅ All {len(st.session_state.contracts)} contracts</li>
            <li>✅ All {len(st.session_state.clauses)} extracted clauses</li>
            <li>✅ All {len(st.session_state.risks)} risk findings</li>
            <li>✅ Cross-contract inconsistency analysis</li>
            <li>✅ Portfolio health assessment</li>
            <li>✅ Strategic recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)