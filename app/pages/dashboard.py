"""
KontractIQ - Dashboard Page
Main landing page with key metrics 
"""

import streamlit as st
from datetime import datetime
from typing import List, Optional

# ============================================================================
# IMPORTS
# ============================================================================

from ..utils.constants import COLORS, PRO_TIPS, QUICK_ACTIONS, DEMO_CONTRACT_NAMES
from ..data.demo_data import load_demo_contracts


def render_dashboard() -> None:
    """
    Render the dashboard page - COMPLETELY FIXED
    """
    
    # ========================================================================
    # HERO SECTION - Using Streamlit components
    # ========================================================================
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
        padding: 32px 40px;
        border-radius: 20px;
        margin-bottom: 24px;
        color: white;
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; right: 20px; bottom: -10px; font-size: 100px; opacity: 0.05;">⚖️</div>
        <h1 style="font-size: 32px; font-weight: 700; margin: 0; color: white;">Welcome to KontractIQ</h1>
        <p style="font-size: 16px; opacity: 0.85; margin: 8px 0 0 0; color: rgba(255,255,255,0.85);">
            Intelligence for every clause.
        </p>
        <p style="font-size: 13px; opacity: 0.6; margin: 4px 0 0 0; color: rgba(255,255,255,0.6);">
            {_get_contract_stats_summary()}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # QUICK STATS - 4 Metric Cards
    # ========================================================================
    
    _render_metrics_section()
    
    # ========================================================================
    # QUICK ACTIONS - 6 Action Buttons
    # ========================================================================
    
    _render_quick_actions()
    
    # ========================================================================
    # CHARTS SECTION - 2 Column Layout
    # ========================================================================
    
    _render_charts_section()
    
    # ========================================================================
    # RECENT ACTIVITY & TIPS - 2 Column Layout
    # ========================================================================
    
    _render_activity_and_tips()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_contract_stats_summary() -> str:
    """Get summary of contract stats"""
    total = len(st.session_state.contracts)
    clauses = len(st.session_state.clauses)
    risks = len(st.session_state.risks)
    
    if total == 0:
        return "Upload contracts to get started"
    
    return f"{total} contracts • {clauses} clauses extracted • {risks} risks detected"


