"""
KontractIQ - Contract Explorer Page
Professional Design with User Instructions
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Optional, Dict, Any
from ..utils.constants import COLORS, CONTRACT_STATUS_COLORS, CONTRACT_STATUS_LABELS
from ..utils.helpers import format_file_size, truncate_text, get_risk_severity_color
from ..data.demo_data import load_demo_contracts, clear_demo_data, is_demo_contract
from ..models.contract import Contract


def render_contract_explorer():
    """Render the contract explorer with Premium UI"""
    
    # Apply premium styles
    _apply_premium_styles()
    
    # Hero Section
    _render_hero_section()
    
    # User Instructions - Always visible for new users
    _render_instructions()
    
    if not st.session_state.contracts:
        _render_empty_state()
        return
    
    # Stats Row
    _render_stats_row()
    
    # Filters
    filtered_contracts = _render_filters()
    
    # Action Bar
    _render_action_bar()
    
    # Contracts Grid
    if filtered_contracts:
        _render_contracts_grid(filtered_contracts)
    else:
        st.info("🔍 No contracts match your filters")
    
    # Analytics
    if len(filtered_contracts) > 1:
        _render_analytics(filtered_contracts)


def _apply_premium_styles():
    """Apply premium styles with safe CSS"""
    st.markdown("""
    <style>
        /* ===== HERO CARD ===== */
        .hero-card {
            background: linear-gradient(135deg, #0A2647 0%, #1B3A5C 50%, #2C5F8A 100%);
            border-radius: 20px;
            padding: 28px 36px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(10, 38, 71, 0.15);
        }
        
        .hero-card .glow1 {
            position: absolute;
            top: -40%;
            right: -10%;
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(44, 95, 138, 0.2) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }
        
        .hero-card .glow2 {
            position: absolute;
            bottom: -30%;
            left: -5%;
            width: 250px;
            height: 250px;
            background: radial-gradient(circle, rgba(74, 127, 165, 0.12) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }
        
        .hero-card .content {
            position: relative;
            z-index: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        
        .hero-card .left {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .hero-card .icon {
            font-size: 36px;
        }
        
        .hero-card .title {
            font-size: 24px;
            font-weight: 700;
            color: white;
            margin: 0;
            letter-spacing: -0.02em;
        }
        
        .hero-card .subtitle {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
            margin: 2px 0 0 0;
        }
        
        .hero-card .badges {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .hero-card .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            color: white;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        .hero-card .badge:hover {
            background: rgba(255, 255, 255, 0.18);
            transition: all 0.3s ease;
        }
        
        .hero-card .stats {
            display: flex;
            gap: 24px;
            margin-top: 12px;
        }
        
        .hero-card .stat-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .hero-card .stat-value {
            font-size: 18px;
            font-weight: 700;
            color: white;
        }
        
        .hero-card .stat-label {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* ===== INSTRUCTION CARD ===== */
        .instruction-card {
            background: #F8FAFE;
            border-radius: 14px;
            padding: 16px 22px;
            margin-bottom: 16px;
            border: 1px solid #E8F1F8;
            border-left: 4px solid #2C5F8A;
        }
        
        .instruction-card .header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .instruction-card .header .icon {
            font-size: 20px;
        }
        
        .instruction-card .header .title {
            font-size: 15px;
            font-weight: 600;
            color: #0A2647;
        }
        
        .instruction-card .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
        }
        
        .instruction-card .item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            background: white;
            border-radius: 10px;
            border: 1px solid #E8F1F8;
        }
        
        .instruction-card .item .emoji {
            font-size: 16px;
        }
        
        .instruction-card .item .text {
            font-size: 13px;
            color: #0A2647;
        }
        
        .instruction-card .item .desc {
            font-size: 11px;
            color: #94A3B8;
        }
        
        /* ===== CONTRACT CARD ===== */
        .contract-card {
            background: white;
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 10px;
            border: 1px solid #E8F1F8;
            box-shadow: 0 1px 3px rgba(10, 38, 71, 0.03);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .contract-card:hover {
            border-color: #2C5F8A;
            box-shadow: 0 4px 20px rgba(10, 38, 71, 0.06);
            transform: translateY(-2px);
        }
        
        .contract-card .accent {
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            border-radius: 4px 0 0 4px;
        }
        
        .contract-card .top-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            flex-wrap: wrap;
        }
        
        .contract-card .left-section {
            display: flex;
            gap: 12px;
            flex: 1;
            min-width: 0;
        }
        
        .contract-card .file-icon {
            font-size: 22px;
            line-height: 1;
            margin-top: 2px;
        }
        
        .contract-card .info {
            min-width: 0;
            flex: 1;
        }
        
        .contract-card .contract-name {
            font-size: 15px;
            font-weight: 600;
            color: #0A2647;
        }
        
        .contract-card .contract-meta {
            font-size: 12px;
            color: #94A3B8;
            margin-top: 2px;
        }
        
        .contract-card .tags {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-top: 4px;
        }
        
        .contract-card .tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 1px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
            background: #F8FAFE;
            border: 1px solid #E8F1F8;
            color: #0A2647;
        }
        
        .contract-card .tag-scanned {
            background: #EFF6FF;
            color: #3B82F6;
            border-color: #BFDBFE;
        }
        
        .contract-card .tag-demo {
            background: #E6F7F5;
            color: #0D9488;
            border-color: #A7F3D0;
        }
        
        .contract-card .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .contract-card .status-dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }
        
        .status-dot.healthy { background: #0D9488; }
        .status-dot.warning { background: #D97706; }
        .status-dot.critical { background: #DC2626; }
        .status-dot.scanned { background: #3B82F6; }
        
        .contract-card .risk-row {
            display: flex;
            gap: 14px;
            font-size: 12px;
            margin-top: 6px;
            flex-wrap: wrap;
        }
        
        .contract-card .risk-critical { color: #DC2626; }
        .contract-card .risk-high { color: #D97706; }
        .contract-card .risk-medium { color: #D97706; }
        .contract-card .risk-low { color: #3B82F6; }
        
        .contract-card .clause-preview {
            font-size: 12px;
            color: #94A3B8;
            margin-left: auto;
        }
        
        .contract-card .actions {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #F1F5F9;
        }
        
        /* ===== STAT CARDS ===== */
        .stat-card {
            background: white;
            border-radius: 14px;
            padding: 16px 20px;
            border: 1px solid #E8F1F8;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .stat-card:hover {
            border-color: #2C5F8A;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(10, 38, 71, 0.04);
        }
        
        .stat-card .value {
            font-size: 28px;
            font-weight: 700;
            color: #0A2647;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }
        
        .stat-card .label {
            font-size: 13px;
            font-weight: 500;
            color: #94A3B8;
            margin-top: 2px;
        }
        
        .stat-card .delta {
            font-size: 12px;
            font-weight: 500;
            margin-top: 4px;
            padding: 2px 12px;
            border-radius: 16px;
            display: inline-block;
        }
        
        /* ===== EMPTY STATE ===== */
        .empty-state {
            text-align: center;
            padding: 50px 20px;
            background: #F8FAFE;
            border-radius: 20px;
            border: 2px dashed #E2E8F0;
        }
        
        .empty-state .icon {
            font-size: 56px;
            display: block;
            margin-bottom: 10px;
        }
        
        .empty-state .title {
            font-size: 20px;
            font-weight: 600;
            color: #0A2647;
            margin: 0 0 4px 0;
        }
        
        .empty-state .desc {
            color: #94A3B8;
            font-size: 14px;
            margin: 0 0 16px 0;
        }
        
        /* ===== ANIMATION ===== */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeInUp 0.4s ease forwards;
        }
        
        /* ===== CLEAN STREAMLIT OVERRIDES ===== */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            font-size: 13px !important;
            padding: 4px 14px !important;
            height: auto !important;
            min-height: 34px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.08) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: #2C5F8A !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: #1B3A5C !important;
            box-shadow: 0 4px 16px rgba(44, 95, 138, 0.3) !important;
        }
        
        [data-testid="metric-container"] {
            background: white !important;
            border-radius: 14px !important;
            padding: 16px 20px !important;
            border: 1px solid #E8F1F8 !important;
        }
        
        [data-testid="metric-container"]:hover {
            border-color: #2C5F8A !important;
        }
        
        .stTextInput > div > div > input {
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
            padding: 8px 14px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #2C5F8A !important;
            box-shadow: 0 0 0 3px rgba(44, 95, 138, 0.08) !important;
        }
        
        .stSelectbox > div > div {
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
        }
        
        hr {
            margin: 12px 0 !important;
            border-color: #E8F1F8 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def _render_hero_section():
    """Render hero section"""
    
    total = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    total_risks = len(st.session_state.risks)
    
    st.markdown(f"""
    <div class="hero-card fade-in">
        <div class="glow1"></div>
        <div class="glow2"></div>
        <div class="content">
            <div>
                <div class="left">
                    <span class="icon">📄</span>
                    <div>
                        <div class="title">Contract Explorer</div>
                        <div class="subtitle">Manage and analyze your contract portfolio</div>
                    </div>
                </div>
                <div class="stats">
                    <div class="stat-item">
                        <span class="stat-value">{total}</span>
                        <span class="stat-label">Total</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{total_clauses}</span>
                        <span class="stat-label">Clauses</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{total_risks}</span>
                        <span class="stat-label">Risks</span>
                    </div>
                </div>
            </div>
            <div class="badges">
                <span class="badge">⚡ Batch Processing</span>
                <span class="badge">🔒 100% Private</span>
                <span class="badge">🤖 AI-Powered</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_instructions():
    """Render user instructions - Always visible for new users"""
    
    st.markdown("""
    <div class="instruction-card fade-in">
        <div class="header">
            <span class="icon">💡</span>
            <span class="title">How to Use This Page</span>
        </div>
        <div class="grid">
            <div class="item">
                <span class="emoji">🔍</span>
                <div>
                    <div class="text">Search & Filter</div>
                    <div class="desc">Find contracts by name, vendor, or type</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">👁️</span>
                <div>
                    <div class="text">View Details</div>
                    <div class="desc">Click "View" to see full contract details</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">📋</span>
                <div>
                    <div class="text">View Clauses</div>
                    <div class="desc">See all extracted clauses from a contract</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">⚠️</span>
                <div>
                    <div class="text">View Risks</div>
                    <div class="desc">Review risk indicators and severity levels</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">📊</span>
                <div>
                    <div class="text">Analyze</div>
                    <div class="desc">Get detailed analysis of contract risks</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">🗑️</span>
                <div>
                    <div class="text">Delete</div>
                    <div class="desc">Remove unwanted contracts from the list</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">📤</span>
                <div>
                    <div class="text">Upload</div>
                    <div class="desc">Add new contracts to your portfolio</div>
                </div>
            </div>
            <div class="item">
                <span class="emoji">📊</span>
                <div>
                    <div class="text">Export</div>
                    <div class="desc">Download contract data as CSV file</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_empty_state():
    """Render empty state"""
    st.markdown("""
    <div class="empty-state fade-in">
        <span class="icon">📭</span>
        <div class="title">No Contracts Yet</div>
        <div class="desc">Upload your first contract or explore with sample data</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Upload Contract", use_container_width=True, type="primary"):
            st.session_state.page = "Upload Contracts"
            st.rerun()
    with col2:
        if st.button("🎯 Load Demo Data", use_container_width=True):
            load_demo_contracts()
            st.rerun()


def _render_stats_row():
    """Render stats row"""
    
    contracts = st.session_state.contracts
    total = len(contracts)
    total_clauses = sum(c.clause_count for c in contracts)
    total_risks = sum(c.risk_count for c in contracts)
    
    healthy_count = sum(1 for c in contracts if c.overall_health == 'healthy')
    critical_risks = sum(1 for r in st.session_state.risks if r.severity == 'critical')
    avg_clauses = total_clauses / total if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card fade-in">
            <div class="value">{total}</div>
            <div class="label">Total Contracts</div>
            <div class="delta" style="background: #E8F1F8; color: #2C5F8A;">✅ {healthy_count} healthy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card fade-in">
            <div class="value">{total_clauses}</div>
            <div class="label">Total Clauses</div>
            <div class="delta" style="background: #E6F7F5; color: #0D9488;">Ø {avg_clauses:.1f} per contract</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card fade-in">
            <div class="value">{total_risks}</div>
            <div class="label">Total Risks</div>
            <div class="delta" style="background: #FEF3C7; color: #D97706;">Monitor all risks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card fade-in">
            <div class="value">{critical_risks}</div>
            <div class="label">Critical Risks</div>
            <div class="delta" style="background: #FEE2E2; color: #DC2626;">{'⚠️ Needs attention' if critical_risks > 0 else '✅ All clear'}</div>
        </div>
        """, unsafe_allow_html=True)


def _render_filters():
    """Render filters"""
    
    contracts = st.session_state.contracts
    
    st.markdown("### Search & Filter")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "Search",
            placeholder="Search by name, vendor, or content...",
            key="explorer_search",
            label_visibility="collapsed"
        )
    
    with col2:
        file_types = ["All"] + sorted(list(set(c.file_type.upper() for c in contracts)))
        file_type_filter = st.selectbox(
            "Type",
            options=file_types,
            key="explorer_file_type",
            label_visibility="collapsed"
        )
    
    with col3:
        sort_options = ["Latest", "Oldest", "A-Z", "Z-A", "Most Clauses", "Most Risks"]
        sort_by = st.selectbox(
            "Sort",
            options=sort_options,
            key="explorer_sort",
            label_visibility="collapsed"
        )
    
    # Apply filters
    filtered = contracts.copy()
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [
            c for c in filtered 
            if search_lower in c.name.lower() 
            or (c.vendor and search_lower in c.vendor.lower())
        ]
    
    if file_type_filter != "All":
        filtered = [c for c in filtered if c.file_type.upper() == file_type_filter]
    
    # Apply sorting
    sort_map = {
        "Latest": (lambda c: c.upload_date, True),
        "Oldest": (lambda c: c.upload_date, False),
        "A-Z": (lambda c: c.name.lower(), False),
        "Z-A": (lambda c: c.name.lower(), True),
        "Most Clauses": (lambda c: c.clause_count, True),
        "Most Risks": (lambda c: c.risk_count, True),
    }
    
    if sort_by in sort_map:
        key_func, reverse = sort_map[sort_by]
        filtered.sort(key=key_func, reverse=reverse)
    
    st.caption(f"Showing **{len(filtered)}** of **{len(contracts)}** contracts")
    
    return filtered


def _render_action_bar():
    """Render action bar"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📤 Upload", use_container_width=True, key="action_upload"):
            st.session_state.page = "Upload Contracts"
            st.rerun()
    
    with col2:
        if st.button("📊 Export CSV", use_container_width=True, key="action_export"):
            _export_contracts_data()
    
    with col3:
        if st.button("📋 All Clauses", use_container_width=True, key="action_clauses"):
            st.session_state.page = "Clause Library"
            st.rerun()
    
    with col4:
        if st.session_state.get('demo_mode', False):
            if st.button("🗑️ Clear Demo", use_container_width=True, key="action_demo"):
                clear_demo_data()
                st.rerun()


def _render_contracts_grid(contracts):
    """Render contracts grid"""
    
    st.markdown("### Contracts")
    
    for idx, contract in enumerate(contracts):
        _render_contract_item(contract, idx)


def _render_contract_item(contract: Contract, idx: int):
    """Render a single contract item - SIMPLIFIED to avoid rendering issues"""
    
    health = contract.overall_health
    health_color = {
        "healthy": "#0D9488",
        "warning": "#D97706",
        "critical": "#DC2626",
        "scanned": "#3B82F6"
    }.get(health, "#2C5F8A")
    
    health_label = health.title()
    file_icon = "📄" if contract.file_type == 'pdf' else "📝" if contract.file_type == 'docx' else "📃"
    risk_summary = contract.risk_severity_summary
    is_demo = is_demo_contract(contract.name)
    
    # Build meta string
    meta_parts = [
        f"📄 {contract.pages} pages",
        f"📊 {format_file_size(contract.file_size)}",
        f"📅 {contract.upload_date.strftime('%b %d, %Y')}"
    ]
    if contract.vendor:
        meta_parts.append(f"🏢 {contract.vendor}")
    if contract.contract_value:
        meta_parts.append(f"💰 ${contract.contract_value:,.0f}")
    meta_text = " • ".join(meta_parts)
    
    # Build tags
    tags_html = f'<span class="tag">{contract.file_type.upper()}</span>'
    if contract.is_scanned:
        tags_html += f'<span class="tag tag-scanned">📄 Scanned</span>'
    if is_demo:
        tags_html += f'<span class="tag tag-demo">🎯 Demo</span>'
    tags_html += f'<span class="status-badge" style="background: {health_color}12; color: {health_color};"><span class="status-dot {health}"></span> {health_label}</span>'
    tags_html += f'<span class="tag">📝 {contract.clause_count} clauses</span>'
    risk_color = "#D97706" if contract.risk_count > 0 else "#0D9488"
    risk_bg = "#FEF3C7" if contract.risk_count > 0 else "#E6F7F5"
    tags_html += f'<span class="tag" style="background: {risk_bg}; color: {risk_color};">⚠️ {contract.risk_count} risks</span>'
    
    # Build clause preview
    clause_preview = ""
    if contract.clause_types:
        clause_preview = ", ".join(contract.clause_types[:3])
        if len(contract.clause_types) > 3:
            clause_preview += "..."
    
    st.markdown(f"""
    <div class="contract-card fade-in">
        <div class="accent" style="background: {health_color};"></div>
        <div class="top-row">
            <div class="left-section">
                <span class="file-icon">{file_icon}</span>
                <div class="info">
                    <div class="contract-name">{contract.name}</div>
                    <div class="contract-meta">{meta_text}</div>
                    <div class="tags">{tags_html}</div>
                </div>
            </div>
        </div>
        <div class="risk-row">
            <span class="risk-critical">🔴 {risk_summary.get('critical', 0)} Critical</span>
            <span class="risk-high">🟠 {risk_summary.get('high', 0)} High</span>
            <span class="risk-medium">🟡 {risk_summary.get('medium', 0)} Medium</span>
            <span class="risk-low">🔵 {risk_summary.get('low', 0)} Low</span>
            <span class="clause-preview">📋 {clause_preview}</span>
        </div>
        <div class="actions">
    """, unsafe_allow_html=True)
    
    # Use Streamlit columns for action buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("👁️ View", key=f"view_{idx}", use_container_width=True):
            _show_contract_details(contract)
    
    with col2:
        if st.button("📋 Clauses", key=f"clauses_{idx}", use_container_width=True):
            st.session_state.page = "Clause Library"
            st.session_state.filter_contract = contract.id
            st.rerun()
    
    with col3:
        if st.button("⚠️ Risks", key=f"risks_{idx}", use_container_width=True):
            st.session_state.page = "RiskScan"
            st.session_state.filter_contract = contract.id
            st.rerun()
    
    with col4:
        if st.button("📊 Analyze", key=f"analyze_{idx}", use_container_width=True):
            _show_contract_analysis(contract)
    
    with col5:
        if st.button("🗑️", key=f"delete_{idx}", use_container_width=True):
            _delete_contract(contract.id)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)


def _show_contract_details(contract: Contract):
    """Show contract details"""
    with st.expander(f"📄 {contract.name} - Details", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("File Type", contract.file_type.upper())
            st.metric("Pages", contract.pages)
        
        with col2:
            st.metric("Size", format_file_size(contract.file_size))
            st.metric("Uploaded", contract.upload_date.strftime('%Y-%m-%d'))
        
        with col3:
            st.metric("Clauses", contract.clause_count)
            st.metric("Risks", contract.risk_count)
        
        with col4:
            st.metric("Health", contract.overall_health.title())
            st.metric("Words", f"{contract.word_count:,}")
        
        if contract.vendor:
            st.info(f"🏢 Vendor: {contract.vendor}")
        if contract.contract_value:
            st.success(f"💰 Contract Value: ${contract.contract_value:,.2f}")
        
        risk_summary = contract.risk_severity_summary
        st.caption(f"🔴 {risk_summary.get('critical', 0)} Critical • 🟠 {risk_summary.get('high', 0)} High • 🟡 {risk_summary.get('medium', 0)} Medium • 🔵 {risk_summary.get('low', 0)} Low")
        
        if contract.clauses:
            st.markdown("**📋 Extracted Clauses:**")
            clause_types = {}
            for clause in contract.clauses:
                clause_types[clause.type] = clause_types.get(clause.type, 0) + 1
            for ct, count in clause_types.items():
                st.markdown(f"- {ct}: {count}")


def _show_contract_analysis(contract: Contract):
    """Show contract analysis"""
    with st.expander(f"📊 {contract.name} - Analysis", expanded=True):
        
        st.markdown("### ⚠️ Risk Breakdown")
        if contract.risks:
            for risk in contract.risks[:10]:
                with st.container():
                    severity_color = get_risk_severity_color(risk.severity)
                    st.markdown(f"**{risk.type.replace('_', ' ').title()}** ({risk.severity.title()})")
                    st.caption(risk.description)
                    if risk.recommendation:
                        st.info(f"💡 {risk.recommendation}")
                    st.divider()
        else:
            st.success("✅ No risks found in this contract")
        
        st.markdown("### 📋 Clause Distribution")
        if contract.clauses:
            clause_counts = {}
            for clause in contract.clauses:
                clause_counts[clause.type] = clause_counts.get(clause.type, 0) + 1
            
            max_count = max(clause_counts.values()) if clause_counts else 1
            for ct, count in sorted(clause_counts.items(), key=lambda x: x[1], reverse=True):
                st.progress(count / max_count, text=f"{ct}: {count}")


def _delete_contract(contract_id: str):
    """Delete a contract"""
    contract = next((c for c in st.session_state.contracts if c.id == contract_id), None)
    if contract:
        st.session_state.contracts.remove(contract)
        st.session_state.clauses = [c for c in st.session_state.clauses if c.contract_id != contract_id]
        st.session_state.risks = [r for r in st.session_state.risks if r.contract_id != contract_id]
        st.success(f"✅ Deleted: {contract.name}")
        st.rerun()


def _export_contracts_data():
    """Export contract data"""
    if not st.session_state.contracts:
        st.warning("No contracts to export")
        return
    
    data = []
    for contract in st.session_state.contracts:
        data.append({
            "Contract Name": contract.name,
            "File Type": contract.file_type.upper(),
            "Pages": contract.pages,
            "Size (KB)": round(contract.file_size / 1024, 1),
            "Clauses": contract.clause_count,
            "Risks": contract.risk_count,
            "Critical Risks": contract.risk_severity_summary.get('critical', 0),
            "Health": contract.overall_health,
            "Upload Date": contract.upload_date.strftime('%Y-%m-%d'),
            "Vendor": contract.vendor or "",
            "Contract Value": contract.contract_value or ""
        })
    
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"contracts_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        key="export_csv_btn"
    )


def _render_analytics(contracts):
    """Render analytics section"""
    if len(contracts) < 2:
        return
    
    with st.expander("📊 Analytics", expanded=False):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Contract Health")
            health_counts = {'healthy': 0, 'warning': 0, 'critical': 0, 'scanned': 0}
            for c in contracts:
                health_counts[c.overall_health] = health_counts.get(c.overall_health, 0) + 1
            
            health_data = pd.DataFrame({
                'Status': list(health_counts.keys()),
                'Count': list(health_counts.values())
            })
            st.bar_chart(health_data.set_index('Status'), height=200)
        
        with col2:
            st.markdown("#### Clause Distribution")
            clause_counts = {}
            for c in contracts:
                for ct in c.clause_types:
                    clause_counts[ct] = clause_counts.get(ct, 0) + 1
            
            if clause_counts:
                clause_data = pd.DataFrame({
                    'Clause Type': list(clause_counts.keys()),
                    'Count': list(clause_counts.values())
                }).sort_values('Count', ascending=False)
                st.bar_chart(clause_data.set_index('Clause Type'), height=200)