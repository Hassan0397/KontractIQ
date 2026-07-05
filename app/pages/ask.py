"""
KontractIQ - Ask Page
AI Contract Assistant with Groq API support
"""

import streamlit as st
import os
import time
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

CHAT_SETTINGS = {
    "max_context_contracts": 10,
    "max_context_chars": 3000,
    "max_history": 50,
    "temperature": 0.7,
    "max_tokens": 800,
    "model": "mixtral-8x7b-32768",
    "available_models": [
        "mixtral-8x7b-32768",
        "llama3-70b-8192",
        "gemma2-9b-it",
        "llama3-8b-8192"
    ]
}

# Color constants for styling
COLORS = {
    'primary': {
        'deepest_navy': '#0A2647',
        'rich_navy': '#1A3A5C',
        'corporate_blue': '#2C5F8A',
        'vibrant_blue': '#4A90D9',
        'ice_blue': '#E8F0FE',
        'pale_blue': '#B8D4E8'
    },
    'neutrals': {
        'white': '#FFFFFF',
        'off_white': '#F8FAFC',
        'light_gray': '#E2E8F0',
        'medium_gray': '#94A3B8',
        'dark_gray': '#475569'
    },
    'semantic': {
        'success': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
        'info': '#3B82F6',
        'success_bg': '#D1FAE5',
        'warning_bg': '#FEF3C7',
        'danger_bg': '#FEE2E2'
    }
}


# ============================================================================
# RENDER FUNCTION
# ============================================================================

def render_ask():
    """Render the AI chat page with premium UI"""
    
    # Hero Section
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
        padding: 24px 32px;
        border-radius: 20px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0;">💬 AI Contract Assistant</h1>
            <p style="color: rgba(255,255,255,0.8); margin: 4px 0 0 0; font-size: 14px;">
                Ask questions about your contracts and get intelligent answers powered by AI
            </p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span style="
                background: rgba(255,255,255,0.15);
                color: white;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">
                🧠 {CHAT_SETTINGS['model']}
            </span>
            <span style="
                background: rgba(255,255,255,0.10);
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
            ">
                {len(st.session_state.get('contracts', []))} contracts
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if there are contracts
    if not st.session_state.get('contracts', []):
        st.info("📭 No contracts uploaded yet. Upload contracts first to ask questions!")
        return
    
    # Show User Guide for first-time users
    if not st.session_state.get('chat_guide_dismissed', False):
        render_user_guide()
    
    # Premium Dashboard Metrics
    render_chat_metrics()
    
    # Main Chat Interface
    render_chat_interface()


# ============================================================================
# USER GUIDE - NEW USER TUTORIAL
# ============================================================================

