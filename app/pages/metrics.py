"""
KontractIQ - System Metrics Page
Monitor system performance and usage
"""

import streamlit as st
import psutil
import os
import sys
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from ..utils.constants import COLORS, LIMITS, CLAUSE_TYPES


def render_metrics():
    """Render the system metrics page"""

    # Hero Section
    render_hero_section()

    # Premium Metric Cards - Row 1
    render_metric_cards_row()

    st.markdown("---")

    # Second Row - Risk Distribution & Performance
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        render_risk_distribution_chart()
    with col2:
        render_performance_metrics()

    st.markdown("---")

    # Third Row - Contract Health Overview
    st.subheader("📊 Contract Health Overview")
    render_contract_health_cards()

    st.markdown("---")

    # Fourth Row - System Information & Session Actions
    col1, col2 = st.columns(2, gap="large")
    with col1:
        render_system_info_cards()
    with col2:
        render_session_actions()

    st.markdown("---")

    # Fifth Row - Contract Details Table
    render_contract_details_table()

    st.markdown("---")

    # Footer
    render_session_footer()


# ============================================================================
# HERO SECTION
# ============================================================================

def render_hero_section():
    """Render the hero section"""

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%); 
                padding: 28px 32px; 
                border-radius: 20px; 
                margin-bottom: 28px; 
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 4px 20px rgba(10,38,71,0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                    📈 System Metrics
                </div>
                <div style="color: rgba(255,255,255,0.75); font-size: 15px; margin: 6px 0 0 0; font-weight: 400;">
                    Monitor system performance, memory usage, and contract analytics
                </div>
            </div>
            <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center;">
                <div style="background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 10px;">
                    <span style="color: rgba(255,255,255,0.6); font-size: 13px;">⏱️ </span>
                    <span style="color: white; font-size: 13px; font-weight: 500;">{datetime.now().strftime('%H:%M:%S')}</span>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 10px;">
                    <span style="color: rgba(255,255,255,0.6); font-size: 13px;">📄 </span>
                    <span style="color: white; font-size: 13px; font-weight: 500;">{len(st.session_state.contracts)} contracts</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# METRIC CARDS ROW 
# ============================================================================

def render_metric_cards_row():
    """Render metric cards with premium design"""

    total_contracts = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    total_risks = len(st.session_state.risks)
    uploads = st.session_state.get('upload_count', 0)

    memory_mb = 0
    memory_limit = LIMITS.get('max_memory_mb', 1024)
    try:
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
    except:
        pass

    usage_percent = (memory_mb / memory_limit) * 100 if memory_limit > 0 else 0

    risk_breakdown = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for risk in st.session_state.risks:
        if risk.severity in risk_breakdown:
            risk_breakdown[risk.severity] += 1

    #  CSS with premium animations and glass-morphism touches
    st.markdown("""
    <style>
    .metric-card-wrapper {
        height: 130px;
        margin-bottom: 0px;
        padding: 0 4px;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 18px 20px;
        border: 1px solid rgba(226, 232, 240, 0.6);
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(10,38,71,0.06);
        transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(2px);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(145deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
        border-radius: 20px;
    }
    .metric-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 40px rgba(10,38,71,0.12), 0 2px 8px rgba(10,38,71,0.06);
        border-color: rgba(44, 95, 138, 0.2);
    }
    .metric-card .glow {
        position: absolute;
        top: -50%;
        right: -50%;
        width: 80%;
        height: 80%;
        border-radius: 50%;
        opacity: 0;
        transition: opacity 0.6s ease;
        pointer-events: none;
        filter: blur(60px);
    }
    .metric-card:hover .glow {
        opacity: 0.12;
    }
    .metric-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        position: relative;
        z-index: 1;
    }
    .metric-icon {
        font-size: 22px;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: rgba(248, 250, 254, 0.8);
        border: 1px solid rgba(226, 232, 240, 0.5);
        backdrop-filter: blur(4px);
    }
    .metric-number {
        font-size: 28px;
        font-weight: 700;
        color: #0A2647;
        line-height: 1.1;
        text-align: right;
        letter-spacing: -0.02em;
    }
    .metric-number .trend {
        font-size: 13px;
        font-weight: 500;
        margin-left: 6px;
        opacity: 0.7;
    }
    .metric-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    .metric-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 10px;
        margin-top: 4px;
        border-top: 1px solid rgba(241, 245, 249, 0.8);
        position: relative;
        z-index: 1;
    }
    .metric-badge {
        font-size: 11px;
        font-weight: 600;
        padding: 4px 14px;
        border-radius: 100px;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }
    .metric-badge:hover {
        transform: scale(1.04);
    }
    .metric-stat {
        font-size: 11px;
        color: #94a3b8;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .metric-stat .dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 4px;
    }
    .progress-container {
        width: 100%;
        height: 5px;
        background: rgba(226, 232, 240, 0.5);
        border-radius: 100px;
        overflow: hidden;
        margin-top: 4px;
    }
    .progress-bar {
        height: 100%;
        border-radius: 100px;
        transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
    }
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="small")

    # Card 1: Total Contracts
    with col1:
        st.markdown(f"""
        <div class="metric-card-wrapper">
            <div class="metric-card" style="border-top: 3px solid {COLORS['primary']['corporate_blue']};">
                <div class="glow" style="background: {COLORS['primary']['corporate_blue']};"></div>
                <div class="metric-top">
                    <div class="metric-icon">📄</div>
                    <div>
                        <div class="metric-number">{total_contracts}</div>
                        <div class="metric-label">Total Contracts</div>
                    </div>
                </div>
                <div class="metric-bottom">
                    <span class="metric-stat">Max {LIMITS['max_contracts']}</span>
                    <span class="metric-badge" style="color: {COLORS['primary']['corporate_blue']}; background: rgba(44,95,138,0.12);">+{uploads} uploaded</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Clauses Extracted
    with col2:
        avg_clauses = total_clauses / max(total_contracts, 1)
        st.markdown(f"""
        <div class="metric-card-wrapper">
            <div class="metric-card" style="border-top: 3px solid {COLORS['semantic']['success']};">
                <div class="glow" style="background: {COLORS['semantic']['success']};"></div>
                <div class="metric-top">
                    <div class="metric-icon">📝</div>
                    <div>
                        <div class="metric-number">{total_clauses}</div>
                        <div class="metric-label">Clauses Extracted</div>
                    </div>
                </div>
                <div class="metric-bottom">
                    <span class="metric-stat">{len(CLAUSE_TYPES)} types</span>
                    <span class="metric-badge" style="color: {COLORS['semantic']['success']}; background: rgba(13,148,136,0.12);">{avg_clauses:.1f} avg</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Total Risks
    with col3:
        risk_color = COLORS['semantic']['danger'] if total_risks > 0 else COLORS['semantic']['success']
        risk_bg = "rgba(220,38,38,0.10)" if total_risks > 0 else "rgba(13,148,136,0.10)"
        avg_risks = total_risks / max(total_contracts, 1)
        st.markdown(f"""
        <div class="metric-card-wrapper">
            <div class="metric-card" style="border-top: 3px solid {risk_color};">
                <div class="glow" style="background: {risk_color};"></div>
                <div class="metric-top">
                    <div class="metric-icon">⚠️</div>
                    <div>
                        <div class="metric-number">{total_risks}</div>
                        <div class="metric-label">Total Risks</div>
                    </div>
                </div>
                <div class="metric-bottom">
                    <span class="metric-stat">
                        <span class="dot" style="background:#DC2626;"></span>{risk_breakdown['critical']}
                        <span class="dot" style="background:#D97706;margin-left:6px;"></span>{risk_breakdown['high']}
                    </span>
                    <span class="metric-badge" style="color: {risk_color}; background: {risk_bg};">{avg_risks:.1f} avg</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Memory Usage
    with col4:
        memory_color = COLORS['semantic']['danger'] if usage_percent > 80 else COLORS['semantic']['warning'] if usage_percent > 60 else COLORS['semantic']['info']
        memory_bg = "rgba(220,38,38,0.10)" if usage_percent > 80 else "rgba(217,119,6,0.10)" if usage_percent > 60 else "rgba(59,130,246,0.10)"
        st.markdown(f"""
        <div class="metric-card-wrapper">
            <div class="metric-card" style="border-top: 3px solid {memory_color};">
                <div class="glow" style="background: {memory_color};"></div>
                <div class="metric-top">
                    <div class="metric-icon">🧠</div>
                    <div>
                        <div class="metric-number">{memory_mb:.0f} <span style="font-size:14px;font-weight:400;color:#94a3b8;">MB</span></div>
                        <div class="metric-label">Memory Usage</div>
                    </div>
                </div>
                <div class="metric-bottom" style="flex-direction: column; align-items: stretch; gap: 2px; padding-top: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="metric-stat">{memory_limit} MB limit</span>
                        <span class="metric-badge" style="color: {memory_color}; background: {memory_bg}; font-size:12px;">{usage_percent:.1f}%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {min(usage_percent, 100)}%; background: {memory_color};"></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# RISK DISTRIBUTION CHART
# ============================================================================

def render_risk_distribution_chart():
    """Render risk distribution chart with proper internal spacing"""

    risk_breakdown = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for risk in st.session_state.risks:
        if risk.severity in risk_breakdown:
            risk_breakdown[risk.severity] += 1

    st.markdown("""
    <style>
    .chart-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(10,38,71,0.06);
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        flex-shrink: 0;
    }
    .chart-title {
        font-size: 16px;
        font-weight: 600;
        color: #0A2647;
    }
    .chart-subtitle {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 2px;
    }
    .chart-total {
        font-size: 11px;
        color: #94A3B8;
        background: #F8FAFE;
        padding: 4px 14px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        font-weight: 500;
        flex-shrink: 0;
    }
    .chart-content {
        flex: 1;
        display: flex;
        align-items: center;
        min-height: 0;
        padding: 4px 0;
    }
    .empty-state {
        text-align: center;
        padding: 30px 20px;
        background: #F8FAFE;
        border-radius: 12px;
        border: 1px dashed #E2E8F0;
        width: 100%;
        margin: 4px 0;
    }
    .empty-icon {
        font-size: 44px;
    }
    .empty-title {
        font-size: 17px;
        font-weight: 600;
        margin-top: 10px;
        color: #0A2647;
    }
    .empty-subtitle {
        font-size: 13px;
        color: #94A3B8;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-header">
            <div>
                <div class="chart-title">⚠️ Risk Distribution</div>
                <div class="chart-subtitle">Breakdown by severity across all contracts</div>
            </div>
            <span class="chart-total">Total: {sum(risk_breakdown.values())}</span>
        </div>
        <div class="chart-content">
    """, unsafe_allow_html=True)

    if sum(risk_breakdown.values()) > 0:
        severity_order = ['critical', 'high', 'medium', 'low']
        labels = ['Critical', 'High', 'Medium', 'Low']
        values = [risk_breakdown.get(s, 0) for s in severity_order]
        colors = ['#DC2626', '#D97706', '#F59E0B', '#3B82F6']

        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Risks: %{y}<extra></extra>'
            )
        ])

        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#475569',
            margin=dict(l=10, r=10, t=10, b=25),
            height=200,
            xaxis=dict(
                gridcolor='#E2E8F0',
                gridwidth=1,
                showgrid=True,
                tickfont=dict(size=11),
                categoryorder='array',
                categoryarray=['Critical', 'High', 'Medium', 'Low']
            ),
            yaxis=dict(
                gridcolor='#E2E8F0',
                gridwidth=1,
                showgrid=True,
                tickfont=dict(size=10),
                zeroline=False
            )
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎉</div>
            <div class="empty-title">No risks detected</div>
            <div class="empty-subtitle">All contracts are risk-free!</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# ============================================================================
# PERFORMANCE METRICS - PERFECTLY ALIGNED
# ============================================================================

def render_performance_metrics():
    """Render performance metrics with perfect alignment"""

    total_contracts = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    total_risks = len(st.session_state.risks)

    clauses_per_contract = total_clauses / max(total_contracts, 1)
    risks_per_contract = total_risks / max(total_contracts, 1)

    total_words = sum(c.word_count for c in st.session_state.contracts)
    risk_density = (total_risks / max(total_words, 1)) * 1000 if total_words > 0 else 0

    st.markdown("""
    <style>
    .perf-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(10,38,71,0.06);
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    .perf-title {
        font-size: 16px;
        font-weight: 600;
        color: #0A2647;
        margin-bottom: 16px;
        flex-shrink: 0;
    }
    .perf-grid {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .perf-item {
        background: #F8FAFE;
        border-radius: 10px;
        padding: 12px 14px;
        border: 1px solid #E2E8F0;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        min-height: 70px;
    }
    .perf-value {
        font-size: 22px;
        font-weight: 700;
    }
    .perf-label {
        font-size: 12px;
        color: #475569;
        margin-top: 2px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="perf-card">
        <div class="perf-title">⚡ Performance Metrics</div>
        <div class="perf-grid">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1;">
                <div class="perf-item">
                    <div class="perf-value" style="color: #2C5F8A;">{clauses_per_contract:.1f}</div>
                    <div class="perf-label">Clauses / Contract</div>
                </div>
                <div class="perf-item">
                    <div class="perf-value" style="color: #D97706;">{risks_per_contract:.1f}</div>
                    <div class="perf-label">Risks / Contract</div>
                </div>
                <div class="perf-item">
                    <div class="perf-value" style="color: #3B82F6;">{risk_density:.2f}</div>
                    <div class="perf-label">Risk Density (per 1000 words)</div>
                </div>
                <div class="perf-item">
                    <div class="perf-value" style="color: #0D9488;">{total_words:,}</div>
                    <div class="perf-label">Total Words</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CONTRACT HEALTH CARDS - FIXED WITH STREAMLIT COLUMNS
# ============================================================================

def render_contract_health_cards():
    """Render contract health status cards with premium design using Streamlit columns"""

    if not st.session_state.contracts:
        st.info("📭 No contracts to analyze")
        return

    health_counts = {'healthy': 0, 'warning': 0, 'critical': 0, 'scanned': 0}
    for contract in st.session_state.contracts:
        status = contract.overall_health
        if status in health_counts:
            health_counts[status] += 1

    total = len(st.session_state.contracts)

    # Add CSS for health cards
    st.markdown("""
    <style>
    .health-card-item {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px 20px 20px 20px;
        border: 1px solid rgba(226, 232, 240, 0.6);
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(10,38,71,0.06);
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        height: 100%;
        min-height: 120px;
        width: 100%;
    }
    .health-card-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(10,38,71,0.12), 0 2px 8px rgba(10,38,71,0.06);
        border-color: rgba(44, 95, 138, 0.15);
    }
    .health-card-item .glow-effect {
        position: absolute;
        top: -30%;
        right: -30%;
        width: 60%;
        height: 60%;
        border-radius: 50%;
        opacity: 0;
        transition: opacity 0.5s ease;
        pointer-events: none;
        filter: blur(50px);
    }
    .health-card-item:hover .glow-effect {
        opacity: 0.10;
    }
    .health-card-top {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        position: relative;
        z-index: 1;
        margin-bottom: 6px;
    }
    .health-icon-box {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
        background: rgba(248, 250, 254, 0.9);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    .health-label-text {
        font-size: 14px;
        font-weight: 600;
        color: #0A2647;
        letter-spacing: -0.01em;
    }
    .health-stats-row {
        display: flex;
        align-items: baseline;
        gap: 10px;
        width: 100%;
        position: relative;
        z-index: 1;
        margin-top: 2px;
    }
    .health-number-large {
        font-size: 32px;
        font-weight: 700;
        color: #0A2647;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .health-percent-badge {
        font-size: 13px;
        font-weight: 500;
        color: #94A3B8;
        background: #F8FAFE;
        padding: 2px 12px;
        border-radius: 100px;
        border: 1px solid #E2E8F0;
        margin-left: 2px;
    }
    .health-divider-line {
        width: 30px;
        height: 3px;
        border-radius: 4px;
        margin-top: 6px;
        position: relative;
        z-index: 1;
    }
    /* Ensure proper spacing in columns */
    .health-col {
        padding: 0 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Define card configurations
    cards_config = [
        {
            'key': 'healthy',
            'icon': '✅',
            'label': 'Healthy',
            'color': '#0D9488',
            'bg': 'rgba(13,148,136,0.06)',
            'border_color': 'rgba(13,148,136,0.2)'
        },
        {
            'key': 'warning',
            'icon': '⚠️',
            'label': 'Needs Review',
            'color': '#D97706',
            'bg': 'rgba(217,119,6,0.06)',
            'border_color': 'rgba(217,119,6,0.2)'
        },
        {
            'key': 'critical',
            'icon': '🔴',
            'label': 'Critical Issues',
            'color': '#DC2626',
            'bg': 'rgba(220,38,38,0.06)',
            'border_color': 'rgba(220,38,38,0.2)'
        },
        {
            'key': 'scanned',
            'icon': '📄',
            'label': 'Scanned',
            'color': '#3B82F6',
            'bg': 'rgba(59,130,246,0.06)',
            'border_color': 'rgba(59,130,246,0.2)'
        }
    ]

    # Use Streamlit columns for proper layout
    cols = st.columns(4, gap="medium")

    for idx, card in enumerate(cards_config):
        with cols[idx]:
            count = health_counts.get(card['key'], 0)
            percentage = (count / max(total, 1)) * 100
            
            st.markdown(f'''
            <div class="health-card-item" style="border-left: 4px solid {card['color']}; background: {card['bg']};">
                <div class="glow-effect" style="background: {card['color']};"></div>
                <div class="health-card-top">
                    <div class="health-icon-box" style="border-color: {card['border_color']};">
                        {card['icon']}
                    </div>
                    <span class="health-label-text">{card['label']}</span>
                </div>
                <div class="health-stats-row">
                    <span class="health-number-large">{count}</span>
                    <span class="health-percent-badge">{percentage:.1f}%</span>
                </div>
                <div class="health-divider-line" style="background: {card['color']};"></div>
            </div>
            ''', unsafe_allow_html=True)


# ============================================================================
# SYSTEM INFO CARDS - PERFECTLY ALIGNED
# ============================================================================

def render_system_info_cards():
    """Render system information with perfect alignment"""

    try:
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent(interval=0.5)
        memory_limit = LIMITS.get('max_memory_mb', 1024)
        usage_percent = (memory_mb / memory_limit) * 100
    except:
        memory_mb = 0
        cpu_percent = 0
        usage_percent = 0

    memory_color = "#DC2626" if usage_percent > 80 else "#D97706" if usage_percent > 60 else "#0D9488"
    cpu_color = "#DC2626" if cpu_percent > 80 else "#D97706" if cpu_percent > 50 else "#0D9488"

    st.markdown("""
    <style>
    .sys-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(10,38,71,0.06);
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    .sys-title {
        font-size: 16px;
        font-weight: 600;
        color: #0A2647;
        margin-bottom: 16px;
        flex-shrink: 0;
    }
    .sys-grid {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .sys-item {
        background: #F8FAFE;
        border-radius: 10px;
        padding: 12px 14px;
        border: 1px solid #E2E8F0;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 70px;
    }
    .sys-label {
        font-size: 10px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .sys-value {
        font-size: 15px;
        font-weight: 600;
        color: #0A2647;
        margin-top: 2px;
    }
    .sys-progress-container {
        width: 100%;
        height: 4px;
        background: #E2E8F0;
        border-radius: 4px;
        margin-top: 6px;
        overflow: hidden;
    }
    .sys-progress-bar {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    .sys-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .sys-percent {
        font-size: 11px;
        font-weight: 500;
    }
    .sys-limit {
        font-size: 10px;
        color: #94A3B8;
        margin-top: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sys-card">
        <div class="sys-title">💻 System Information</div>
        <div class="sys-grid">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1;">
                <div class="sys-item">
                    <div class="sys-label">Python</div>
                    <div class="sys-value">{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}</div>
                </div>
                <div class="sys-item">
                    <div class="sys-label">Streamlit</div>
                    <div class="sys-value">{st.__version__}</div>
                </div>
                <div class="sys-item">
                    <div class="sys-label">Memory</div>
                    <div class="sys-meta">
                        <div class="sys-value">{memory_mb:.0f} MB</div>
                        <div class="sys-percent" style="color: {memory_color};">{usage_percent:.1f}%</div>
                    </div>
                    <div class="sys-progress-container">
                        <div class="sys-progress-bar" style="width: {min(usage_percent, 100)}%; background: {memory_color};"></div>
                    </div>
                    <div class="sys-limit">Limit: {memory_limit} MB</div>
                </div>
                <div class="sys-item">
                    <div class="sys-label">CPU</div>
                    <div class="sys-meta">
                        <div class="sys-value">{cpu_percent:.1f}%</div>
                        <div class="sys-percent" style="color: {cpu_color};">Usage</div>
                    </div>
                    <div class="sys-progress-container">
                        <div class="sys-progress-bar" style="width: {min(cpu_percent, 100)}%; background: {cpu_color};"></div>
                    </div>
                    <div class="sys-limit">Current process usage</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SESSION ACTIONS - FIXED: PROPER VERTICAL SPACING BETWEEN CONTENT AND BUTTONS
# ============================================================================

def render_session_actions():
    """Render session management actions with proper vertical spacing between content and buttons"""

    session_id = st.session_state.get('session_id', 'N/A')

    st.markdown("""
    <style>
    .session-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px 24px 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(10,38,71,0.06);
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    .session-title {
        font-size: 16px;
        font-weight: 600;
        color: #0A2647;
        margin-bottom: 16px;
        flex-shrink: 0;
    }
    .session-items {
        flex: 0 0 auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 32px !important;
    }
    .session-item {
        background: #F8FAFE;
        border-radius: 10px;
        padding: 12px 16px;
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 0 0 auto;
        min-height: 65px;
        transition: all 0.2s ease;
    }
    .session-item:hover {
        background: #F1F5F9;
        border-color: #CBD5E1;
    }
    .session-icon {
        font-size: 20px;
        flex-shrink: 0;
    }
    .session-content {
        flex: 1;
    }
    .session-item-title {
        font-size: 13px;
        font-weight: 500;
        color: #0A2647;
    }
    .session-item-desc {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 1px;
    }
    .session-id-badge {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #0A2647;
        font-weight: 600;
        background: #EFF6FF;
        padding: 2px 10px;
        border-radius: 6px;
        border: 1px solid #BFDBFE;
        display: inline-block;
    }
    .session-spacer {
        flex: 1;
        min-height: 16px;
    }
    .session-buttons-wrapper {
        flex-shrink: 0;
        padding-top: 24px !important;
        border-top: 1px solid #E2E8F0;
        margin-top: 0px;
    }
    .session-buttons-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
    }
    .real-button-gap {
        height: 22px;
        width: 100%;
    }
    .stButton {
        width: 100%;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 10px 16px;
        font-weight: 500;
        transition: all 0.2s ease;
        background-color: #F8FAFE;
        border: 1px solid #E2E8F0;
        color: #0A2647;
        margin-top: 6px;
    }
    .stButton > button:hover {
        background-color: #F1F5F9;
        border-color: #CBD5E1;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(10,38,71,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="session-card">
        <div class="session-title">🛠️ Session Management</div>
        <div class="session-items">
            <div class="session-item" style="background: #FEF2F2; border-color: #FECACA;">
                <span class="session-icon">🗑️</span>
                <div class="session-content">
                    <div class="session-item-title">Clear All Session Data</div>
                    <div class="session-item-desc">Remove all contracts, clauses, and risks</div>
                </div>
            </div>
            <div class="session-item" style="background: #EFF6FF; border-color: #BFDBFE;">
                <span class="session-icon">📊</span>
                <div class="session-content">
                    <div class="session-item-title">Export Session Data</div>
                    <div class="session-item-desc">Download all data as JSON backup</div>
                </div>
            </div>
            <div class="session-item">
                <span class="session-icon">🔑</span>
                <div class="session-content">
                    <div class="session-item-title">Session ID</div>
                    <div class="session-id-badge">{session_id}</div>
                </div>
            </div>
        </div>
        <div class="session-spacer"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="real-button-gap"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button("🗑️ Clear Session", key="clear_session_btn", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    with col2:
        if st.button("📊 Export Data", key="export_session_btn", use_container_width=True):
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "contract_count": len(st.session_state.contracts),
                "clause_count": len(st.session_state.clauses),
                "risk_count": len(st.session_state.risks),
                "contracts": [c.to_dict() for c in st.session_state.contracts]
            }
            import json
            json_data = json.dumps(export_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"session_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="download_session_btn",
                use_container_width=True
            )


# ============================================================================
# CONTRACT DETAILS TABLE
# ============================================================================

def render_contract_details_table():
    """Render contract details table"""

    st.markdown("""
    <div style="margin: 16px 0 12px 0;">
        <div style="font-size: 18px; font-weight: 600; color: #0A2647;">📋 Contract Details</div>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 2px;">View all uploaded contracts and their key metrics</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.contracts:
        contract_data = []
        for contract in st.session_state.contracts:
            health = contract.overall_health
            health_icon = {
                'healthy': '✅',
                'warning': '⚠️',
                'critical': '🔴',
                'scanned': '📄'
            }.get(health, '❓')

            risk_summary = contract.risk_severity_summary

            contract_data.append({
                "Status": health_icon,
                "Name": contract.name,
                "Type": contract.file_type.upper(),
                "Pages": contract.pages,
                "Clauses": contract.clause_count,
                "Risks": contract.risk_count,
                "Critical": risk_summary.get('critical', 0),
                "High": risk_summary.get('high', 0),
                "Size": f"{contract.file_size / 1024:.1f} KB",
                "Uploaded": contract.upload_date.strftime('%Y-%m-%d %H:%M')
            })

        df = pd.DataFrame(contract_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Name": st.column_config.TextColumn("Contract", width="medium"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Pages": st.column_config.NumberColumn("Pages", width="small"),
                "Clauses": st.column_config.NumberColumn("Clauses", width="small"),
                "Risks": st.column_config.NumberColumn("Total", width="small"),
                "Critical": st.column_config.NumberColumn("🔴", width="small", help="Critical Risks"),
                "High": st.column_config.NumberColumn("🟠", width="small", help="High Risks"),
                "Size": st.column_config.TextColumn("Size", width="small"),
                "Uploaded": st.column_config.TextColumn("Uploaded", width="small")
            }
        )
    else:
        st.info("📭 No contracts uploaded yet")


# ============================================================================
# SESSION FOOTER
# ============================================================================

def render_session_footer():
    """Render session footer"""

    if 'session_id' not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]

    session_start = st.session_state.get('session_start', datetime.now())
    duration = datetime.now() - session_start
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0 4px 0; border-top: 1px solid #E2E8F0; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 12px; color: #94A3B8;">🆔</span>
                <span style="font-size: 12px; font-weight: 600; color: #0A2647; background: #F1F5F9; padding: 2px 10px; border-radius: 6px; font-family: monospace;">{st.session_state.session_id}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 12px; color: #94A3B8;">⏱️</span>
                <span style="font-size: 12px; font-weight: 500; color: #0A2647;">{hours}h {minutes}m</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 12px; color: #94A3B8;">📄</span>
                <span style="font-size: 12px; font-weight: 500; color: #0A2647;">{len(st.session_state.contracts)} contracts</span>
            </div>
        </div>
        <span style="font-size: 11px; color: #94A3B8; font-weight: 400;">KontractIQ v1.0.0</span>
    </div>
    """, unsafe_allow_html=True)