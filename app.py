"""
KontractIQ - AI-Powered Contract Intelligence Platform
Main entry point for Streamlit Cloud deployment
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="KontractIQ",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import after page config
from app.components.layout import apply_custom_css
from app.utils.constants import COLORS

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'contracts' not in st.session_state:
        st.session_state.contracts = []
    if 'clauses' not in st.session_state:
        st.session_state.clauses = []
    if 'risks' not in st.session_state:
        st.session_state.risks = []
    if 'risk_rules' not in st.session_state:
        from app.utils.constants import DEFAULT_RISK_RULES
        st.session_state.risk_rules = DEFAULT_RISK_RULES.copy()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'upload_count' not in st.session_state:
        st.session_state.upload_count = 0
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"

# Apply custom CSS
apply_custom_css()

# Initialize session state
init_session_state()

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 48px;">⚖️</div>
            <div style="font-size: 24px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">KontractIQ</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">Intelligence for every clause.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        st.markdown("### 📁 CONTRACTS")
        pages = {
            "Dashboard": "🏠",
            "Upload Contracts": "📤",
            "Contract Explorer": "📄",
            "Clause Library": "📚"
        }
        
        for page_name, icon in pages.items():
            # Highlight current page
            is_active = st.session_state.page == page_name
            button_label = f"{icon} {page_name}"
            if is_active:
                button_label = f"▶️ {button_label}"
            
            if st.button(button_label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                st.rerun()
        
        st.divider()
        
        st.markdown("### 🔍 ANALYSIS")
        analysis_pages = {
            "Search": "🔎",
            "Compare": "📊",
            "CrossCheck": "🔄",
            "RiskScan": "⚠️"
        }
        
        for page_name, icon in analysis_pages.items():
            is_active = st.session_state.page == page_name
            button_label = f"{icon} {page_name}"
            if is_active:
                button_label = f"▶️ {button_label}"
            
            if st.button(button_label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                st.rerun()
        
        st.divider()
        
        st.markdown("### 📊 INSIGHTS")
        insight_pages = {
            "Vendor Consistency": "🏢",
            "Anomaly Detection": "🔍"
        }
        
        for page_name, icon in insight_pages.items():
            is_active = st.session_state.page == page_name
            button_label = f"{icon} {page_name}"
            if is_active:
                button_label = f"▶️ {button_label}"
            
            if st.button(button_label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                st.rerun()
        
        st.divider()
        
        st.markdown("### 🤖 AI FEATURES")
        ai_pages = {
            "AI Chat": "💬",
            "Create Contract": "📝"
        }
        
        for page_name, icon in ai_pages.items():
            is_active = st.session_state.page == page_name
            button_label = f"{icon} {page_name}"
            if is_active:
                button_label = f"▶️ {button_label}"
            
            if st.button(button_label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                st.rerun()
        
        st.divider()
        
        st.markdown("### 📄 OUTPUTS")
        output_pages = {
            "Reports": "📊",
            "System Metrics": "📈"
        }
        
        for page_name, icon in output_pages.items():
            is_active = st.session_state.page == page_name
            button_label = f"{icon} {page_name}"
            if is_active:
                button_label = f"▶️ {button_label}"
            
            if st.button(button_label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                st.rerun()
        
        st.divider()
        
        # Footer with contract count
        st.caption(f"📄 {len(st.session_state.contracts)} contracts loaded")
        st.caption(f"v1.0.0 | {datetime.now().strftime('%Y')}")
    
    # Main content - Page routing
    page = st.session_state.get('page', 'Dashboard')
    
    try:
        if page == "Dashboard":
            from app.pages.dashboard import render_dashboard
            render_dashboard()
        elif page == "Upload Contracts":
            from app.pages.upload import render_upload
            render_upload()
        elif page == "Contract Explorer":
            from app.pages.contract_explorer import render_contract_explorer
            render_contract_explorer()
        elif page == "Clause Library":
            from app.pages.clause_library import render_clause_library
            render_clause_library()
        elif page == "Search":
            from app.pages.search import render_search
            render_search()
        elif page == "Compare":
            from app.pages.compare import render_compare
            render_compare()
        elif page == "CrossCheck":
            from app.pages.crosscheck import render_crosscheck
            render_crosscheck()
        elif page == "RiskScan":
            from app.pages.riskscan import render_riskscan
            render_riskscan()
        elif page == "Vendor Consistency":
            from app.pages.vendor_consistency import render_vendor_consistency
            render_vendor_consistency()
        elif page == "Anomaly Detection":
            from app.pages.anomaly_detection import render_anomaly_detection
            render_anomaly_detection()
        elif page == "AI Chat":
            from app.pages.ask import render_ask
            render_ask()
        elif page == "Create Contract":
            from app.pages.create import render_create
            render_create()
        elif page == "Reports":
            from app.pages.reports import render_reports
            render_reports()
        elif page == "System Metrics":
            from app.pages.metrics import render_metrics
            render_metrics()
        else:
            st.info("👈 Select a page from the sidebar to get started")
    except ImportError as e:
        st.error(f"⚠️ Page not ready yet: {page}")
        st.info("This page is under construction. Please check back soon!")
        st.caption(f"Error: {str(e)}")

if __name__ == "__main__":
    main()