def render_user_guide():
    """Render comprehensive user guide for new users"""
    
    # Use a container with a dismiss button instead of nested expander
    with st.container():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['primary']['ice_blue']}, {COLORS['neutrals']['white']});
            border-radius: 16px;
            padding: 24px;
            border: 1px solid {COLORS['primary']['pale_blue']};
            margin-bottom: 16px;
        ">
            <h3 style="color: {COLORS['primary']['deepest_navy']}; margin-top: 0;">🚀 Quick Start Guide</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 2px 8px rgba(10, 38, 71, 0.06);
                border-left: 4px solid #2C5F8A;
                margin-bottom: 12px;
            ">
                <div style="font-size: 24px;">🔑</div>
                <div style="font-weight: 600; color: #0A2647; margin: 8px 0 4px 0;">Step 1: Setup</div>
                <div style="font-size: 13px; color: #475569;">
                    • Click <strong>⚙️ Settings</strong> above<br>
                    • Enter your <strong>Groq API Key</strong> (optional)<br>
                    • Or use <strong>Fallback Mode</strong> without API
                </div>
            </div>
            
            <div style="
                background: white;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 2px 8px rgba(10, 38, 71, 0.06);
                border-left: 4px solid #F59E0B;
                margin-bottom: 12px;
            ">
                <div style="font-size: 24px;">📊</div>
                <div style="font-weight: 600; color: #0A2647; margin: 8px 0 4px 0;">Step 3: Get Insights</div>
                <div style="font-size: 13px; color: #475569;">
                    • <strong>AI Mode:</strong> Detailed contract analysis<br>
                    • <strong>Fallback Mode:</strong> Smart keyword search<br>
                    • Results include contract citations
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 2px 8px rgba(10, 38, 71, 0.06);
                border-left: 4px solid #10B981;
                margin-bottom: 12px;
            ">
                <div style="font-size: 24px;">💬</div>
                <div style="font-weight: 600; color: #0A2647; margin: 8px 0 4px 0;">Step 2: Ask Questions</div>
                <div style="font-size: 13px; color: #475569;">
                    • Type your question in the <strong>text area</strong><br>
                    • Click <strong>💬 Ask Question</strong><br>
                    • Or try <strong>💡 Ideas</strong> for suggestions
                </div>
            </div>
            
            <div style="
                background: white;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 2px 8px rgba(10, 38, 71, 0.06);
                border-left: 4px solid #4A90D9;
                margin-bottom: 12px;
            ">
                <div style="font-size: 24px;">🎯</div>
                <div style="font-weight: 600; color: #0A2647; margin: 8px 0 4px 0;">Step 4: Take Action</div>
                <div style="font-size: 13px; color: #475569;">
                    • Review risk recommendations<br>
                    • Export chat history<br>
                    • Clear and start fresh
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Pro Tip Section
        st.markdown(f"""
        <div style="
            background: {COLORS['primary']['deepest_navy']};
            color: white;
            border-radius: 12px;
            padding: 16px;
            margin: 12px 0;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 24px;">💡</span>
                <div>
                    <strong>Pro Tip:</strong> 
                    <span style="opacity: 0.9;">
                        Use specific questions like "What are the payment terms across all contracts?" 
                        or "Show me contracts with unlimited liability" for best results.
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Example questions - using a simple expand/collapse with button instead of nested expander
        if st.button("📚 Show Example Questions", key="toggle_examples", use_container_width=True):
            st.session_state.show_examples = not st.session_state.get('show_examples', False)
        
        if st.session_state.get('show_examples', False):
            st.markdown(f"""
            <div style="
                background: {COLORS['neutrals']['white']};
                border-radius: 12px;
                padding: 16px;
                margin: 12px 0;
                border: 1px solid {COLORS['neutrals']['light_gray']};
            ">
                <div style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin-bottom: 12px;">
                    📚 Example Questions You Can Ask
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            examples = [
                "• \"What are the payment terms across all contracts?\"",
                "• \"Show me contracts with unlimited liability\"",
                "• \"Which contracts have auto-renewal clauses?\"",
                "• \"Compare termination notice periods\"",
                "• \"What are the governing laws in my contracts?\"",
                "• \"Show me liability caps summary\"",
                "• \"Which contracts have confidentiality issues?\"",
                "• \"Summarize all indemnification clauses\"",
                "• \"What contracts have the highest risk?\"",
                "• \"Show me contract health scores summary\""
            ]
            with col1:
                for ex in examples[:5]:
                    st.markdown(f"<div style='font-size: 13px; color: #475569; margin: 4px 0;'>{ex}</div>", unsafe_allow_html=True)
            with col2:
                for ex in examples[5:]:
                    st.markdown(f"<div style='font-size: 13px; color: #475569; margin: 4px 0;'>{ex}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Dismiss button
        if st.button("✅ Got it! Let's start chatting", key="dismiss_guide", use_container_width=True):
            st.session_state.chat_guide_dismissed = True
            st.rerun()


# ============================================================================
# CHAT METRICS
# ============================================================================

def render_chat_metrics():
    """Render premium chat metrics cards"""
    
    # Calculate metrics
    contracts = st.session_state.get('contracts', [])
    total_contracts = len(contracts)
    chat_history = st.session_state.get('chat_history', [])
    total_questions = len([m for m in chat_history if m.get('role') == 'user'])
    has_api_key = 'groq_api_key' in st.session_state
    
    total_clauses = sum(getattr(c, 'clause_count', 0) for c in contracts)
    total_risks = sum(getattr(c, 'risk_count', 0) for c in contracts)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.08);
            border-left: 4px solid {COLORS['primary']['corporate_blue']};
            text-align: center;
        ">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{total_contracts}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">📄 Contracts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.08);
            border-left: 4px solid {COLORS['semantic']['success']};
            text-align: center;
        ">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{total_questions}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">💬 Questions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status_color = COLORS['semantic']['success'] if has_api_key else COLORS['semantic']['warning']
        status_text = "AI Active" if has_api_key else "Fallback"
        status_icon = "✅" if has_api_key else "⚡"
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.08);
            border-left: 4px solid {status_color};
            text-align: center;
        ">
            <div style="font-size: 22px; font-weight: 700; color: {status_color};">{status_icon} {status_text}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">🤖 AI Status</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.08);
            border-left: 4px solid {COLORS['primary']['vibrant_blue']};
            text-align: center;
        ">
            <div style="font-size: 28px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{total_clauses + total_risks}</div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">📊 Total Insights</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()


