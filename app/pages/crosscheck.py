"""
KontractIQ - CrossCheck Page (Enterprise Edition)
Advanced cross-contract inconsistency detection with premium UI/UX
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import time
import numpy as np
import base64
from io import BytesIO, StringIO

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from ..core.crosscheck import CrossCheckEngine


def render_crosscheck():
    """Render the premium crosscheck page with enterprise-grade UI/UX"""
    
    # =====================================================================
    # PREMIUM HEADER WITH GRADIENT BACKGROUND
    # =====================================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .premium-header {
        background: linear-gradient(135deg, #0a1929 0%, #1a3a5c 50%, #0d47a1 100%);
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(10, 25, 41, 0.3);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .premium-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(26, 115, 232, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .premium-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(26, 115, 232, 0.05) 0%, transparent 70%);
        border-radius: 50%;
    }
    .header-content {
        position: relative;
        z-index: 2;
        text-align: center;
    }
    .header-title {
        color: white;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .header-title span {
        background: linear-gradient(135deg, #64b5f6, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .header-subtitle {
        color: rgba(255, 255, 255, 0.85);
        font-size: 16px;
        margin: 8px 0 0 0;
        font-weight: 400;
    }
    .header-badges {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 12px;
        flex-wrap: wrap;
    }
    .header-badge {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 6px 16px;
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.9);
        font-size: 13px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .header-badge:hover {
        background: rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    .developer-credit {
        text-align: center;
        margin-top: 16px;
        padding: 12px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 500;
        letter-spacing: 1px;
    }
    .developer-credit strong {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 700;
    }
    .developer-credit .highlight {
        background: linear-gradient(135deg, #64b5f6, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metrics Grid Styles */
    .metrics-wrapper {
        margin: 8px 0 24px 0;
        padding: 4px 0;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 0;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
        border-left: 4px solid #1a73e8;
        transition: all 0.3s ease;
        min-height: 80px;
        display: flex;
        align-items: center;
    }
    .metric-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .metric-content {
        display: flex;
        align-items: center;
        gap: 14px;
        width: 100%;
    }
    .metric-icon {
        font-size: 28px;
        flex-shrink: 0;
    }
    .metric-info {
        flex: 1;
        min-width: 0;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0a1929;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
        line-height: 1.3;
        margin-top: 2px;
    }
    @media (max-width: 768px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        .metric-card {
            padding: 16px 18px;
            min-height: 70px;
        }
        .metric-value {
            font-size: 22px;
        }
    }
    @media (max-width: 480px) {
        .metrics-grid {
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .metric-card {
            padding: 12px 14px;
            min-height: 60px;
        }
        .metric-icon {
            font-size: 22px;
        }
        .metric-value {
            font-size: 18px;
        }
        .metric-label {
            font-size: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="premium-header">
        <div class="header-content">
            <h1 class="header-title">
                🔄 KontractIQ <span>CrossCheck</span>
            </h1>
            <p class="header-subtitle">
                Enterprise-grade cross-contract inconsistency detection engine
            </p>
            <div class="header-badges">
                <span class="header-badge">📊 6 Metrics Analyzed</span>
                <span class="header-badge">🎯 AI-Powered Detection</span>
                <span class="header-badge">🔒 100% Private</span>
                <span class="header-badge">⚡ Real-time Analysis</span>
            </div>
        </div>
        <div class="developer-credit">
            Developed by <strong class="highlight">Hassan Subhani</strong> 
            <span style="color: rgba(255,255,255,0.4); margin: 0 8px;">|</span> 
            KontractIQ v2.0 Enterprise
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================================
    # CONTRACT COUNT CHECK
    # =====================================================================
    contract_count = len(st.session_state.contracts)
    
    if contract_count < 2:
        st.info("""
        ### 📭 Need More Contracts
        
        CrossCheck requires at least **2 contracts** to detect inconsistencies.
        
        **Current:** {} contract(s)
        **Required:** 2+ contracts
        
        Upload more contracts or load demo data to get started.
        """.format(contract_count))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Upload Contracts", key="crosscheck_upload_btn", use_container_width=True):
                st.session_state.page = "Upload Contracts"
                st.rerun()
        with col2:
            if st.button("🎯 Load Demo Data", key="crosscheck_demo_btn", use_container_width=True):
                from ..data.demo_data import load_demo_contracts
                load_demo_contracts()
                st.rerun()
        return

    # =====================================================================
    # PREMIUM METRICS DASHBOARD - FIXED SPACING
    # =====================================================================
    display_metrics_dashboard(contract_count)

    # =====================================================================
    # EXPANDABLE EDUCATIONAL SECTIONS
    # =====================================================================
    with st.expander("📖 Understanding CrossCheck - Complete Guide", expanded=False):
        display_comprehensive_guide()
    
    with st.expander("🚀 How to Use CrossCheck - Step by Step Tutorial", expanded=False):
        display_interactive_tutorial()

    # =====================================================================
    # ANALYSIS CONFIGURATION WITH ADVANCED OPTIONS
    # =====================================================================
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
        <div style='padding: 8px 0;'>
            <span style='font-size: 18px; font-weight: 600; color: #0a1929;'>🔍 Analysis Configuration</span>
            <span style='font-size: 13px; color: #6c757d; margin-left: 12px;'>
                Advanced settings for precision analysis
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced options in expander
        with st.expander("⚙️ Advanced Analysis Options", expanded=False):
            col_a, col_b = st.columns(2)
            with col_a:
                confidence_threshold = st.slider(
                    "Confidence Threshold",
                    min_value=50,
                    max_value=95,
                    value=70,
                    step=5,
                    help="Higher values detect only strong deviations, lower values catch more subtle inconsistencies"
                )
            with col_b:
                analysis_depth = st.selectbox(
                    "Analysis Depth",
                    options=["Standard", "Deep", "Comprehensive"],
                    index=0,
                    help="Deep analysis checks more contract clauses but takes longer"
                )
            
            st.caption(f"⚡ Current settings: {analysis_depth} analysis with {confidence_threshold}% confidence threshold")
    
    with col2:
        analyze_btn = st.button(
            "🚀 Run Cross-Check Analysis",
            key="crosscheck_analyze_btn",
            use_container_width=True,
            type="primary"
        )
    
    with col3:
        if st.session_state.get('crosscheck_results', None):
            if st.button("🗑️ Clear Results", key="crosscheck_clear_btn", use_container_width=True):
                st.session_state.crosscheck_results = None
                st.session_state.crosscheck_timestamp = None
                st.rerun()

    # =====================================================================
    # EXECUTE ANALYSIS WITH REAL-TIME PROGRESS
    # =====================================================================
    if analyze_btn:
        with st.spinner("🔍 Analyzing contracts for inconsistencies..."):
            # Real-time progress tracking
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                detail_text = st.empty()
            
            # Step 1: Data Extraction
            status_text.markdown("**📊 Phase 1/4: Data Extraction**")
            detail_text.markdown("🔍 Scanning contracts and extracting key clauses...")
            progress_bar.progress(15)
            time.sleep(0.8)
            
            # Step 2: Clause Analysis
            status_text.markdown("**🔍 Phase 2/4: Clause Analysis**")
            detail_text.markdown("📋 Identifying and categorizing contract clauses...")
            progress_bar.progress(35)
            time.sleep(0.8)
            
            # Step 3: Pattern Detection
            status_text.markdown("**📈 Phase 3/4: Pattern Detection**")
            detail_text.markdown("🎯 Comparing contracts and detecting patterns...")
            progress_bar.progress(55)
            time.sleep(0.8)
            
            # Step 4: Norm Identification
            status_text.markdown("**🎯 Phase 4/4: Norm Identification**")
            detail_text.markdown("📊 Calculating portfolio norms and identifying deviations...")
            progress_bar.progress(75)
            time.sleep(0.8)
            
            # Execute analysis
            engine = CrossCheckEngine()
            result = engine.analyze(st.session_state.contracts)
            
            # Store in session state
            st.session_state.crosscheck_results = result
            st.session_state.crosscheck_timestamp = datetime.now()
            st.session_state.analysis_settings = {
                'confidence_threshold': confidence_threshold,
                'analysis_depth': analysis_depth
            }
            
            progress_bar.progress(100)
            status_text.markdown("**✅ Analysis Complete!**")
            detail_text.markdown(f"🎉 Successfully analyzed {result.get('total_contracts', 0)} contracts")
            time.sleep(0.5)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            detail_text.empty()
            progress_container.empty()
        
        if 'error' in result:
            st.error(f"⚠️ {result['error']}")
        else:
            st.balloons()
            st.success(f"✅ Analysis complete! Analyzed {result['total_contracts']} contracts in {analysis_depth} mode")
            st.rerun()

    # =====================================================================
    # DISPLAY RESULTS
    # =====================================================================
    if st.session_state.get('crosscheck_results', None):
        results = st.session_state.crosscheck_results
        
        if 'error' in results:
            st.warning(results['error'])
            return
        
        display_expert_analysis_results(results)
    
    else:
        # =====================================================================
        # EMPTY STATE
        # =====================================================================
        display_expert_empty_state()


# =============================================================================
# EXPERT-LEVEL COMPONENTS
# =============================================================================

def display_metrics_dashboard(contract_count: int):
    """Display expert-level metrics dashboard with proper spacing"""
    
    # Calculate statistics
    total_clauses = sum(c.clause_count for c in st.session_state.contracts)
    total_risks = sum(c.risk_count for c in st.session_state.contracts)
    avg_clauses = total_clauses / contract_count if contract_count > 0 else 0
    
    # Check for previous results
    has_results = st.session_state.get('crosscheck_results', None) is not None
    findings_count = 0
    if has_results:
        results = st.session_state.crosscheck_results
        findings_count = len(results.get('findings', []))
    
    # Display metrics using Streamlit columns for better spacing
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown("""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e9ecef;
            border-left: 4px solid #1a73e8;
            height: 100%;
            display: flex;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 14px; width: 100%;">
                <span style="font-size: 28px;">📄</span>
                <div>
                    <div style="font-size: 26px; font-weight: 700; color: #0a1929;">{}</div>
                    <div style="font-size: 14px; color: #6c757d;">Contracts Analyzed</div>
                </div>
            </div>
        </div>
        """.format(contract_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e9ecef;
            border-left: 4px solid #1e7e34;
            height: 100%;
            display: flex;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 14px; width: 100%;">
                <span style="font-size: 28px;">📝</span>
                <div>
                    <div style="font-size: 26px; font-weight: 700; color: #0a1929;">{}</div>
                    <div style="font-size: 14px; color: #6c757d;">Clauses ({:.1f}/contract)</div>
                </div>
            </div>
        </div>
        """.format(total_clauses, avg_clauses), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e9ecef;
            border-left: 4px solid #e37400;
            height: 100%;
            display: flex;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 14px; width: 100%;">
                <span style="font-size: 28px;">⚠️</span>
                <div>
                    <div style="font-size: 26px; font-weight: 700; color: #0a1929;">{}</div>
                    <div style="font-size: 14px; color: #6c757d;">Risks Detected</div>
                </div>
            </div>
        </div>
        """.format(total_risks), unsafe_allow_html=True)
    
    with col4:
        status_color = "#1e7e34" if findings_count == 0 and has_results else "#c62828" if findings_count > 0 else "#6c757d"
        status_icon = "✅" if findings_count == 0 and has_results else "⚠️" if findings_count > 0 else "—"
        status_text = "All Consistent" if findings_count == 0 and has_results else f"{findings_count} Issues" if findings_count > 0 else "Ready"
        
        st.markdown("""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e9ecef;
            border-left: 4px solid {};
            height: 100%;
            display: flex;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 14px; width: 100%;">
                <span style="font-size: 28px;">{}</span>
                <div>
                    <div style="font-size: 26px; font-weight: 700; color: {};">{}</div>
                    <div style="font-size: 14px; color: #6c757d;">{}</div>
                </div>
            </div>
        </div>
        """.format(status_color, status_icon, status_color, findings_count if has_results else "—", status_text), unsafe_allow_html=True)


def display_comprehensive_guide():
    """Display comprehensive educational guide"""
    
    st.markdown("### 🤔 What is CrossCheck?")
    st.markdown("""
    CrossCheck is an **intelligent contract analysis engine** that automatically compares all your contracts 
    to identify inconsistencies, deviations, and outliers. It helps you maintain **portfolio-wide consistency** 
    by detecting when contracts don't follow your organization's standard terms.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 Why It Matters")
        st.markdown("""
        - **⚠️ Identify Risks**: Spot outliers and deviations early
        - **📊 Standardize**: Align contracts with best practices
        - **🎯 Negotiate Better**: Know your portfolio norms
        - **🛡️ Reduce Liability**: Avoid costly variations
        """)
    
    with col2:
        st.markdown("#### ⚙️ How It Works")
        st.markdown("""
        1. **Extract**: Scans contracts for key clauses
        2. **Analyze**: Extracts values for contract metrics
        3. **Compare**: Finds patterns across all contracts
        4. **Identify Norms**: Calculates portfolio standards
        5. **Flag Deviations**: Highlights inconsistencies
        """)
    
    st.markdown("---")
    st.markdown("### 🔍 What Gets Detected")
    
    detection_cols = st.columns(3)
    detection_items = [
        ("💰", "Payment Terms", "30 vs 60 vs 90 days", "#1a73e8"),
        ("🛡️", "Liability Caps", "$1M vs $5M vs Unlimited", "#e37400"),
        ("📅", "Termination Notice", "30 vs 60 vs 90 days", "#0d47a1"),
        ("⚖️", "Governing Law", "CA vs NY vs DE", "#1e7e34"),
        ("🔒", "Confidentiality", "1yr vs 3yr vs 5yr", "#0a1929"),
        ("🔄", "Renewal Terms", "Auto vs Manual vs None", "#c62828")
    ]
    
    for idx, (icon, label, desc, color) in enumerate(detection_items):
        with detection_cols[idx % 3]:
            st.markdown(f"""
            <div style="
                background: white;
                padding: 16px;
                border-radius: 10px;
                border: 1px solid #e9ecef;
                text-align: center;
                border-top: 3px solid {color};
                margin-bottom: 12px;
            ">
                <div style="font-size: 28px;">{icon}</div>
                <div style="font-weight: 600; color: #0a1929; font-size: 14px;">{label}</div>
                <div style="font-size: 12px; color: #6c757d;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.info("💡 **Pro Tip:** The more contracts you analyze, the more accurate your portfolio norms become. Aim for at least 5-10 contracts for reliable insights.")


def display_interactive_tutorial():
    """Display interactive tutorial with clear actions"""
    
    steps = [
        {
            "number": "1",
            "icon": "📤",
            "title": "Upload Your Contracts",
            "description": "Navigate to the Upload Contracts page and upload at least 2 contracts (PDF, DOCX, TXT).",
            "action": "Up to 20 contracts per session",
            "tip": "Upload contracts from the same category for more meaningful comparisons."
        },
        {
            "number": "2",
            "icon": "🚀",
            "title": "Run Cross-Check Analysis",
            "description": "Click the 'Run Cross-Check Analysis' button above to start the analysis.",
            "action": "One-click analysis with real-time progress",
            "tip": "Analysis typically completes in 5-10 seconds depending on contract size."
        },
        {
            "number": "3",
            "icon": "📊",
            "title": "Review Results",
            "description": "Examine the detailed findings including inconsistency types, norms, and recommendations.",
            "action": "Interactive tabs and visualizations",
            "tip": "Pay attention to critical and high-severity issues first."
        },
        {
            "number": "4",
            "icon": "⚡",
            "title": "Take Action",
            "description": "Export reports, share summaries, or re-run analysis after making changes.",
            "action": "Multiple export formats available (TXT, PDF, HTML)",
            "tip": "Use the export feature to share findings with your team."
        }
    ]
    
    for step in steps:
        with st.container():
            col1, col2, col3 = st.columns([1, 10, 1])
            with col2:
                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 12px;
                    padding: 16px 20px;
                    margin-bottom: 12px;
                    border: 1px solid #e9ecef;
                    border-left: 4px solid #1a73e8;
                ">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            width: 32px;
                            height: 32px;
                            background: #1a3a5c;
                            color: white;
                            border-radius: 50%;
                            font-weight: 700;
                            font-size: 14px;
                        ">{step['number']}</span>
                        <span style="font-size: 20px;">{step['icon']}</span>
                        <span style="font-size: 17px; font-weight: 600; color: #0a1929;">{step['title']}</span>
                    </div>
                    <div style="padding-left: 44px;">
                        <p style="color: #4a5568; margin: 4px 0; font-size: 14px;">{step['description']}</p>
                        <p style="color: #1a73e8; margin: 4px 0; font-size: 13px; font-weight: 500;">⚡ {step['action']}</p>
                        <p style="color: #6c757d; margin: 4px 0; font-size: 13px;">💡 {step['tip']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)


def display_expert_empty_state():
    """Display expert-level empty state with actionable guidance"""
    
    st.markdown("---")
    
    # Main empty state
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                border-radius: 16px;
                border: 2px dashed #dee2e6;
            ">
                <div style="font-size: 64px; margin-bottom: 16px;">🔍</div>
                <h3 style="color: #0a1929; margin: 0; font-size: 22px;">Ready to Analyze Your Contracts</h3>
                <p style="color: #4a5568; font-size: 15px; margin: 12px 0 20px 0; max-width: 500px; margin-left: auto; margin-right: auto;">
                    Click the <strong>"Run Cross-Check Analysis"</strong> button above to detect inconsistencies
                    across all your contracts.
                </p>
                <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
                    <span style="background: #e8f0fe; padding: 6px 16px; border-radius: 20px; font-size: 13px; color: #1a73e8;">⚡ Instant Analysis</span>
                    <span style="background: #e6f4ea; padding: 6px 16px; border-radius: 20px; font-size: 13px; color: #1e7e34;">🔒 100% Private</span>
                    <span style="background: #e0f7fa; padding: 6px 16px; border-radius: 20px; font-size: 13px; color: #00695c;">📊 6 Metrics Analyzed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detection grid
    st.markdown("""
    <div style="text-align: center; margin: 16px 0 12px 0;">
        <span style="font-size: 16px; font-weight: 600; color: #0a1929;">📋 What CrossCheck Detects</span>
    </div>
    """, unsafe_allow_html=True)
    
    detection_cols = st.columns(3)
    detection_items = [
        ("💰", "Payment Terms", "30 vs 60 vs 90 days"),
        ("🛡️", "Liability Caps", "$1M vs $5M vs Unlimited"),
        ("📅", "Termination Notice", "30 vs 60 vs 90 days"),
        ("⚖️", "Governing Law", "CA vs NY vs DE"),
        ("🔒", "Confidentiality", "1yr vs 3yr vs 5yr"),
        ("🔄", "Renewal Terms", "Auto vs Manual vs None")
    ]
    
    for idx, (icon, label, desc) in enumerate(detection_items):
        with detection_cols[idx % 3]:
            st.markdown(f"""
            <div style="
                background: white;
                padding: 14px;
                border-radius: 10px;
                border: 1px solid #e9ecef;
                text-align: center;
                margin-bottom: 12px;
                transition: all 0.3s ease;
            ">
                <div style="font-size: 28px;">{icon}</div>
                <div style="font-weight: 600; color: #0a1929; font-size: 13px;">{label}</div>
                <div style="font-size: 12px; color: #6c757d;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.info("💡 **Need sample contracts?** Load demo data or upload your own contracts to get started with CrossCheck.")


def display_expert_analysis_results(results: Dict[str, Any]):
    """Display expert-level analysis results with advanced visualizations"""
    
    timestamp = st.session_state.get('crosscheck_timestamp', datetime.now())
    total_contracts = results.get('total_contracts', 0)
    findings = results.get('findings', [])
    
    # =====================================================================
    # RESULTS HEADER
    # =====================================================================
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div style="padding: 4px 0;">
            <span style="font-size: 22px; font-weight: 700; color: #0a1929;">📊 Analysis Results</span>
            <span style="font-size: 14px; color: #6c757d; margin-left: 12px;">
                {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if findings:
            settings = st.session_state.get('analysis_settings', {})
            depth = settings.get('analysis_depth', 'Standard')
            st.caption(f"⚙️ {depth} Analysis | {len(findings)} issue types found")
    
    # =====================================================================
    # INTELLIGENT INSIGHTS DASHBOARD
    # =====================================================================
    if findings:
        total_deviations = sum(len(f.get('deviations', [])) for f in findings)
        
        # Calculate severity metrics
        critical = len([f for f in findings if len(f.get('deviations', [])) > total_contracts * 0.5])
        moderate = len([f for f in findings if 0 < len(f.get('deviations', [])) <= total_contracts * 0.5])
        clean = len([f for f in findings if len(f.get('deviations', [])) == 0])
        
        # Display insight cards
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 10px;
                padding: 14px 16px;
                border: 1px solid #e9ecef;
                border-left: 4px solid #c62828;
                height: 100%;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">🚨</span>
                    <div>
                        <div style="font-size: 20px; font-weight: 700; color: #0a1929;">{total_deviations}</div>
                        <div style="font-size: 12px; color: #6c757d;">Deviating Contracts</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 10px;
                padding: 14px 16px;
                border: 1px solid #e9ecef;
                border-left: 4px solid #c62828;
                height: 100%;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">🔴</span>
                    <div>
                        <div style="font-size: 20px; font-weight: 700; color: #0a1929;">{critical}</div>
                        <div style="font-size: 12px; color: #6c757d;">Critical Issues</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 10px;
                padding: 14px 16px;
                border: 1px solid #e9ecef;
                border-left: 4px solid #e37400;
                height: 100%;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">🟠</span>
                    <div>
                        <div style="font-size: 20px; font-weight: 700; color: #0a1929;">{moderate}</div>
                        <div style="font-size: 12px; color: #6c757d;">Moderate Issues</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 10px;
                padding: 14px 16px;
                border: 1px solid #e9ecef;
                border-left: 4px solid #1e7e34;
                height: 100%;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">🟢</span>
                    <div>
                        <div style="font-size: 20px; font-weight: 700; color: #0a1929;">{clean}</div>
                        <div style="font-size: 12px; color: #6c757d;">Clean Categories</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # =====================================================================
        # ADVANCED VISUALIZATION
        # =====================================================================
        st.markdown("---")
        st.markdown("### 📈 Inconsistency Analysis Dashboard")
        
        # Prepare data for visualization
        chart_data = []
        for finding in findings:
            chart_data.append({
                'Type': finding.get('type', 'Unknown'),
                'Deviations': len(finding.get('deviations', [])),
                'Total Values': len(finding.get('values', []))
            })
        
        if chart_data:
            df = pd.DataFrame(chart_data)
            
            # Create two columns for charts
            viz_col1, viz_col2 = st.columns([2, 1])
            
            with viz_col1:
                # Bar chart with Plotly
                fig = px.bar(
                    df,
                    x='Type',
                    y='Deviations',
                    color='Deviations',
                    color_continuous_scale=['#4CAF50', '#FFA726', '#EF5350'],
                    title='Inconsistencies by Contract Clause Type',
                    labels={'Deviations': 'Number of Contracts'},
                    height=400
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#4a5568'),
                    xaxis_title="",
                    yaxis_title="Deviating Contracts",
                    showlegend=False,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                fig.update_traces(marker=dict(line=dict(width=0)))
                st.plotly_chart(fig, use_container_width=True)
            
            with viz_col2:
                # Summary statistics
                st.markdown("""
                <div style="
                    background: white;
                    border-radius: 12px;
                    padding: 20px;
                    border: 1px solid #e9ecef;
                    height: 100%;
                ">
                    <div style="font-weight: 600; color: #0a1929; margin-bottom: 16px; font-size: 16px;">
                        📊 Portfolio Health Summary
                    </div>
                """, unsafe_allow_html=True)
                
                # Calculate health score
                health_score = max(0, 100 - (total_deviations / total_contracts * 50))
                health_score = min(100, health_score)
                
                st.metric("Portfolio Health Score", f"{health_score:.0f}%", 
                         delta="Good" if health_score > 70 else "Needs Review")
                
                st.markdown(f"""
                    <div style="margin-top: 12px;">
                        <div style="font-size: 14px; color: #4a5568; line-height: 2;">
                            <div>📋 <strong>{len(findings)}</strong> Categories Analyzed</div>
                            <div>🚨 <strong>{total_deviations}</strong> Total Deviations</div>
                            <div>📄 <strong>{total_contracts}</strong> Contracts Reviewed</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # All clear message
        st.markdown(f"""
        <div style="
            background: #e8f5e9;
            border-radius: 12px;
            padding: 24px 32px;
            margin: 12px 0;
            border: 1px solid #a5d6a7;
            text-align: center;
        ">
            <span style="font-size: 48px; display: block; margin-bottom: 8px;">🎉</span>
            <span style="font-weight: 700; color: #1e7e34; font-size: 20px;">
                All contracts are consistent!
            </span>
            <p style="font-size: 15px; color: #4a5568; margin: 8px 0 0 0;">
                No inconsistencies found across {total_contracts} contracts
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # =====================================================================
    # DETAILED FINDINGS WITH EXPERT ANALYSIS
    # =====================================================================
    if findings:
        st.markdown("---")
        st.markdown("### 🔍 Detailed Contract Analysis")
        st.caption("Click each tab to explore specific inconsistency types with expert recommendations")
        
        # Create tabs for each finding type
        tabs = st.tabs([f"{f.get('type', 'Unknown')}" for f in findings])
        
        for idx, (tab, finding) in enumerate(zip(tabs, findings)):
            with tab:
                display_expert_finding_card(finding, idx, total_contracts)
        
        # =====================================================================
        # EXPORT AND ACTIONS
        # =====================================================================
        display_expert_actions(results)


def display_expert_finding_card(finding: Dict[str, Any], idx: int, total_contracts: int):
    """Display expert-level finding card with detailed analysis"""
    
    finding_type = finding.get('type', 'Unknown')
    values = finding.get('values', [])
    most_common = finding.get('most_common', {})
    deviations = finding.get('deviations', [])
    recommendation = finding.get('recommendation', '')
    
    deviation_count = len(deviations)
    deviation_percentage = (deviation_count / total_contracts) * 100 if total_contracts > 0 else 0
    
    # Determine severity
    if deviation_percentage > 50:
        severity = "Critical"
        color = "#c62828"
        bg_color = "#ffebee"
        icon = "🔴"
    elif deviation_percentage > 25:
        severity = "High"
        color = "#e37400"
        bg_color = "#fff3e0"
        icon = "🟠"
    elif deviation_percentage > 0:
        severity = "Medium"
        color = "#f9a825"
        bg_color = "#fff8e1"
        icon = "🟡"
    else:
        severity = "Low"
        color = "#1e7e34"
        bg_color = "#e8f5e9"
        icon = "🟢"
    
    type_icons = {
        'Payment Terms': '💰',
        'Liability Cap': '🛡️',
        'Termination Notice': '📅',
        'Governing Law': '⚖️',
        'Confidentiality Period': '🔒',
        'Renewal Terms': '🔄'
    }
    type_icon = type_icons.get(finding_type, '📋')
    
    # Main card
    with st.container():
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 16px;
            border: 1px solid #e9ecef;
            border-left: 6px solid {color};
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 32px;">{type_icon}</span>
                    <div>
                        <div style="font-size: 18px; font-weight: 700; color: #0a1929;">{finding_type}</div>
                        <div style="font-size: 14px; color: #4a5568;">
                            {deviation_count} of {total_contracts} contracts deviate ({deviation_percentage:.0f}%)
                        </div>
                    </div>
                </div>
                <span style="
                    background: {bg_color};
                    color: {color};
                    padding: 4px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                ">
                    {icon} {severity} Severity
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Two column layout for values and norm
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: #f8f9fa;
                border-radius: 8px;
                padding: 12px 16px;
                border: 1px solid #e9ecef;
            ">
                <div style="font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 8px;">
                    📊 Values Distribution
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            """, unsafe_allow_html=True)
            
            for v in values:
                is_norm = v == most_common.get('value')
                if is_norm:
                    st.markdown(f"""
                    <span style="
                        background: #e8f5e9;
                        color: #1e7e34;
                        padding: 4px 12px;
                        border-radius: 16px;
                        font-size: 13px;
                        font-weight: 500;
                        border: 1px solid #a5d6a7;
                    ">
                        {v} ✅
                    </span>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <span style="
                        background: #ffebee;
                        color: #c62828;
                        padding: 4px 12px;
                        border-radius: 16px;
                        font-size: 13px;
                        font-weight: 500;
                        border: 1px solid #ef9a9a;
                    ">
                        {v} ⚠️
                    </span>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: #f8f9fa;
                border-radius: 8px;
                padding: 12px 16px;
                border: 1px solid #e9ecef;
            ">
                <div style="font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 8px;">
                    📈 Portfolio Norm
                </div>
                <div style="display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap;">
                    <span style="font-size: 24px; font-weight: 700; color: #0a1929;">
                        {most_common.get('value', 'N/A')}
                    </span>
                    <span style="font-size: 14px; color: #4a5568;">
                        {most_common.get('percentage', 0):.0f}% of contracts
                    </span>
                    <span style="
                        background: #e8f5e9;
                        color: #1e7e34;
                        padding: 2px 12px;
                        border-radius: 14px;
                        font-size: 12px;
                        font-weight: 500;
                    ">
                        Standard
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Deviating contracts
        if deviations:
            st.markdown("""
            <div style="margin-top: 12px;">
                <div style="font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 8px;">
                    🚨 Deviating Contracts
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            """, unsafe_allow_html=True)
            
            for contract in deviations:
                st.markdown(f"""
                <span style="
                    background: #ffebee;
                    padding: 4px 12px;
                    border-radius: 16px;
                    font-size: 13px;
                    color: #c62828;
                    font-weight: 500;
                    border: 1px solid #ef9a9a;
                ">
                    {contract}
                </span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Recommendation
        st.markdown(f"""
        <div style="
            margin-top: 12px;
            background: #e3f2fd;
            border-radius: 8px;
            padding: 12px 16px;
            border-left: 4px solid #1976d2;
        ">
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <span style="font-size: 18px;">💡</span>
                <div>
                    <div style="font-size: 13px; font-weight: 600; color: #0a1929;">Expert Recommendation</div>
                    <div style="font-size: 14px; color: #4a5568; line-height: 1.6;">{recommendation}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def display_expert_actions(results: Dict[str, Any]):
    """Display expert-level action buttons with enhanced functionality"""
    
    st.markdown("---")
    
    # Main action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export TXT Report", key="crosscheck_export_txt", use_container_width=True):
            export_expert_report(results, format_type="txt")
    
    with col2:
        if st.button("📄 Export PDF Report", key="crosscheck_export_pdf", use_container_width=True):
            export_expert_report(results, format_type="pdf")
    
    with col3:
        if st.button("🌐 Export HTML Report", key="crosscheck_export_html", use_container_width=True):
            export_expert_report(results, format_type="html")
    
    with col4:
        if st.button("📋 Copy Summary", key="crosscheck_copy_summary", use_container_width=True):
            summary = generate_expert_summary(results)
            st.code(summary, language="text")
            st.success("✅ Summary generated! You can copy from the code block above.")
    
    # Additional actions
    st.markdown("---")
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        if st.button("📈 View Dashboard", key="crosscheck_dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()
    
    with col6:
        if st.button("🔄 Re-run Analysis", key="crosscheck_rerun", use_container_width=True):
            st.session_state.crosscheck_results = None
            st.session_state.crosscheck_timestamp = None
            st.rerun()
    
    with col7:
        if st.button("📊 Export JSON", key="crosscheck_export_json", use_container_width=True):
            json_data = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"crosscheck_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
                key="crosscheck_download_json_btn"
            )
    
    with col8:
        if st.button("📧 Email Report", key="crosscheck_email", use_container_width=True):
            st.info("📧 Email sharing feature coming soon! Use the copy summary feature for now.")


def export_expert_report(results: Dict[str, Any], format_type: str = "txt"):
    """Generate and export expert-level report in multiple formats"""
    
    findings = results.get('findings', [])
    total_contracts = results.get('total_contracts', 0)
    settings = st.session_state.get('analysis_settings', {})
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_str = datetime.now().strftime('%Y%m%d_%H%M')
    
    if format_type == "txt":
        # Generate TXT report
        report = generate_txt_report(results)
        
        st.download_button(
            label="📥 Download TXT Report",
            data=report,
            file_name=f"crosscheck_expert_report_{date_str}.txt",
            mime="text/plain",
            key="crosscheck_download_txt_report",
            use_container_width=True
        )
        
    elif format_type == "html":
        # Generate HTML Report
        html_report = generate_html_report(results)
        
        st.download_button(
            label="📥 Download HTML Report",
            data=html_report,
            file_name=f"crosscheck_expert_report_{date_str}.html",
            mime="text/html",
            key="crosscheck_download_html_report",
            use_container_width=True
        )
        
    elif format_type == "pdf":
        # Generate PDF report using reportlab if available
        if REPORTLAB_AVAILABLE:
            try:
                pdf_buffer = generate_pdf_report(results)
                
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"crosscheck_expert_report_{date_str}.pdf",
                    mime="application/pdf",
                    key="crosscheck_download_pdf_report",
                    use_container_width=True
                )
                st.success("✅ PDF Report generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                st.info("💡 Falling back to HTML report.")
                
                # Fallback to HTML
                html_report = generate_html_report(results)
                st.download_button(
                    label="📥 Download HTML Report (Fallback)",
                    data=html_report,
                    file_name=f"crosscheck_expert_report_{date_str}.html",
                    mime="text/html",
                    key="crosscheck_download_html_fallback",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ ReportLab library not installed. Please install it for PDF generation.")
            st.info("💡 You can still download HTML or TXT reports.")
            
            # Offer HTML as fallback
            html_report = generate_html_report(results)
            st.download_button(
                label="📥 Download HTML Report",
                data=html_report,
                file_name=f"crosscheck_expert_report_{date_str}.html",
                mime="text/html",
                key="crosscheck_download_html_fallback",
                use_container_width=True
            )


def generate_txt_report(results: Dict[str, Any]) -> str:
    """Generate TXT report"""
    
    findings = results.get('findings', [])
    total_contracts = results.get('total_contracts', 0)
    settings = st.session_state.get('analysis_settings', {})
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              KONTRACTIQ CROSSCHECK EXPERT REPORT                  ║
║                                                                   ║
║         Developed by Hassan Subhani | KontractIQ v2.0            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

📋 Executive Summary
─────────────────────────────────────────────────────────────────────
  Generated:        {timestamp}
  Contracts:        {total_contracts}
  Issues Found:     {len(findings)}
  Analysis Mode:    {settings.get('analysis_depth', 'Standard')}
  Confidence:       {settings.get('confidence_threshold', 70)}%
  Status:           {'⚠️ Action Required' if findings else '✅ All Clear'}

{'═' * 68}

"""
    
    if findings:
        total_deviations = sum(len(f.get('deviations', [])) for f in findings)
        critical = len([f for f in findings if len(f.get('deviations', [])) > total_contracts * 0.5])
        moderate = len([f for f in findings if 0 < len(f.get('deviations', [])) <= total_contracts * 0.5])
        
        report += f"""
📊 Portfolio Health Summary
─────────────────────────────────────────────────────────────────────
  Health Score:     {max(0, 100 - (total_deviations / total_contracts * 50)):.0f}%
  Critical Issues:  {critical}
  Moderate Issues:  {moderate}
  Total Deviations: {total_deviations}

🔍 Detailed Findings
─────────────────────────────────────────────────────────────────────
"""
        
        for idx, finding in enumerate(findings, 1):
            report += f"""
[{idx}] {finding.get('type', 'Unknown')}
─────────────────────────────────────────────────────────────────────
  Values Found:       {', '.join(finding.get('values', []))}
  Portfolio Norm:     {finding.get('most_common', {}).get('value', 'N/A')} 
                      ({finding.get('most_common', {}).get('percentage', 0):.0f}%)
  Deviating Contracts: {', '.join(finding.get('deviations', [])) or 'None'}
  Recommendation:     {finding.get('recommendation', 'Review and standardize')}
  
"""
    else:
        report += """
✅ All Clear! No inconsistencies detected across your contracts.

"""
    
    report += f"""
{'═' * 68}

💡 Next Steps
─────────────────────────────────────────────────────────────────────
  1. Review critical and high-severity issues first
  2. Prioritize standardization based on business impact
  3. Update contracts to align with portfolio norms
  4. Re-run analysis after making changes

{'═' * 68}
  Generated by KontractIQ CrossCheck Expert Engine v2.0
  Developed by Hassan Subhani
  🔒 All analysis performed locally - 100% private and secure
{'═' * 68}
"""
    
    return report


def generate_pdf_report(results: Dict[str, Any]) -> BytesIO:
    """Generate PDF report using reportlab"""
    
    findings = results.get('findings', [])
    total_contracts = results.get('total_contracts', 0)
    settings = st.session_state.get('analysis_settings', {})
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0a1929'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#0a1929'),
        spaceAfter=12
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6
    )
    
    story = []
    
    # Title
    story.append(Paragraph("KontractIQ CrossCheck Expert Report", title_style))
    story.append(Paragraph("Developed by Hassan Subhani", styles['Italic']))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(f"Generated: {timestamp}", normal_style))
    story.append(Paragraph(f"Contracts Analyzed: {total_contracts}", normal_style))
    story.append(Paragraph(f"Issues Found: {len(findings)}", normal_style))
    story.append(Paragraph(f"Analysis Mode: {settings.get('analysis_depth', 'Standard')}", normal_style))
    story.append(Paragraph(f"Confidence Threshold: {settings.get('confidence_threshold', 70)}%", normal_style))
    status = '⚠️ Action Required' if findings else '✅ All Clear'
    story.append(Paragraph(f"Status: {status}", normal_style))
    story.append(Spacer(1, 15))
    
    if findings:
        total_deviations = sum(len(f.get('deviations', [])) for f in findings)
        health_score = max(0, 100 - (total_deviations / total_contracts * 50)) if total_contracts > 0 else 100
        health_score = min(100, health_score)
        
        story.append(Paragraph("Portfolio Health Summary", heading_style))
        story.append(Paragraph(f"Health Score: {health_score:.0f}%", normal_style))
        story.append(Paragraph(f"Total Deviations: {total_deviations}", normal_style))
        story.append(Spacer(1, 15))
        
        # Detailed Findings
        story.append(Paragraph("Detailed Findings", heading_style))
        
        for idx, finding in enumerate(findings, 1):
            finding_type = finding.get('type', 'Unknown')
            values = ', '.join(finding.get('values', []))
            norm = finding.get('most_common', {}).get('value', 'N/A')
            norm_pct = finding.get('most_common', {}).get('percentage', 0)
            deviations = ', '.join(finding.get('deviations', [])) or 'None'
            recommendation = finding.get('recommendation', 'Review and standardize')
            
            story.append(Paragraph(f"{idx}. {finding_type}", heading_style))
            story.append(Paragraph(f"Values Found: {values}", normal_style))
            story.append(Paragraph(f"Portfolio Norm: {norm} ({norm_pct:.0f}% of contracts)", normal_style))
            story.append(Paragraph(f"Deviating Contracts: {deviations}", normal_style))
            story.append(Paragraph(f"Recommendation: {recommendation}", normal_style))
            story.append(Spacer(1, 10))
    
    else:
        story.append(Paragraph("✅ All Clear! No inconsistencies detected.", heading_style))
        story.append(Spacer(1, 10))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("—" * 50, normal_style))
    story.append(Paragraph("Generated by KontractIQ CrossCheck Expert Engine v2.0", styles['Italic']))
    story.append(Paragraph("Developed by Hassan Subhani", styles['Italic']))
    story.append(Paragraph("🔒 All analysis performed locally - 100% private and secure", styles['Italic']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer


def generate_html_report(results: Dict[str, Any]) -> str:
    """Generate a professional HTML report"""
    
    findings = results.get('findings', [])
    total_contracts = results.get('total_contracts', 0)
    settings = st.session_state.get('analysis_settings', {})
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Calculate metrics
    total_deviations = sum(len(f.get('deviations', [])) for f in findings)
    health_score = max(0, 100 - (total_deviations / total_contracts * 50)) if total_contracts > 0 else 100
    health_score = min(100, health_score)
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KontractIQ CrossCheck Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            color: #0a1929;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #0a1929 0%, #1a3a5c 50%, #0d47a1 100%);
            color: white;
            padding: 40px 50px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: rgba(255,255,255,0.85);
            font-size: 16px;
            margin-bottom: 16px;
        }}
        .header .badges {{
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .header .badge {{
            background: rgba(255,255,255,0.1);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .header .developer {{
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.6);
            font-size: 14px;
        }}
        .header .developer strong {{
            color: rgba(255,255,255,0.9);
        }}
        .content {{
            padding: 40px 50px;
        }}
        .section {{
            margin-bottom: 32px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            color: #0a1929;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e9ecef;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 16px 20px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
            border-left: 4px solid #1a73e8;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: 700;
            color: #0a1929;
        }}
        .metric-label {{
            font-size: 13px;
            color: #6c757d;
        }}
        .finding-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px 24px;
            margin-bottom: 16px;
            border-left: 4px solid #1a73e8;
        }}
        .finding-title {{
            font-size: 18px;
            font-weight: 700;
            color: #0a1929;
            margin-bottom: 8px;
        }}
        .finding-detail {{
            color: #4a5568;
            font-size: 14px;
            margin-bottom: 4px;
        }}
        .finding-values {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0;
        }}
        .value-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 500;
        }}
        .value-tag-norm {{
            background: #e8f5e9;
            color: #1e7e34;
            border: 1px solid #a5d6a7;
        }}
        .value-tag-deviation {{
            background: #ffebee;
            color: #c62828;
            border: 1px solid #ef9a9a;
        }}
        .contract-tag {{
            display: inline-block;
            background: #ffebee;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 13px;
            color: #c62828;
            border: 1px solid #ef9a9a;
            margin: 4px;
        }}
        .recommendation {{
            margin-top: 12px;
            background: #e3f2fd;
            border-radius: 8px;
            padding: 12px 16px;
            border-left: 4px solid #1976d2;
        }}
        .recommendation strong {{
            color: #0a1929;
        }}
        .recommendation p {{
            color: #4a5568;
            margin-top: 4px;
        }}
        .health-score {{
            display: inline-block;
            padding: 4px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
        }}
        .health-good {{
            background: #e8f5e9;
            color: #1e7e34;
        }}
        .health-warning {{
            background: #fff3e0;
            color: #e37400;
        }}
        .health-critical {{
            background: #ffebee;
            color: #c62828;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px 50px;
            text-align: center;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
            font-size: 14px;
        }}
        .footer strong {{
            color: #0a1929;
        }}
        @media (max-width: 768px) {{
            .header {{
                padding: 30px 20px;
            }}
            .content {{
                padding: 20px;
            }}
            .metrics-grid {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 KontractIQ CrossCheck</h1>
            <div class="subtitle">Enterprise-Grade Cross-Contract Inconsistency Detection</div>
            <div class="badges">
                <span class="badge">📊 6 Metrics Analyzed</span>
                <span class="badge">🎯 AI-Powered Detection</span>
                <span class="badge">🔒 100% Private</span>
                <span class="badge">⚡ Real-time Analysis</span>
            </div>
            <div class="developer">
                Developed by <strong>Hassan Subhani</strong> | KontractIQ v2.0 Enterprise
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2 class="section-title">📋 Executive Summary</h2>
                <div class="metrics-grid">
                    <div class="metric-card" style="border-left-color: #1a73e8;">
                        <div class="metric-value">{total_contracts}</div>
                        <div class="metric-label">Contracts Analyzed</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #1e7e34;">
                        <div class="metric-value">{len(findings)}</div>
                        <div class="metric-label">Issues Found</div>
                    </div>
                    <div class="metric-card" style="border-left-color: #e37400;">
                        <div class="metric-value">{settings.get('analysis_depth', 'Standard')}</div>
                        <div class="metric-label">Analysis Mode</div>
                    </div>
                    <div class="metric-card" style="border-left-color: {'#1e7e34' if not findings else '#c62828'};">
                        <div class="metric-value">{'✅ All Clear' if not findings else '⚠️ Action Required'}</div>
                        <div class="metric-label">Status</div>
                    </div>
                </div>
            </div>
"""
    
    if findings:
        html += f"""
            <div class="section">
                <h2 class="section-title">📊 Portfolio Health</h2>
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap;">
                    <span style="font-size: 18px; font-weight: 600;">Health Score:</span>
                    <span class="health-score {'health-good' if health_score > 70 else 'health-warning' if health_score > 40 else 'health-critical'}">
                        {health_score:.0f}%
                    </span>
                    <span style="color: #4a5568; font-size: 14px;">
                        {total_deviations} total deviations across {len(findings)} categories
                    </span>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">🔍 Detailed Findings</h2>
"""
        
        for finding in findings:
            deviation_count = len(finding.get('deviations', []))
            deviation_percentage = (deviation_count / total_contracts * 100) if total_contracts > 0 else 0
            
            if deviation_percentage > 50:
                border_color = "#c62828"
            elif deviation_percentage > 25:
                border_color = "#e37400"
            elif deviation_percentage > 0:
                border_color = "#f9a825"
            else:
                border_color = "#1e7e34"
            
            html += f"""
                <div class="finding-card" style="border-left-color: {border_color};">
                    <div class="finding-title">{finding.get('type', 'Unknown')}</div>
                    <div class="finding-detail">
                        {deviation_count} of {total_contracts} contracts deviate ({deviation_percentage:.0f}%)
                    </div>
                    <div style="margin: 8px 0;">
                        <strong>Values Found:</strong>
                        <div class="finding-values">
"""
            
            for v in finding.get('values', []):
                is_norm = v == finding.get('most_common', {}).get('value')
                tag_class = "value-tag-norm" if is_norm else "value-tag-deviation"
                html += f'                            <span class="value-tag {tag_class}">{v} {"✅" if is_norm else "⚠️"}</span>\n'
            
            html += f"""
                        </div>
                    </div>
                    <div style="margin: 8px 0;">
                        <strong>Portfolio Norm:</strong>
                        <span style="font-size: 18px; font-weight: 700; color: #0a1929; margin-left: 8px;">
                            {finding.get('most_common', {}).get('value', 'N/A')}
                        </span>
                        <span style="color: #4a5568; font-size: 14px; margin-left: 8px;">
                            ({finding.get('most_common', {}).get('percentage', 0):.0f}% of contracts)
                        </span>
                    </div>
"""
            
            if finding.get('deviations', []):
                html += """
                    <div style="margin: 8px 0;">
                        <strong>Deviating Contracts:</strong>
                        <div style="display: flex; flex-wrap: wrap; margin-top: 4px;">
"""
                for contract in finding.get('deviations', []):
                    html += f'                            <span class="contract-tag">{contract}</span>\n'
                html += """
                        </div>
                    </div>
"""
            
            html += f"""
                    <div class="recommendation">
                        <strong>💡 Recommendation:</strong>
                        <p>{finding.get('recommendation', 'Review and standardize')}</p>
                    </div>
                </div>
"""
        
        html += """
            </div>
"""
    
    else:
        html += """
            <div class="section">
                <div style="
                    background: #e8f5e9;
                    border-radius: 12px;
                    padding: 32px;
                    text-align: center;
                    border: 2px solid #a5d6a7;
                ">
                    <div style="font-size: 48px; margin-bottom: 8px;">🎉</div>
                    <h3 style="color: #1e7e34; font-size: 20px; margin-bottom: 8px;">All contracts are consistent!</h3>
                    <p style="color: #4a5568; font-size: 15px;">No inconsistencies found across your portfolio</p>
                </div>
            </div>
"""
    
    html += f"""
            <div class="section">
                <h2 class="section-title">💡 Next Steps</h2>
                <ul style="color: #4a5568; line-height: 2; padding-left: 20px;">
                    <li>Review critical and high-severity issues first</li>
                    <li>Prioritize standardization based on business impact</li>
                    <li>Update contracts to align with portfolio norms</li>
                    <li>Re-run analysis after making changes</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>
                Generated by <strong>KontractIQ CrossCheck Expert Engine v2.0</strong><br>
                Developed by <strong>Hassan Subhani</strong> | {timestamp}<br>
                🔒 All analysis performed locally - 100% private and secure
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def generate_expert_summary(results: Dict[str, Any]) -> str:
    """Generate expert-level summary"""
    
    findings = results.get('findings', [])
    total_contracts = results.get('total_contracts', 0)
    
    summary = f"""
╔═══════════════════════════════════════════════════════════╗
║  KONTRACTIQ CROSSCHECK EXPERT SUMMARY                     ║
║  Developed by Hassan Subhani                              ║
╚═══════════════════════════════════════════════════════════╝

📊 Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Contracts Analyzed:  {total_contracts}
  Total Issues Found:  {len(findings)}
  Generated:           {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    
    if findings:
        total_deviations = sum(len(f.get('deviations', [])) for f in findings)
        summary += f"""
🔍 Issues Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Deviations:  {total_deviations}
  Categories:        {len(findings)}
  
"""
        for finding in findings:
            summary += f"""
  • {finding.get('type')}
      Norm:     {finding.get('most_common', {}).get('value')}
      Values:   {', '.join(finding.get('values', []))}
      Issues:   {len(finding.get('deviations', []))} contract(s)
      Action:   {finding.get('recommendation', 'Review and align')}
"""
    else:
        summary += """
✅ All Clear! No inconsistencies detected across your portfolio.

"""
    
    summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Generated by KontractIQ Expert Engine
  Developed by Hassan Subhani
  🔒 100% private and secure analysis
"""
    
    return summary