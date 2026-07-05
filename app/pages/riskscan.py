"""
KontractIQ - RiskScan Page
contract risk detection with active learning 
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import defaultdict
from ..core.risk_scanner import RiskScanner
from ..utils.constants import COLORS, RISK_SEVERITIES, DEFAULT_RISK_RULES
from ..models.risk import Risk
from ..models.contract import Contract


# ============================================================================
# COLOR CONSTANTS (Matching Dashboard Perfectly)
# ============================================================================

DASHBOARD_COLORS = {
    'primary': {
        'deepest_navy': '#0A2647',
        'rich_navy': '#144272',
        'corporate_blue': '#205295',
        'ice_blue': '#E8F1F8',
        'light_blue': '#F0F7FC',
        'hover_blue': '#1A3A5C',
    },
    'neutrals': {
        'white': '#FFFFFF',
        'off_white': '#F8FAFE',
        'light_gray': '#E2E8F0',
        'medium_gray': '#94A3B8',
        'dark_gray': '#475569',
        'slate': '#1E293B',
        'border': '#E8EDF2',
    },
    'semantic': {
        'success': '#22C55E',
        'success_bg': '#F0FDF4',
        'warning': '#F59E0B',
        'warning_bg': '#FFFBEB',
        'danger': '#EF4444',
        'danger_bg': '#FEF2F2',
        'info': '#3B82F6',
        'info_bg': '#EFF6FF',
    },
    'gradients': {
        'hero': 'linear-gradient(135deg, #0A2647 0%, #144272 100%)',
        'card': 'linear-gradient(135deg, #F8FAFE 0%, #FFFFFF 100%)',
        'success': 'linear-gradient(135deg, #22C55E 0%, #16A34A 100%)',
        'warning': 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
        'danger': 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)',
        'info': 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
    }
}

# Card spacing constants
CARD_SPACING = {
    'padding': '20px',
    'margin': '12px',
    'border_radius': '16px',
    'shadow': '0 1px 3px rgba(10, 38, 71, 0.08)',
    'hover_shadow': '0 4px 12px rgba(10, 38, 71, 0.12)',
}


# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================

def render_riskscan():
    """Render the enhanced RiskScan page with premium UI matching dashboard"""
    
    # ========================================================================
    # HERO SECTION - Perfect Match with Dashboard
    # ========================================================================
    
    total_contracts = len(st.session_state.contracts)
    total_risks = len(st.session_state.risks)
    
    st.markdown(f"""
    <div style="
        background: {DASHBOARD_COLORS['gradients']['hero']};
        padding: 32px 40px;
        border-radius: 20px;
        margin-bottom: 28px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(10, 38, 71, 0.15);
    ">
        <div style="position: absolute; right: 20px; bottom: -10px; font-size: 120px; opacity: 0.06;">🛡️</div>
        <div style="position: absolute; right: 80px; top: -30px; font-size: 60px; opacity: 0.04;">⚖️</div>
        <h1 style="font-size: 32px; font-weight: 700; margin: 0; color: white; letter-spacing: -0.5px;">
            Risk Intelligence Center
        </h1>
        <p style="font-size: 16px; opacity: 0.85; margin: 8px 0 0 0; color: rgba(255,255,255,0.85);">
            AI-powered risk detection with active learning & compliance automation
        </p>
        <div style="display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap;">
            <span style="
                background: rgba(255,255,255,0.12);
                backdrop-filter: blur(10px);
                padding: 5px 16px;
                border-radius: 20px;
                font-size: 12px;
                color: rgba(255,255,255,0.9);
                border: 1px solid rgba(255,255,255,0.08);
            ">🎯 7+ Risk Patterns</span>
            <span style="
                background: rgba(255,255,255,0.12);
                backdrop-filter: blur(10px);
                padding: 5px 16px;
                border-radius: 20px;
                font-size: 12px;
                color: rgba(255,255,255,0.9);
                border: 1px solid rgba(255,255,255,0.08);
            ">⚡ Active Learning</span>
            <span style="
                background: rgba(255,255,255,0.12);
                backdrop-filter: blur(10px);
                padding: 5px 16px;
                border-radius: 20px;
                font-size: 12px;
                color: rgba(255,255,255,0.9);
                border: 1px solid rgba(255,255,255,0.08);
            ">📊 Real-time Analytics</span>
            <span style="
                background: rgba(255,255,255,0.12);
                backdrop-filter: blur(10px);
                padding: 5px 16px;
                border-radius: 20px;
                font-size: 12px;
                color: rgba(255,255,255,0.9);
                border: 1px solid rgba(255,255,255,0.08);
            ">{total_contracts} contracts • {total_risks} risks</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # QUICK STATS - Premium Metric Cards (Perfect Spacing)
    # ========================================================================
    
    _render_premium_metrics()
    
    # ========================================================================
    # SPACER - Added to fix touch issue
    # ========================================================================
    
    st.markdown(f"""
    <div style="height: 8px;"></div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # USER INSTRUCTION PANEL - Enhanced with Premium UI (Using st.columns for proper rendering)
    # ========================================================================
    
    with st.expander("📖 How to Use Risk Intelligence Center", expanded=False):
        # Use st.columns instead of grid for better Streamlit compatibility
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: {DASHBOARD_COLORS['neutrals']['white']};
                border-radius: 10px;
                padding: 16px 18px;
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
                border-top: 3px solid {DASHBOARD_COLORS['primary']['corporate_blue']};
                height: 100%;
            ">
                <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; font-size: 15px; margin-bottom: 10px;">
                    🚀 Quick Start
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span style="font-size: 16px;">1️⃣</span>
                        <span><strong>Upload Contracts</strong> — via the Upload page</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span style="font-size: 16px;">2️⃣</span>
                        <span><strong>Scan for Risks</strong> — Click "Scan All Contracts"</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span style="font-size: 16px;">3️⃣</span>
                        <span><strong>Customize Rules</strong> — Adjust severity or add patterns</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span style="font-size: 16px;">4️⃣</span>
                        <span><strong>Export & Share</strong> — Export rules as JSON</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: {DASHBOARD_COLORS['neutrals']['white']};
                border-radius: 10px;
                padding: 16px 18px;
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
                border-top: 3px solid {DASHBOARD_COLORS['semantic']['warning']};
                height: 100%;
            ">
                <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; font-size: 15px; margin-bottom: 10px;">
                    💡 Pro Tips
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>🎯</span>
                        <span>Use custom rules for industry-specific risks</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>📊</span>
                        <span>Monitor risk trends over time</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>🔄</span>
                        <span>Import rules from team members</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>📈</span>
                        <span>Generate reports for compliance audits</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="
                background: {DASHBOARD_COLORS['neutrals']['white']};
                border-radius: 10px;
                padding: 16px 18px;
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
                border-top: 3px solid {DASHBOARD_COLORS['semantic']['info']};
                height: 100%;
            ">
                <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; font-size: 15px; margin-bottom: 10px;">
                    📊 Key Metrics
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>📊</span>
                        <span><strong>Risk Score</strong> — Composite risk indicator</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>❤️</span>
                        <span><strong>Health Status</strong> — Portfolio health overview</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>🚨</span>
                        <span><strong>Priority Items</strong> — Critical & high-risk findings</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                        <span>📈</span>
                        <span><strong>Trend Analysis</strong> — Risk patterns over time</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHECK FOR CONTRACTS
    # ========================================================================
    
    if not st.session_state.contracts:
        _render_empty_state()
        return
    
    # ========================================================================
    # INITIALIZE SCANNER
    # ========================================================================
    
    scanner = RiskScanner(st.session_state.risk_rules)
    
    # ========================================================================
    # MAIN TABS with Enhanced UI
    # ========================================================================
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Scan & Review",
        "📊 Risk Analytics",
        "⚙️ Manage Rules",
        "📤 Export/Import"
    ])
    
    with tab1:
        render_scan_tab_enhanced(scanner)
    
    with tab2:
        render_analytics_tab()
    
    with tab3:
        render_rules_tab_enhanced(scanner)
    
    with tab4:
        render_export_import_tab(scanner)


# ============================================================================
# PREMIUM METRICS SECTION - Perfect Card Consistency
# ============================================================================

def _render_premium_metrics():
    """Render premium metric cards with perfect consistency and spacing"""
    
    total_risks = len(st.session_state.risks)
    total_contracts = len(st.session_state.contracts)
    
    critical_count = sum(1 for r in st.session_state.risks if r.severity == 'critical')
    high_count = sum(1 for r in st.session_state.risks if r.severity == 'high')
    medium_count = sum(1 for r in st.session_state.risks if r.severity == 'medium')
    low_count = sum(1 for r in st.session_state.risks if r.severity == 'low')
    
    contracts_with_risks = len({r.contract_id for r in st.session_state.risks})
    healthy_contracts = total_contracts - contracts_with_risks
    
    risk_score = (critical_count * 10) + (high_count * 7) + (medium_count * 4) + (low_count * 1)
    
    if risk_score > 50:
        risk_level = "CRITICAL"
        risk_color = DASHBOARD_COLORS['semantic']['danger']
    elif risk_score > 20:
        risk_level = "MODERATE"
        risk_color = DASHBOARD_COLORS['semantic']['warning']
    else:
        risk_level = "LOW"
        risk_color = DASHBOARD_COLORS['semantic']['success']
    
    # Metric configurations for consistent rendering
    metrics = [
        {
            "icon": "⚠️",
            "value": total_risks,
            "label": "Total Risks",
            "sub": f"From {contracts_with_risks} contracts",
            "border_color": DASHBOARD_COLORS['primary']['corporate_blue'],
            "key": "total"
        },
        {
            "icon": "🔴",
            "value": critical_count + high_count,
            "label": "High Priority Risks",
            "sub": f"{critical_count} critical, {high_count} high",
            "border_color": DASHBOARD_COLORS['semantic']['danger'],
            "key": "high"
        },
        {
            "icon": "📊",
            "value": risk_score,
            "label": "Risk Score",
            "sub": risk_level,
            "border_color": risk_color,
            "key": "score"
        },
        {
            "icon": "✅",
            "value": healthy_contracts,
            "label": "Healthy Contracts",
            "sub": f"{healthy_contracts}/{total_contracts} total",
            "border_color": DASHBOARD_COLORS['semantic']['success'],
            "key": "healthy"
        }
    ]
    
    cols = st.columns(4)
    
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            st.markdown(f"""
            <div style="
                background: {DASHBOARD_COLORS['neutrals']['white']};
                border-radius: {CARD_SPACING['border_radius']};
                padding: {CARD_SPACING['padding']};
                box-shadow: {CARD_SPACING['shadow']};
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
                border-left: 4px solid {metric['border_color']};
                transition: all 0.2s ease;
                height: 100%;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
                    <span style="font-size: 28px; line-height: 1;">{metric['icon']}</span>
                    <div>
                        <div style="font-size: 28px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; line-height: 1.2;">
                            {metric['value']}
                        </div>
                    </div>
                </div>
                <div style="font-size: 14px; font-weight: 500; color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; margin-top: 2px;">
                    {metric['label']}
                </div>
                <div style="font-size: 12px; color: {DASHBOARD_COLORS['neutrals']['medium_gray']}; margin-top: 2px;">
                    {metric['sub']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def _render_empty_state():
    """Render empty state matching dashboard style"""
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 80px 40px;
        background: {DASHBOARD_COLORS['neutrals']['off_white']};
        border-radius: 20px;
        border: 2px dashed {DASHBOARD_COLORS['neutrals']['light_gray']};
        margin: 32px 0;
    ">
        <div style="font-size: 72px; margin-bottom: 20px;">📭</div>
        <div style="font-size: 26px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">
            No Contracts Uploaded
        </div>
        <div style="font-size: 16px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; margin-top: 10px; max-width: 500px; margin-left: auto; margin-right: auto;">
            Upload contracts first to scan for risks and get intelligence insights
        </div>
        <div style="margin-top: 24px; display: flex; gap: 12px; justify-content: center;">
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                padding: 8px 20px;
                border-radius: 12px;
                font-size: 13px;
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
            ">📤 Upload PDF, DOCX, TXT</span>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                padding: 8px 20px;
                border-radius: 12px;
                font-size: 13px;
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
            ">🔍 AI-Powered Analysis</span>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                padding: 8px 20px;
                border-radius: 12px;
                font-size: 13px;
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
            ">📊 Real-time Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Go to Upload", key="riskscan_goto_upload", use_container_width=True, type="primary"):
            st.session_state.page = "Upload Contracts"
            st.rerun()
    with col2:
        if st.button("🎯 Load Demo Data", key="riskscan_load_demo", use_container_width=True):
            from ..data.demo_data import load_demo_contracts
            load_demo_contracts()
            st.success("✅ Demo data loaded! Now you can scan for risks.")
            st.rerun()


# ============================================================================
# SCAN TAB - Enhanced
# ============================================================================

def render_scan_tab_enhanced(scanner):
    """Render the enhanced scan tab with premium UI"""
    
    # Action Buttons Row with consistent spacing
    st.markdown(f"""
    <div style="
        background: {DASHBOARD_COLORS['neutrals']['off_white']};
        border-radius: 16px;
        padding: 16px 20px;
        border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        margin-bottom: 20px;
    ">
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
            <span style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; font-size: 14px;">⚡ Quick Actions</span>
            <span style="flex: 1;"></span>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                font-weight: 500;
            ">📊 {len(st.session_state.risks)} risks detected</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        if st.button("🔍 Scan All Contracts", key="scan_risks_btn_enhanced", use_container_width=True, type="primary"):
            if st.session_state.contracts:
                with st.spinner("🔍 Scanning all contracts for risks..."):
                    st.session_state.risks = []
                    all_risks = scanner.scan_all_contracts(st.session_state.contracts)
                    st.session_state.risks = all_risks
                    st.session_state._last_scan_time = datetime.now()
                
                st.success(f"✅ Scan complete! Found {len(st.session_state.risks)} risks across {len(st.session_state.contracts)} contracts")
                st.balloons()
                st.rerun()
            else:
                st.warning("⚠️ No contracts to scan. Upload contracts first!")
    
    with col2:
        if st.button("🗑️ Clear Risks", key="clear_risks_btn", use_container_width=True):
            st.session_state.risks = []
            st.success("✅ All risks cleared")
            st.rerun()
    
    with col3:
        if st.button("📊 Export Report", key="export_report_btn", use_container_width=True):
            if st.session_state.risks:
                _generate_risk_report()
            else:
                st.warning("⚠️ No risks to export")
    
    with col4:
        risk_count = len(st.session_state.risks)
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['primary']['ice_blue']};
            border-radius: 12px;
            padding: 10px 16px;
            text-align: center;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 46px;
        ">
            <span style="font-size: 14px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['corporate_blue']};">
                📊 {risk_count} risks
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.session_state.risks:
        render_premium_risk_display()
    else:
        render_empty_risk_state()


def _generate_risk_report():
    """Generate and download a risk report"""
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Contract', 'Risk Type', 'Severity', 'Description', 'Recommendation', 'Detected At'])
    
    for risk in st.session_state.risks:
        writer.writerow([
            risk.contract_name,
            risk.type.replace('_', ' ').title(),
            risk.severity.capitalize(),
            risk.description,
            risk.recommendation or 'Review recommended',
            risk.detected_at.strftime('%Y-%m-%d %H:%M') if hasattr(risk, 'detected_at') else datetime.now().strftime('%Y-%m-%d %H:%M')
        ])
    
    st.download_button(
        label="📥 Download Risk Report (CSV)",
        data=output.getvalue(),
        file_name=f"risk_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        key="download_report_btn",
        use_container_width=True
    )


def render_empty_risk_state():
    """Render premium empty state with consistent styling"""
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 60px 40px;
        background: {DASHBOARD_COLORS['neutrals']['off_white']};
        border-radius: 16px;
        border: 2px dashed {DASHBOARD_COLORS['neutrals']['light_gray']};
        margin: 16px 0;
    ">
        <div style="font-size: 56px; margin-bottom: 16px;">🛡️</div>
        <div style="font-size: 22px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">
            No Risks Detected
        </div>
        <div style="font-size: 15px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; margin-top: 8px; max-width: 450px; margin-left: auto; margin-right: auto;">
            Your contracts appear clean! Click <strong>Scan All Contracts</strong> to run a comprehensive risk analysis.
        </div>
        <div style="margin-top: 16px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <span style="
                background: {DASHBOARD_COLORS['semantic']['success_bg']};
                color: {DASHBOARD_COLORS['semantic']['success']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">✅ Low Risk</span>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">📊 Ready for Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 8px;">🔍 Risk Categories Monitored</div>
            <div style="display: grid; gap: 6px;">
                <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                    <span>🔴</span> Unlimited Liability - High risk exposure
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                    <span>🟠</span> Auto-Renewal - May lock you in
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                    <span>🟡</span> No Termination - Inflexible terms
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
                    <span>🟡</span> Broad Indemnification - Potential liability
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 8px;">💡 Next Steps</div>
            <div style="display: grid; gap: 6px;">
                <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">1. 📤 Upload more contracts for comprehensive analysis</div>
                <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">2. ⚙️ Customize rules for industry-specific risks</div>
                <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">3. 📤 Export rules to share with your team</div>
                <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">4. 📊 Generate compliance-ready risk reports</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_premium_risk_display():
    """Render risks with premium UI and consistent card styling"""
    
    severity_counts = {
        'critical': sum(1 for r in st.session_state.risks if r.severity == 'critical'),
        'high': sum(1 for r in st.session_state.risks if r.severity == 'high'),
        'medium': sum(1 for r in st.session_state.risks if r.severity == 'medium'),
        'low': sum(1 for r in st.session_state.risks if r.severity == 'low')
    }
    
    total = sum(severity_counts.values())
    
    if total > 0:
        # Section header with consistent styling
        st.markdown(f"""
        <div style="margin: 20px 0 16px 0;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <h2 style="font-size: 22px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin: 0;">
                    📊 Risk Distribution Dashboard
                </h2>
                <span style="
                    background: {DASHBOARD_COLORS['primary']['ice_blue']};
                    color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                    padding: 4px 14px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 500;
                ">{total} total risks</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create bar chart using Streamlit
        df_severity = pd.DataFrame({
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Count': [severity_counts['critical'], severity_counts['high'], 
                     severity_counts['medium'], severity_counts['low']]
        })
        st.bar_chart(df_severity.set_index('Severity'), height=280)
        
        # Quick summary cards with consistent styling
        severity_cards = [
            {"label": "Critical", "count": severity_counts['critical'], "color": DASHBOARD_COLORS['semantic']['danger'], "icon": "🔴"},
            {"label": "High", "count": severity_counts['high'], "color": DASHBOARD_COLORS['semantic']['warning'], "icon": "🟠"},
            {"label": "Medium", "count": severity_counts['medium'], "color": DASHBOARD_COLORS['primary']['corporate_blue'], "icon": "🟡"},
            {"label": "Low", "count": severity_counts['low'], "color": DASHBOARD_COLORS['semantic']['success'], "icon": "🔵"}
        ]
        
        cols = st.columns(4)
        for idx, card in enumerate(severity_cards):
            with cols[idx]:
                st.markdown(f"""
                <div style="
                    background: {DASHBOARD_COLORS['neutrals']['white']};
                    border-radius: 12px;
                    padding: 14px 16px;
                    border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
                    text-align: center;
                    border-top: 3px solid {card['color']};
                ">
                    <div style="font-size: 24px; margin-bottom: 2px;">{card['icon']}</div>
                    <div style="font-size: 24px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">{card['count']}</div>
                    <div style="font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">{card['label']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Contract Risk Portfolio
    st.markdown(f"""
    <div style="margin: 20px 0 16px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin: 0;">
                📋 Contract Risk Portfolio
            </h2>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">Health status overview</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    contracts_with_risks = []
    for contract in st.session_state.contracts:
        contract_risks = [r for r in st.session_state.risks if r.contract_id == contract.id]
        if contract_risks:
            has_critical = any(r.severity == 'critical' for r in contract_risks)
            has_high = any(r.severity == 'high' for r in contract_risks)
            contracts_with_risks.append((contract, contract_risks, has_critical, has_high))
    
    contracts_with_risks.sort(key=lambda x: (not x[2], not x[3], -len(x[1])))
    
    for contract, contract_risks, has_critical, has_high in contracts_with_risks:
        render_premium_health_card(contract, len(contract_risks), has_critical, has_high)
        
        with st.expander(f"📋 View {len(contract_risks)} Risks", expanded=has_critical):
            for idx, risk in enumerate(contract_risks):
                render_premium_risk_card(risk, idx)


def render_premium_risk_card(risk, index):
    """Render a premium risk card with consistent styling"""
    
    severity_data = RISK_SEVERITIES.get(risk.severity, {})
    severity_color = severity_data.get('color', '#475569')
    severity_bg = severity_data.get('bg', '#F8FAFE')
    severity_icon = severity_data.get('icon', '⚠️')
    severity_label = severity_data.get('label', risk.severity.capitalize())
    
    recommendation_text = risk.recommendation if risk.recommendation else getattr(risk, 'recommendation_default', None)
    
    st.markdown(f"""
    <div style="
        background: {severity_bg};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        border-left: 4px solid {severity_color};
        box-shadow: {CARD_SPACING['shadow']};
        border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        border-left-width: 4px;
        transition: all 0.2s ease;
    ">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 20px;">{severity_icon}</span>
            <strong style="font-size: 15px; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">{risk.type.replace('_', ' ').title()}</strong>
            <span style="
                background: {severity_color}; 
                color: white; 
                padding: 2px 14px; 
                border-radius: 12px; 
                font-size: 11px; 
                font-weight: 600;
            ">{severity_label}</span>
            <span style="
                background: {DASHBOARD_COLORS['neutrals']['white']}; 
                color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; 
                padding: 2px 10px; 
                border-radius: 10px; 
                font-size: 11px; 
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            ">📄 {risk.contract_name[:25]}{'...' if len(risk.contract_name) > 25 else ''}</span>
            <span style="
                background: {DASHBOARD_COLORS['neutrals']['white']}; 
                color: {DASHBOARD_COLORS['neutrals']['medium_gray']}; 
                padding: 2px 10px; 
                border-radius: 10px; 
                font-size: 10px; 
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            ">#{index + 1}</span>
        </div>
        <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; margin: 4px 0;">
            {risk.description}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if recommendation_text:
        st.info(f"💡 {recommendation_text}")
    
    if risk.clause_text:
        with st.expander("📄 View Clause Context"):
            st.caption(risk.clause_text[:500] + ("..." if len(risk.clause_text) > 500 else ""))


def render_premium_health_card(contract, risk_count, has_critical, has_high):
    """Render a premium contract health card with consistent styling"""
    
    health_score = contract.health_score if hasattr(contract, 'health_score') else max(0, min(100, 100 - (risk_count * 5)))
    
    if has_critical:
        status = "🔴 Critical"
        status_color = DASHBOARD_COLORS['semantic']['danger']
        bg_color = DASHBOARD_COLORS['semantic']['danger_bg']
    elif has_high:
        status = "🟠 At Risk"
        status_color = DASHBOARD_COLORS['semantic']['warning']
        bg_color = DASHBOARD_COLORS['semantic']['warning_bg']
    elif risk_count > 0:
        status = "🟡 Needs Review"
        status_color = DASHBOARD_COLORS['semantic']['warning']
        bg_color = DASHBOARD_COLORS['semantic']['warning_bg']
    else:
        status = "🟢 Healthy"
        status_color = DASHBOARD_COLORS['semantic']['success']
        bg_color = DASHBOARD_COLORS['semantic']['success_bg']
    
    st.markdown(f"""
    <div style="
        background: {DASHBOARD_COLORS['neutrals']['white']};
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 12px;
        border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        box-shadow: {CARD_SPACING['shadow']};
        transition: all 0.2s ease;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="flex: 1; min-width: 200px;">
                <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; font-size: 16px;">
                    {contract.name[:45]}{'...' if len(contract.name) > 45 else ''}
                </div>
                <div style="font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['medium_gray']}; margin-top: 2px;">
                    📄 {contract.pages} pages • 📝 {contract.clause_count} clauses • ⚠️ {risk_count} risks
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
                <div style="text-align: right; min-width: 80px;">
                    <div style="font-size: 12px; color: {DASHBOARD_COLORS['neutrals']['medium_gray']};">Health Score</div>
                    <div style="font-size: 22px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">{health_score}%</div>
                </div>
                <div style="
                    background: {bg_color};
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                    color: {status_color};
                    border: 1px solid {status_color}40;
                ">{status}</div>
            </div>
        </div>
        <div style="margin-top: 12px;">
            <div style="
                width: 100%;
                height: 6px;
                background: {DASHBOARD_COLORS['neutrals']['light_gray']};
                border-radius: 4px;
                overflow: hidden;
            ">
                <div style="
                    width: {health_score}%;
                    height: 100%;
                    background: {status_color};
                    border-radius: 4px;
                    transition: width 0.6s ease;
                "></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ANALYTICS TAB - Enhanced
# ============================================================================

def render_analytics_tab():
    """Render the analytics tab with insights"""
    
    st.markdown(f"""
    <div style="margin: 0 0 20px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin: 0;">
                📊 Risk Analytics Dashboard
            </h2>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">Deep insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.risks:
        st.info("📭 No risks to analyze. Run a risk scan first!")
        if st.button("🔍 Run Risk Scan Now", key="analytics_run_scan", use_container_width=True):
            st.rerun()
        return
    
    total_risks = len(st.session_state.risks)
    total_contracts = len(st.session_state.contracts)
    affected_contracts = len({r.contract_id for r in st.session_state.risks})
    
    # Analytics metrics with consistent cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            text-align: center;
        ">
            <div style="font-size: 28px;">📊</div>
            <div style="font-size: 24px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">{total_risks}</div>
            <div style="font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">Total Risks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            text-align: center;
        ">
            <div style="font-size: 28px;">📄</div>
            <div style="font-size: 24px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">{affected_contracts}</div>
            <div style="font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">Affected Contracts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_risks = total_risks / affected_contracts if affected_contracts > 0 else 0
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            text-align: center;
        ">
            <div style="font-size: 28px;">📈</div>
            <div style="font-size: 24px; font-weight: 700; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">{avg_risks:.1f}</div>
            <div style="font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">Avg Risks/Contract</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        high_priority = sum(1 for r in st.session_state.risks if r.severity in ['critical', 'high'])
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            text-align: center;
            border-top: 3px solid {DASHBOARD_COLORS['semantic']['danger']};
        ">
            <div style="font-size: 28px;">🚨</div>
            <div style="font-size: 24px; font-weight: 700; color: {DASHBOARD_COLORS['semantic']['danger']};">{high_priority}</div>
            <div style="font-size: 13px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">High Priority Risks</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 12px;">🔍 Risk Type Distribution</div>
        """, unsafe_allow_html=True)
        
        type_counts = defaultdict(int)
        for risk in st.session_state.risks:
            type_counts[risk.type.replace('_', ' ').title()] += 1
        
        type_df = pd.DataFrame({
            'Risk Type': list(type_counts.keys()),
            'Count': list(type_counts.values())
        })
        type_df = type_df.sort_values('Count', ascending=False)
        
        st.dataframe(
            type_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Risk Type": st.column_config.TextColumn("Risk Type", width="medium"),
                "Count": st.column_config.NumberColumn("Count", width="small")
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 12px;">📋 Risk by Contract</div>
        """, unsafe_allow_html=True)
        
        contract_data = []
        for contract in st.session_state.contracts:
            risk_count = len([r for r in st.session_state.risks if r.contract_id == contract.id])
            if risk_count > 0:
                critical = sum(1 for r in st.session_state.risks if r.contract_id == contract.id and r.severity == 'critical')
                high = sum(1 for r in st.session_state.risks if r.contract_id == contract.id and r.severity == 'high')
                contract_data.append({
                    "Contract": contract.name[:30] + ('...' if len(contract.name) > 30 else ''),
                    "Risks": risk_count,
                    "Critical": critical,
                    "High": high
                })
        
        if contract_data:
            contract_df = pd.DataFrame(contract_data)
            contract_df = contract_df.sort_values('Risks', ascending=False)
            st.dataframe(contract_df, use_container_width=True, hide_index=True)
        else:
            st.info("No contracts with risks detected")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Actionable Recommendations with consistent styling
    st.markdown(f"""
    <div style="margin: 16px 0 12px 0;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <span style="font-size: 22px;">💡</span>
            <h3 style="font-size: 18px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin: 0;">
                Actionable Recommendations
            </h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    recommendations = []
    
    critical_risks = [r for r in st.session_state.risks if r.severity == 'critical']
    if critical_risks:
        contracts_with_critical = {r.contract_name for r in critical_risks}
        recommendations.append({
            "icon": "🔴",
            "text": f"Review {len(critical_risks)} critical risks in {len(contracts_with_critical)} contracts immediately",
            "severity": "critical"
        })
    
    high_risks = [r for r in st.session_state.risks if r.severity == 'high']
    if high_risks:
        recommendations.append({
            "icon": "🟠",
            "text": f"Address {len(high_risks)} high-risk clauses within 7 days",
            "severity": "high"
        })
    
    unlimited = [r for r in st.session_state.risks if 'unlimited_liability' in r.type]
    if unlimited:
        recommendations.append({
            "icon": "💰",
            "text": f"Cap unlimited liability in {len(unlimited)} contracts to reduce exposure",
            "severity": "medium"
        })
    
    auto_renewal = [r for r in st.session_state.risks if 'auto_renewal' in r.type]
    if auto_renewal:
        recommendations.append({
            "icon": "🔄",
            "text": f"Review auto-renewal clauses in {len(auto_renewal)} contracts",
            "severity": "medium"
        })
    
    if not recommendations:
        recommendations.append({
            "icon": "✅",
            "text": "No critical issues found. Continue monitoring your contract portfolio.",
            "severity": "low"
        })
    
    for rec in recommendations:
        color_map = {
            'critical': DASHBOARD_COLORS['semantic']['danger'],
            'high': DASHBOARD_COLORS['semantic']['warning'],
            'medium': DASHBOARD_COLORS['primary']['corporate_blue'],
            'low': DASHBOARD_COLORS['semantic']['success']
        }
        bg_map = {
            'critical': DASHBOARD_COLORS['semantic']['danger_bg'],
            'high': DASHBOARD_COLORS['semantic']['warning_bg'],
            'medium': DASHBOARD_COLORS['primary']['ice_blue'],
            'low': DASHBOARD_COLORS['semantic']['success_bg']
        }
        
        st.markdown(f"""
        <div style="
            background: {bg_map[rec['severity']]};
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 8px;
            border-left: 4px solid {color_map[rec['severity']]};
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span style="font-size: 18px;">{rec['icon']}</span>
            <span style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">{rec['text']}</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# RULES TAB - Enhanced
# ============================================================================

def render_rules_tab_enhanced(scanner):
    """Render the enhanced rules management tab"""
    
    st.markdown(f"""
    <div style="margin: 0 0 20px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin: 0;">
                ⚙️ Risk Rules Management
            </h2>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">{len(scanner.rules)} active rules</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    💡 **How It Works**: Adjust severity levels, add custom patterns, delete rules you don't need, and export rules to share or backup.
    """)
    
    st.divider()
    
    st.markdown("#### 📋 Active Rules")
    
    if not scanner.rules:
        st.warning("No rules configured. Add custom rules below.")
    else:
        rules_data = []
        for rule_key, rule in scanner.rules.items():
            severity = rule.get('severity', 'low')
            severity_icon = RISK_SEVERITIES.get(severity, {}).get('icon', '⚠️')
            rules_data.append({
                "Rule": rule_key.replace('_', ' ').title(),
                "Severity": f"{severity_icon} {severity.capitalize()}",
                "Pattern": rule.get('pattern', ''),
                "Description": rule.get('description', '')[:60] + ('...' if len(rule.get('description', '')) > 60 else '')
            })
        
        df = pd.DataFrame(rules_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 12px;">✏️ Update Rule Severity</div>
        """, unsafe_allow_html=True)
        
        rule_keys = list(scanner.rules.keys())
        if rule_keys:
            selected_rule = st.selectbox("Select Rule", options=rule_keys, key="rule_select")
            
            current_severity = scanner.rules[selected_rule].get('severity', 'low')
            new_severity = st.selectbox(
                "New Severity",
                options=['critical', 'high', 'medium', 'low'],
                index=['critical', 'high', 'medium', 'low'].index(current_severity),
                key="severity_select"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔄 Update Severity", key="update_severity_btn", use_container_width=True):
                    scanner.update_rule_severity(selected_rule, new_severity)
                    st.session_state.risk_rules = scanner.rules
                    st.success(f"✅ Updated severity to {new_severity}")
                    st.rerun()
            
            with col_b:
                if st.button("🗑️ Delete Rule", key="delete_rule_btn", use_container_width=True):
                    scanner.remove_rule(selected_rule)
                    st.session_state.risk_rules = scanner.rules
                    st.success(f"✅ Deleted rule: {selected_rule}")
                    st.rerun()
        else:
            st.info("No rules available to manage")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 16px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 12px;">➕ Add Custom Rule</div>
        """, unsafe_allow_html=True)
        
        with st.form("add_custom_rule_form_enhanced"):
            rule_key = st.text_input("Rule Key", placeholder="e.g., 'unlimited_liability'")
            pattern = st.text_input("Regex Pattern", placeholder="e.g., 'unlimited liability'")
            severity = st.selectbox("Severity", options=['critical', 'high', 'medium', 'low'])
            description = st.text_area("Description", placeholder="Describe this risk rule")
            
            submitted = st.form_submit_button("➕ Add Custom Rule", use_container_width=True)
            
            if submitted:
                if not rule_key or not pattern or not description:
                    st.error("❌ Please fill in all fields")
                else:
                    rule_key = rule_key.lower().replace(' ', '_')
                    try:
                        scanner.add_custom_rule(rule_key, pattern, severity, description)
                        st.session_state.risk_rules = scanner.rules
                        st.success(f"✅ Added custom rule: {rule_key}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error adding rule: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("#### 💡 Suggested Rule Patterns")
    
    suggestions = [
        {"name": "Excessive Liability", "pattern": r"liability.*exceed.*(?:10|15|20)\s*(?:million|M)", "severity": "critical"},
        {"name": "Missing Termination", "pattern": r"(?i)(?!.*termination)", "severity": "high"},
        {"name": "Short Renewal", "pattern": r"renew.*(?:30|45)\s*days", "severity": "medium"},
        {"name": "Exclusive Rights", "pattern": r"exclusive.*rights", "severity": "medium"},
        {"name": "Non-Compete", "pattern": r"non-?compete", "severity": "low"},
    ]
    
    cols = st.columns(2)
    for idx, suggestion in enumerate(suggestions):
        with cols[idx % 2]:
            severity_icon = RISK_SEVERITIES.get(suggestion['severity'], {}).get('icon', '⚠️')
            st.markdown(f"""
            <div style="
                background: {DASHBOARD_COLORS['neutrals']['white']};
                border-radius: 10px;
                padding: 14px 16px;
                border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
                margin-bottom: 10px;
            ">
                <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']};">
                    {severity_icon} {suggestion['name']}
                </div>
                <div style="font-size: 12px; color: {DASHBOARD_COLORS['neutrals']['medium_gray']}; margin-top: 4px;">
                    Pattern: <code style="background: {DASHBOARD_COLORS['neutrals']['off_white']}; padding: 2px 6px; border-radius: 4px;">{suggestion['pattern']}</code>
                </div>
                <div style="font-size: 12px; color: {DASHBOARD_COLORS['neutrals']['medium_gray']};">
                    Severity: <strong>{suggestion['severity'].capitalize()}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"➕ Add {suggestion['name']}", key=f"add_suggestion_{idx}", use_container_width=True):
                try:
                    rule_key = suggestion['name'].lower().replace(' ', '_')
                    scanner.add_custom_rule(rule_key, suggestion['pattern'], suggestion['severity'], f"Detects {suggestion['name'].lower()} patterns")
                    st.session_state.risk_rules = scanner.rules
                    st.success(f"✅ Added rule: {suggestion['name']}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding rule: {str(e)}")


# ============================================================================
# EXPORT/IMPORT TAB - Enhanced
# ============================================================================

def render_export_import_tab(scanner):
    """Render the export/import tab"""
    
    st.markdown(f"""
    <div style="margin: 0 0 20px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin: 0;">
                📤 Export & Import Risk Rules
            </h2>
            <span style="
                background: {DASHBOARD_COLORS['primary']['ice_blue']};
                color: {DASHBOARD_COLORS['primary']['corporate_blue']};
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">Share & backup</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 20px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            height: 100%;
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 8px;">📥 Export Rules</div>
            <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; margin-bottom: 16px;">
                Download your current risk rules as a JSON file for backup or sharing.
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📥 Export Rules", key="export_rules_btn_enhanced", use_container_width=True):
            rules_json = scanner.export_rules()
            st.download_button(
                label="📥 Download Rules JSON",
                data=rules_json,
                file_name=f"risk_rules_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="download_rules_btn_enhanced",
                use_container_width=True
            )
            st.success("✅ Rules exported successfully!")
        
        st.caption(f"📊 {len(scanner.rules)} rules currently active")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {DASHBOARD_COLORS['neutrals']['white']};
            border-radius: 12px;
            padding: 20px;
            border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
            height: 100%;
        ">
            <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 8px;">📤 Import Rules</div>
            <div style="font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']}; margin-bottom: 16px;">
                Upload a JSON file to restore previously exported rules.
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_rules = st.file_uploader(
            "Drop your rules JSON file here",
            type=['json'],
            key="import_rules_uploader_enhanced",
            help="Upload a JSON file exported from RiskScan"
        )
        
        if uploaded_rules:
            try:
                rules_content = uploaded_rules.read().decode('utf-8')
                
                with st.expander("📋 Preview Import", expanded=False):
                    try:
                        preview_data = json.loads(rules_content)
                        st.json(preview_data)
                    except:
                        st.warning("Could not preview file content")
                
                if st.button("🔄 Import Rules", key="import_rules_btn_enhanced", use_container_width=True):
                    if scanner.import_rules(rules_content):
                        st.session_state.risk_rules = scanner.rules
                        st.success(f"✅ Rules imported successfully! {len(scanner.rules)} rules loaded.")
                        st.rerun()
                    else:
                        st.error("❌ Invalid rules file format")
                        
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown(f"""
    <div style="
        background: {DASHBOARD_COLORS['primary']['ice_blue']};
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid {DASHBOARD_COLORS['neutrals']['border']};
    ">
        <div style="font-weight: 600; color: {DASHBOARD_COLORS['primary']['deepest_navy']}; margin-bottom: 8px;">💾 Backup & Versioning Best Practices</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 14px; color: {DASHBOARD_COLORS['neutrals']['dark_gray']};">
            <div>• Export rules before major changes to keep a backup</div>
            <div>• Use version control in your filename (e.g., risk_rules_v2.json)</div>
            <div>• Share rules with your team for consistent risk detection</div>
            <div>• Import rules to quickly restore custom configurations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")