# ============================================================================
# CHAT INTERFACE
# ============================================================================

def render_chat_interface():
    """Render the main chat interface"""
    
    # Settings in expander
    with st.expander("⚙️ Settings & Configuration", expanded=False):
        render_settings()
    
    # Suggested Questions
    if st.session_state.get('show_suggestions', False):
        render_suggested_questions()
    
    # Chat History
    render_chat_history()
    
    # Add spacing before chat input
    st.markdown('<div style="margin-top: 32px;"></div>', unsafe_allow_html=True)
    
    # Chat Input
    render_chat_input()


# ============================================================================
# SETTINGS
# ============================================================================

def render_settings():
    """Render settings panel"""
    
    # API Key Section
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['off_white']};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    ">
        <h4 style="color: {COLORS['primary']['deepest_navy']}; margin: 0 0 12px 0;">🔑 API Configuration</h4>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        "Groq API Key (Optional)",
        type="password",
        placeholder="Enter your Groq API key for AI-powered answers",
        key="groq_api_key_settings",
        help="Get your free API key at console.groq.com"
    )
    
    if api_key:
        st.session_state.groq_api_key = api_key
        st.success("✅ API key set successfully!")
        st.rerun()
    elif 'groq_api_key' in st.session_state:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success("✅ API key is active")
        with col2:
            if st.button("🗑️ Remove", key="remove_api_key_settings", use_container_width=True):
                del st.session_state.groq_api_key
                st.rerun()
    else:
        st.info("ℹ️ Using fallback mode (keyword matching)")
        st.caption("Get your free API key at [console.groq.com](https://console.groq.com)")
    
    # Model Settings (only if API key is set)
    if 'groq_api_key' in st.session_state:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['off_white']};
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
        ">
            <h4 style="color: {COLORS['primary']['deepest_navy']}; margin: 0 0 12px 0;">🧠 Model Settings</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_model = st.selectbox(
                "Select Model",
                options=CHAT_SETTINGS['available_models'],
                index=CHAT_SETTINGS['available_models'].index(CHAT_SETTINGS['model']),
                key="chat_model_settings"
            )
            st.session_state.chat_model = selected_model
        
        with col2:
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=CHAT_SETTINGS['temperature'],
                step=0.1,
                key="chat_temperature_settings",
                help="Higher = more creative, Lower = more focused"
            )
            st.session_state.chat_temperature = temperature
    
    # Advanced Settings
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['off_white']};
        border-radius: 12px;
        padding: 16px;
    ">
        <h4 style="color: {COLORS['primary']['deepest_navy']}; margin: 0 0 12px 0;">🔧 Advanced</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_contracts = st.number_input(
            "Max Context Contracts",
            min_value=1,
            max_value=20,
            value=CHAT_SETTINGS['max_context_contracts'],
            key="max_context_contracts_settings",
            help="Number of contracts to include in AI context"
        )
        st.session_state.max_context_contracts = max_contracts
    
    with col2:
        max_chars = st.number_input(
            "Max Context Characters",
            min_value=500,
            max_value=10000,
            value=CHAT_SETTINGS['max_context_chars'],
            step=500,
            key="max_context_chars_settings",
            help="Maximum characters per contract for context"
        )
        st.session_state.max_context_chars = max_chars
    
    # Quick Actions
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Suggestions", key="show_suggestions_settings", use_container_width=True):
            st.session_state.show_suggestions = not st.session_state.get('show_suggestions', False)
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear History", key="clear_chat_settings", use_container_width=True):
            st.session_state.chat_history = []
            st.success("✅ Chat history cleared!")
            st.rerun()
    
    with col3:
        if st.button("📤 Export Chat", key="export_chat_settings", use_container_width=True):
            export_data = export_chat_history()
            st.download_button(
                label="📥 Download JSON",
                data=export_data,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="download_chat_export"
            )