def _render_metrics_section() -> None:
    """Render the metrics section - FIXED"""
    
    total_contracts = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    total_risks = len(st.session_state.risks)
    critical_risks = sum(1 for r in st.session_state.risks if r.severity == "critical")
    demo_active = st.session_state.get('demo_mode', False)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(10, 38, 71, 0.06);
            border: 1px solid {COLORS['neutrals']['light_gray']};
            border-left: 4px solid {COLORS['primary']['corporate_blue']};
        ">
            <div style="font-size: 28px; margin-bottom: 4px;">📄</div>
            <div style="font-size: 28px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">{total_contracts}</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">Total Contracts</div>
            <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">In session</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(10, 38, 71, 0.06);
            border: 1px solid {COLORS['neutrals']['light_gray']};
            border-left: 4px solid {COLORS['semantic']['success']};
        ">
            <div style="font-size: 28px; margin-bottom: 4px;">📝</div>
            <div style="font-size: 28px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">{total_clauses}</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">Clauses Extracted</div>
            <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">From {total_contracts} contract(s)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(10, 38, 71, 0.06);
            border: 1px solid {COLORS['neutrals']['light_gray']};
            border-left: 4px solid {COLORS['semantic']['warning']};
        ">
            <div style="font-size: 28px; margin-bottom: 4px;">⚠️</div>
            <div style="font-size: 28px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">{total_risks}</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">Total Risks</div>
            <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">{critical_risks} critical</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status_text = "Active" if demo_active else "Inactive"
        status_color = COLORS['semantic']['success'] if demo_active else COLORS['neutrals']['medium_gray']
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(10, 38, 71, 0.06);
            border: 1px solid {COLORS['neutrals']['light_gray']};
            border-left: 4px solid {status_color};
        ">
            <div style="font-size: 28px; margin-bottom: 4px;">{'✅' if demo_active else '⭕'}</div>
            <div style="font-size: 28px; font-weight: 600; color: {status_color};">{status_text}</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">Demo Mode</div>
            <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">Sample contracts</div>
        </div>
        """, unsafe_allow_html=True)


def _render_quick_actions() -> None:
    """Render quick action buttons - FIXED"""
    
    st.markdown(f"""
    <div style="margin: 24px 0 16px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin: 0;">🚀 Quick Actions</h2>
            <span style="
                background: {COLORS['primary']['ice_blue']};
                color: {COLORS['primary']['corporate_blue']};
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">{len(st.session_state.contracts)} contracts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(6)
    
    actions = [
        {"icon": "📤", "label": "Upload", "page": "Upload Contracts"},
        {"icon": "🔍", "label": "Search", "page": "Search"},
        {"icon": "📊", "label": "Report", "page": "Reports"},
        {"icon": "⚠️", "label": "Scan Risks", "page": "RiskScan"},
        {"icon": "📝", "label": "Create", "page": "Create Contract"},
        {"icon": "📈", "label": "Metrics", "page": "System Metrics"}
    ]
    
    for idx, action in enumerate(actions):
        with cols[idx]:
            if st.button(
                f"{action['icon']}\n{action['label']}",
                key=f"dash_action_{idx}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.page = action['page']
                st.rerun()


def _render_charts_section() -> None:
    """Render the charts section - FIXED"""
    
    st.markdown(f"""
    <div style="margin: 24px 0 16px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin: 0;">📊 Analytics</h2>
            <span style="
                background: {COLORS['primary']['ice_blue']};
                color: {COLORS['primary']['corporate_blue']};
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">Visual Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.contracts:
        _render_empty_charts_state()
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk Distribution
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 16px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">Risk Distribution</span>
                <span style="
                    background: {COLORS['primary']['ice_blue']};
                    color: {COLORS['primary']['corporate_blue']};
                    padding: 2px 10px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                ">{len(st.session_state.risks)} total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.risks:
            _render_simple_risk_chart()
        else:
            st.info("ℹ️ No risks detected. Upload contracts and run RiskScan.")
    
    with col2:
        # Clause Distribution
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 16px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">Clause Distribution</span>
                <span style="
                    background: {COLORS['primary']['ice_blue']};
                    color: {COLORS['primary']['corporate_blue']};
                    padding: 2px 10px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                ">{len(st.session_state.clauses)} total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.clauses:
            _render_simple_clause_chart()
        else:
            st.info("ℹ️ No clauses extracted yet.")


def _render_empty_charts_state() -> None:
    """Render empty state for charts - FIXED"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 48px 24px;
            background: {COLORS['neutrals']['off_white']};
            border-radius: 16px;
            border: 2px dashed {COLORS['neutrals']['light_gray']};
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 48px; margin-bottom: 12px;">📭</div>
            <div style="font-size: 18px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">No Contracts Yet</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']}; margin-top: 8px;">
                Upload contracts to see risk<br>distribution, clause types, and more
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 48px 24px;
            background: {COLORS['neutrals']['off_white']};
            border-radius: 16px;
            border: 2px dashed {COLORS['neutrals']['light_gray']};
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 48px; margin-bottom: 12px;">📊</div>
            <div style="font-size: 18px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">Charts Will Appear Here</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']}; margin-top: 8px;">
                Upload contracts to see<br>visual insights and analytics
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_simple_risk_chart() -> None:
    """Render a simple risk distribution chart using Streamlit - FIXED"""
    severity_counts = {
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    for risk in st.session_state.risks:
        if risk.severity in severity_counts:
            severity_counts[risk.severity] += 1
    
    # Create a simple bar chart using Streamlit
    import pandas as pd
    df = pd.DataFrame({
        'Severity': ['Critical', 'High', 'Medium', 'Low'],
        'Count': [
            severity_counts['critical'],
            severity_counts['high'],
            severity_counts['medium'],
            severity_counts['low']
        ]
    })
    
    st.bar_chart(df.set_index('Severity'), height=250)


def _render_simple_clause_chart() -> None:
    """Render a simple clause distribution chart using Streamlit - FIXED"""
    type_counts = {}
    for clause in st.session_state.clauses:
        type_counts[clause.type] = type_counts.get(clause.type, 0) + 1
    
    # Create a simple bar chart using Streamlit
    import pandas as pd
    df = pd.DataFrame({
        'Clause Type': list(type_counts.keys()),
        'Count': list(type_counts.values())
    })
    
    if not df.empty:
        st.bar_chart(df.set_index('Clause Type'), height=250)


def _render_activity_and_tips() -> None:
    """Render recent activity and pro tips - FIXED"""
    
    st.markdown("""
    <div style="margin: 24px 0 16px 0;">
        <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 24px 0;">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin: 0;">📋 Recent Activity</h2>
            <span style="
                background: {COLORS['primary']['ice_blue']};
                color: {COLORS['primary']['corporate_blue']};
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">Last {min(5, len(st.session_state.contracts))} contracts</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.contracts:
            _render_recent_contracts()
        else:
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 32px 24px;
                background: {COLORS['neutrals']['off_white']};
                border-radius: 16px;
                border: 2px dashed {COLORS['neutrals']['light_gray']};
            ">
                <div style="font-size: 32px; margin-bottom: 8px;">📭</div>
                <div style="font-size: 16px; font-weight: 500; color: {COLORS['primary']['deepest_navy']};">No recent activity</div>
                <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']}; margin-top: 4px;">
                    Upload your first contract to get started
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <h2 style="font-size: 22px; font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin: 0;">💡 Pro Tips</h2>
        </div>
        """, unsafe_allow_html=True)
        
        _render_pro_tips()


def _render_recent_contracts() -> None:
    """Render recent contracts list - FIXED"""
    recent_contracts = sorted(
        st.session_state.contracts,
        key=lambda c: c.upload_date,
        reverse=True
    )[:5]
    
    for contract in recent_contracts:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background: {COLORS['neutrals']['white']};
            border-radius: 12px;
            border: 1px solid {COLORS['neutrals']['light_gray']};
            margin-bottom: 8px;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 20px;">{'📄' if contract.file_type == 'pdf' else '📝' if contract.file_type == 'docx' else '📃'}</span>
                <div>
                    <div style="font-weight: 500; color: {COLORS['primary']['deepest_navy']};">
                        {contract.name[:35]}{'...' if len(contract.name) > 35 else ''}
                    </div>
                    <div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']};">
                        {contract.file_type.upper()} • {contract.clause_count} clauses • {contract.risk_count} risks
                    </div>
                </div>
            </div>
            <div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']};">
                {contract.upload_date.strftime('%b %d, %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_pro_tips() -> None:
    """Render pro tips list - FIXED"""
    # Show tips in a clean list
    for tip in PRO_TIPS[:6]:
        st.markdown(f"""
        <div style="
            padding: 10px 14px;
            margin-bottom: 8px;
            background: {COLORS['neutrals']['off_white']};
            border-radius: 10px;
            border-left: 3px solid {COLORS['primary']['corporate_blue']};
            font-size: 14px;
            color: {COLORS['neutrals']['dark_gray']};
        ">
            {tip}
        </div>
        """, unsafe_allow_html=True)