# ============================================================================
# SUGGESTED QUESTIONS
# ============================================================================

def render_suggested_questions():
    """Render suggested questions as premium cards"""
    
    st.markdown(f"""
    <div style="
        background: {COLORS['primary']['ice_blue']};
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid {COLORS['primary']['pale_blue']};
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; font-size: 16px;">
                💡 Suggested Questions
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    suggestions = [
        "What are the payment terms across all contracts?",
        "Show me contracts with unlimited liability",
        "Which contracts have auto-renewal clauses?",
        "Compare termination notice periods",
        "What are the governing laws in my contracts?",
        "Show me liability caps summary",
        "Which contracts have confidentiality issues?",
        "Summarize all indemnification clauses",
        "What contracts have the highest risk?",
        "Show me contract health scores summary"
    ]
    
    # Display in 2 columns
    col1, col2 = st.columns(2)
    
    for i, suggestion in enumerate(suggestions):
        if i % 2 == 0:
            with col1:
                if st.button(
                    f"💡 {suggestion}",
                    key=f"suggestion_{i}",
                    use_container_width=True
                ):
                    st.session_state.chat_question = suggestion
                    st.rerun()
        else:
            with col2:
                if st.button(
                    f"💡 {suggestion}",
                    key=f"suggestion_{i}",
                    use_container_width=True
                ):
                    st.session_state.chat_question = suggestion
                    st.rerun()
    
    # Close button
    if st.button("✕ Close Suggestions", key="close_suggestions", use_container_width=True):
        st.session_state.show_suggestions = False
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# CHAT HISTORY
# ============================================================================

def render_chat_history():
    """Render chat history with premium message styling"""
    
    chat_history = st.session_state.get('chat_history', [])
    
    if not chat_history:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.08);
            margin-bottom: 16px;
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">💬</div>
            <div style="font-size: 18px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">No messages yet</div>
            <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">Ask a question about your contracts to get started</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display chat messages
    for idx, message in enumerate(chat_history):
        if message.get('role') == 'user':
            render_user_message(message.get('content', ''))
        else:
            render_assistant_message(message.get('content', ''), idx)
    
    # Add spacing after chat history
    st.markdown('<div style="margin-bottom: 16px;"></div>', unsafe_allow_html=True)


def render_user_message(content: str):
    """Render a user message with premium styling"""
    
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: flex-end;
        margin-bottom: 16px;
    ">
        <div style="
            max-width: 80%;
            background: linear-gradient(135deg, {COLORS['primary']['corporate_blue']}, {COLORS['primary']['vibrant_blue']});
            color: white;
            padding: 14px 20px;
            border-radius: 18px 18px 4px 18px;
            box-shadow: 0 2px 8px rgba(44, 95, 138, 0.2);
        ">
            <div style="font-size: 14px; line-height: 1.6;">{content}</div>
            <div style="font-size: 10px; opacity: 0.7; margin-top: 6px; text-align: right;">
                {datetime.now().strftime('%H:%M')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_assistant_message(content: str, idx: int):
    """Render an assistant message with premium styling"""
    
    # Check if content contains error or fallback
    is_error = "⚠️" in content or "Error" in content
    is_fallback = "fallback" in content.lower() or "keyword" in content.lower()
    
    border_color = COLORS['semantic']['danger'] if is_error else COLORS['primary']['corporate_blue']
    bg_color = COLORS['semantic']['danger_bg'] if is_error else COLORS['neutrals']['off_white']
    
    # Extract metadata if present
    thinking_time = ""
    token_info = ""
    
    # Simple extraction of metadata
    lines = content.split('\n')
    clean_content = []
    for line in lines:
        if '⏱️' in line:
            thinking_time = line.strip()
        elif 'tokens' in line.lower():
            token_info = line.strip()
        else:
            clean_content.append(line)
    
    content = '\n'.join(clean_content)
    
    # Build the HTML content with proper string concatenation
    html_content = f"""
    <div style="
        display: flex;
        justify-content: flex-start;
        margin-bottom: 16px;
    ">
        <div style="
            max-width: 85%;
            background: {bg_color};
            border: 1px solid {COLORS['neutrals']['light_gray']};
            padding: 14px 20px;
            border-radius: 18px 18px 18px 4px;
            box-shadow: 0 2px 8px rgba(10, 38, 71, 0.06);
            border-left: 4px solid {border_color};
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 8px;
                flex-wrap: wrap;
            ">
                <span style="font-size: 16px;">{'⚠️' if is_error else '🤖'}</span>
                <span style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; font-size: 13px;">
                    {'Error' if is_error else 'Assistant'}
                </span>"""
    
    if thinking_time:
        html_content += f'<span style="font-size: 10px; color: {COLORS["neutrals"]["medium_gray"]};">{thinking_time}</span>'
    
    if token_info:
        html_content += f'<span style="font-size: 10px; color: {COLORS["neutrals"]["medium_gray"]};">{token_info}</span>'
    
    if is_fallback and not is_error:
        html_content += f'<span style="font-size: 10px; background: {COLORS["semantic"]["warning_bg"]}; color: {COLORS["semantic"]["warning"]}; padding: 2px 10px; border-radius: 10px; font-weight: 500;">Fallback</span>'
    
    html_content += f"""
            </div>
            <div style="font-size: 14px; line-height: 1.7; color: {COLORS['neutrals']['dark_gray']};">{content}</div>
            <div style="font-size: 10px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 8px;">
                {datetime.now().strftime('%H:%M')}
            </div>
        </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)


# ============================================================================
# CHAT INPUT - NO WHITE CARD WITH PROPER SPACING
# ============================================================================

def render_chat_input():
    """Render premium chat input with no white card - just the text field"""
    
    # Get question from session or default
    default_question = st.session_state.get('chat_question', '')
    if 'chat_question' in st.session_state:
        del st.session_state.chat_question
    
    # Question input - no white card wrapper
    question = st.text_area(
        "Ask a question about your contracts",
        value=default_question,
        placeholder="e.g., What are the payment terms across all contracts?",
        key="chat_question_input",
        height=80,
        label_visibility="collapsed"
    )
    
    # Add spacing between text area and buttons
    st.markdown('<div style="margin-top: 12px;"></div>', unsafe_allow_html=True)
    
    # Buttons in a row
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    
    with col1:
        st.markdown(f"""
        <div style="
            font-size: 11px;
            color: {COLORS['neutrals']['medium_gray']};
            padding-top: 8px;
        ">
            ⏎ Press Ctrl+Enter to apply
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ask_btn = st.button(
            "💬 Ask Question",
            key="ask_btn_premium",
            use_container_width=True,
            type="primary"
        )
    
    with col3:
        clear_btn = st.button(
            "🗑️ Clear",
            key="clear_chat_btn_premium",
            use_container_width=True,
            help="Clear chat history"
        )
    
    with col4:
        suggestions_btn = st.button(
            "💡 Ideas",
            key="toggle_suggestions",
            use_container_width=True,
            help="Show suggested questions"
        )
    
    # Handle buttons
    if suggestions_btn:
        st.session_state.show_suggestions = not st.session_state.get('show_suggestions', False)
        st.rerun()
    
    if clear_btn:
        st.session_state.chat_history = []
        st.success("✅ Chat history cleared!")
        st.rerun()
    
    if ask_btn and question.strip():
        with st.spinner("🤖 Analyzing your question with AI..."):
            process_question(question)


# ============================================================================
# QUESTION PROCESSING
# ============================================================================

def process_question(question: str):
    """Process a question with premium features"""
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Add user question to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': question,
        'timestamp': datetime.now().isoformat()
    })
    
    # Process with AI or fallback
    start_time = time.time()
    
    if 'groq_api_key' in st.session_state:
        response = ask_groq_premium(question)
    else:
        response = fallback_search_premium(question)
    
    elapsed_time = time.time() - start_time
    
    # Add metadata to response
    token_count = len(response.split())
    response_with_meta = f"{response}\n\n⏱️ {elapsed_time:.2f}s • 📊 ~{token_count} tokens"
    
    # Add assistant response to history
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response_with_meta,
        'timestamp': datetime.now().isoformat()
    })
    
    st.rerun()


# ============================================================================
# PREMIUM GROQ API
# ============================================================================

def ask_groq_premium(question: str) -> str:
    """Premium Groq API integration with advanced features"""
    
    try:
        from groq import Groq
    except ImportError:
        return "⚠️ Groq library not installed. Install it with: `pip install groq`"
    
    try:
        # Get settings
        model = st.session_state.get('chat_model', CHAT_SETTINGS['model'])
        temperature = st.session_state.get('chat_temperature', CHAT_SETTINGS['temperature'])
        max_contracts = st.session_state.get('max_context_contracts', CHAT_SETTINGS['max_context_contracts'])
        max_chars = st.session_state.get('max_context_chars', CHAT_SETTINGS['max_context_chars'])
        
        # Initialize client
        client = Groq(api_key=st.session_state.groq_api_key)
        
        # Prepare context with premium contract selection
        context = prepare_premium_context(max_contracts, max_chars)
        
        # Get conversation history for context
        history_context = get_conversation_context()
        
        # Build detailed system prompt
        system_prompt = f"""You are a premium contract intelligence assistant for KontractIQ .

**Your Expertise:**
- Contract analysis and clause extraction
- Risk identification and assessment
- Cross-contract comparison and inconsistency detection
- Legal document summarization
- Compliance and regulatory analysis

**Available Contract Data:**
{context}

**Conversation Context:**
{history_context}

**User Question:**
{question}

**Response Requirements:**
1. Provide detailed, specific answers citing contract names
2. Include relevant clause text when applicable
3. Highlight risks, inconsistencies, and opportunities
4. Use structured format with clear sections
5. Include actionable recommendations
6. Be professional yet accessible
7. Quantify findings when possible

**Response Structure:**
📋 **Summary**
[Brief overview of the answer]

📊 **Key Findings**
[Bullet points of key findings with contract references]

⚠️ **Risks & Issues**
[Any risks or issues identified]

💡 **Recommendations**
[Actionable recommendations]

📄 **Contract Details**
[Specific contract references with clause details]

---
Provide a comprehensive, professional response that demonstrates deep contract analysis expertise."""
        
        # Get response
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {question}"}
            ],
            temperature=temperature,
            max_tokens=CHAT_SETTINGS['max_tokens'],
            top_p=0.9,
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg:
            return "⚠️ Invalid or expired API key. Please check your Groq API key."
        elif "rate" in error_msg.lower():
            return "⏳ Rate limit exceeded. Please wait a moment and try again."
        else:
            return f"⚠️ AI Error: {error_msg}\n\nFalling back to enhanced keyword search...\n\n{fallback_search_premium(question)}"


# ============================================================================
# PREMIUM CONTEXT PREPARATION
# ============================================================================

def prepare_premium_context(max_contracts: int = 10, max_chars: int = 3000) -> str:
    """Prepare premium context with smart contract selection"""
    
    contracts = st.session_state.get('contracts', [])
    
    # Smart contract selection with scoring
    scored_contracts = []
    for contract in contracts:
        score = 0
        # Health score bonus
        if hasattr(contract, 'health_score'):
            score += getattr(contract, 'health_score', 0) * 0.5
        # Clause count bonus
        score += getattr(contract, 'clause_count', 0) * 2
        # Risk count bonus (more risky contracts = more interesting)
        score += getattr(contract, 'risk_count', 0) * 1.5
        # Recency bonus
        upload_date = getattr(contract, 'upload_date', datetime.now())
        if hasattr(upload_date, 'days'):
            days_old = (datetime.now() - upload_date).days
        else:
            days_old = 0
        score += max(0, 30 - days_old)
        
        scored_contracts.append((score, contract))
    
    scored_contracts.sort(key=lambda x: x[0], reverse=True)
    selected_contracts = [c for _, c in scored_contracts[:max_contracts]]
    
    # Build detailed context
    context_parts = []
    for contract in selected_contracts:
        text = getattr(contract, 'searchable_text', getattr(contract, 'text', ''))[:max_chars]
        
        # Build comprehensive contract info
        health_label = getattr(contract, 'health_label', 'N/A')
        health_score = getattr(contract, 'health_score', 'N/A')
        
        # Clause presence summary
        clause_presence = getattr(contract, 'clause_presence_summary', {})
        clause_summary = "\n".join([f"    • {k}: {'✅' if v else '❌'}" for k, v in clause_presence.items()])
        
        # Risk summary
        risk_summary = getattr(contract, 'risk_severity_summary', {})
        risk_text = f"    • Critical: {risk_summary.get('critical', 0)}\n    • High: {risk_summary.get('high', 0)}\n    • Medium: {risk_summary.get('medium', 0)}\n    • Low: {risk_summary.get('low', 0)}"
        
        contract_info = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 **CONTRACT: {getattr(contract, 'name', 'Unknown')}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Metadata:**
• File Type: {getattr(contract, 'file_type', 'N/A').upper()}
• Pages: {getattr(contract, 'pages', 'N/A')}
• Clauses: {getattr(contract, 'clause_count', 0)}
• Risks: {getattr(contract, 'risk_count', 0)}
• Health: {health_label} (Score: {health_score})
• Upload Date: {getattr(contract, 'upload_date', datetime.now()).strftime('%Y-%m-%d') if hasattr(getattr(contract, 'upload_date', datetime.now()), 'strftime') else 'N/A'}
• Word Count: {getattr(contract, 'word_count', 'N/A')}
{f'• Vendor: {contract.vendor}' if hasattr(contract, 'vendor') and contract.vendor else ''}
{f'• Contract Value: ${contract.contract_value:,.2f}' if hasattr(contract, 'contract_value') and contract.contract_value else ''}

**Clause Coverage:**
{clause_summary}

**Risk Distribution:**
{risk_text}

**Contract Text:**
{text}
"""
        context_parts.append(contract_info)
    
    return "\n\n".join(context_parts)


def get_conversation_context() -> str:
    """Get recent conversation context"""
    chat_history = st.session_state.get('chat_history', [])
    if not chat_history:
        return "No previous conversation."
    
    recent = chat_history[-6:]
    context = []
    for msg in recent:
        role = "User" if msg.get('role') == 'user' else "Assistant"
        content = msg.get('content', '').split('\n\n⏱️')[0][:300]
        context.append(f"{role}: {content}")
    
    return "\n".join(context)


# ============================================================================
# ENHANCED FALLBACK SEARCH
# ============================================================================

def fallback_search_premium(question: str) -> str:
    """Enhanced fallback search with detailed results"""
    
    # Extract keywords
    keywords = extract_smart_keywords(question)
    
    if not keywords:
        return "Please ask a more specific question with keywords."
    
    # Search across contracts with detailed scoring
    results = []
    contract_matches = {}
    
    for contract in st.session_state.get('contracts', []):
        text = getattr(contract, 'text', '')
        text_lower = text.lower()
        matches = []
        
        for keyword in keywords:
            count = text_lower.count(keyword)
            if count > 0:
                matches.append((keyword, count))
        
        if matches:
            contract_matches[contract] = matches
            # Find best matching lines
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                for keyword, _ in matches:
                    if keyword in line_lower:
                        results.append({
                            'contract': contract,
                            'line': line.strip(),
                            'keyword': keyword,
                            'score': len(matches) * 10 + (100 - i) * 2
                        })
    
    if not results:
        return f"I couldn't find any matches for '{question}'. Try different keywords or enable AI with a Groq API key."
    
    # Sort and group results
    results.sort(key=lambda x: x['score'], reverse=True)
    results = results[:15]
    
    # Build detailed response
    response = "📋 **Enhanced Keyword Search Results**\n\n"
    
    # Add contract summary
    response += "📊 **Contracts with Matches:**\n"
    for contract, matches in contract_matches.items():
        match_summary = ", ".join([f"'{k}' ({c}x)" for k, c in matches])
        contract_name = getattr(contract, 'name', 'Unknown')
        response += f"  • {contract_name}: {match_summary}\n"
    
    response += "\n📄 **Detailed Matches:**\n\n"
    
    for result in results[:10]:
        # Get clause type if available
        clause_type = "Unknown"
        for clause in getattr(result['contract'], 'clauses', []):
            if result['keyword'].lower() in getattr(clause, 'text', '').lower():
                clause_type = getattr(clause, 'type', 'Unknown')
                break
        
        contract_name = getattr(result['contract'], 'name', 'Unknown')
        response += f"**{contract_name}**"
        if clause_type != "Unknown":
            response += f" [{clause_type}]"
        response += f"\n  • {result['line']}\n\n"
    
    response += "---\n💡 **Tip:** Enable AI with a Groq API key for more detailed, intelligent analysis!"
    
    return response


def extract_smart_keywords(question: str) -> List[str]:
    """Extract keywords with smart filtering"""
    
    # Clean and tokenize
    words = question.lower().split()
    
    # Remove common stopwords
    stopwords = {
        'what', 'are', 'the', 'is', 'a', 'an', 'of', 'for', 'on', 'at', 'to',
        'with', 'without', 'by', 'from', 'in', 'up', 'off', 'over', 'under',
        'above', 'below', 'across', 'through', 'between', 'among', 'within',
        'show', 'me', 'tell', 'which', 'where', 'when', 'why', 'how', 'about',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
        'such', 'than', 'that', 'then', 'these', 'they', 'this', 'those'
    }
    
    # Keep important terms
    keywords = []
    for word in words:
        word = ''.join(c for c in word if c.isalnum())
        if len(word) > 2 and word not in stopwords:
            keywords.append(word)
    
    # Add contract-specific terms
    contract_terms = {
        'payment': ['payment', 'pay', 'invoice', 'due', 'net', 'fee', 'cost', 'price'],
        'liability': ['liability', 'liable', 'cap', 'limit', 'damages', 'exposure'],
        'termination': ['terminate', 'termination', 'notice', 'cancel', 'end'],
        'confidentiality': ['confidential', 'nda', 'secret', 'proprietary', 'privacy'],
        'indemnification': ['indemnify', 'indemnification', 'hold harmless', 'defend'],
        'renewal': ['renew', 'renewal', 'auto-renew', 'automatic', 'extension'],
        'governing': ['governing', 'law', 'jurisdiction', 'forum', 'venue'],
        'risk': ['risk', 'exposure', 'liability', 'unlimited', 'uncapped']
    }
    
    question_lower = question.lower()
    for category, terms in contract_terms.items():
        if any(term in question_lower for term in terms):
            for term in terms[:2]:
                if term not in keywords:
                    keywords.append(term)
    
    # Remove duplicates
    seen = set()
    unique_keywords = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique_keywords.append(k)
    
    return unique_keywords[:10]


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_chat_history() -> str:
    """Export chat history as JSON"""
    chat_history = st.session_state.get('chat_history', [])
    if not chat_history:
        return json.dumps({"error": "No chat history available"}, indent=2)
    
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_messages": len(chat_history),
        "total_questions": len([m for m in chat_history if m.get('role') == 'user']),
        "total_responses": len([m for m in chat_history if m.get('role') == 'assistant']),
        "has_api_key": 'groq_api_key' in st.session_state,
        "messages": chat_history
    }
    
    return json.dumps(export_data, indent=2)