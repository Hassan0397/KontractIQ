"""
KontractIQ - Reusable Modal Components
"""

import streamlit as st
from ..utils.constants import COLORS, BORDER_RADIUS, SHADOWS, SPACING

def render_modal(title: str, content, on_close=None):
    """
    Render a modal dialog
    
    Args:
        title: Modal title
        content: Content to display (HTML string or streamlit elements)
        on_close: Callback when modal is closed
    """
    # Use a placeholder to create modal effect
    with st.container():
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        ">
            <div style="
                background-color: {COLORS['neutrals']['white']};
                border-radius: {BORDER_RADIUS['xxl']}px;
                padding: {SPACING['xxxl']}px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: {SHADOWS['xl']};
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: {SPACING['lg']}px;">
                    <h2 style="color: {COLORS['primary']['deepest_navy']}; margin: 0; font-size: 20px;">
                        {title}
                    </h2>
                    <button onclick="this.parentElement.parentElement.parentElement.style.display='none'" style="
                        background: none;
                        border: none;
                        font-size: 24px;
                        cursor: pointer;
                        color: {COLORS['neutrals']['medium_gray']};
                    ">✕</button>
                </div>
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_confirmation_modal(title: str, message: str, on_confirm=None, on_cancel=None):
    """
    Render a confirmation modal
    
    Args:
        title: Modal title
        message: Confirmation message
        on_confirm: Callback when confirmed
        on_cancel: Callback when cancelled
    """
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Cancel", key="modal_cancel", use_container_width=True):
            if on_cancel:
                on_cancel()
    
    with col2:
        if st.button("Confirm", key="modal_confirm", use_container_width=True, type="primary"):
            if on_confirm:
                on_confirm()


def render_success_modal(title: str, message: str, on_close=None):
    """
    Render a success modal
    
    Args:
        title: Modal title
        message: Success message
        on_close: Callback when closed
    """
    st.markdown(f"""
    <div style="
        background-color: {COLORS['semantic']['success_bg']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        border-left: 4px solid {COLORS['semantic']['success']};
        margin: {SPACING['md']}px 0;
    ">
        <div style="display: flex; align-items: center; gap: {SPACING['sm']}px;">
            <span style="font-size: 24px;">✅</span>
            <div>
                <div style="font-weight: 600; color: {COLORS['semantic']['success']};">
                    {title}
                </div>
                <div style="color: {COLORS['neutrals']['dark_gray']};">
                    {message}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Close", key="success_modal_close", use_container_width=True):
        if on_close:
            on_close()


def render_error_modal(title: str, message: str, on_close=None):
    """
    Render an error modal
    
    Args:
        title: Modal title
        message: Error message
        on_close: Callback when closed
    """
    st.markdown(f"""
    <div style="
        background-color: {COLORS['semantic']['danger_bg']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        border-left: 4px solid {COLORS['semantic']['danger']};
        margin: {SPACING['md']}px 0;
    ">
        <div style="display: flex; align-items: center; gap: {SPACING['sm']}px;">
            <span style="font-size: 24px;">❌</span>
            <div>
                <div style="font-weight: 600; color: {COLORS['semantic']['danger']};">
                    {title}
                </div>
                <div style="color: {COLORS['neutrals']['dark_gray']};">
                    {message}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Close", key="error_modal_close", use_container_width=True):
        if on_close:
            on_close()


def render_info_modal(title: str, message: str, on_close=None):
    """
    Render an info modal
    
    Args:
        title: Modal title
        message: Info message
        on_close: Callback when closed
    """
    st.markdown(f"""
    <div style="
        background-color: {COLORS['semantic']['info_bg']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        border-left: 4px solid {COLORS['semantic']['info']};
        margin: {SPACING['md']}px 0;
    ">
        <div style="display: flex; align-items: center; gap: {SPACING['sm']}px;">
            <span style="font-size: 24px;">ℹ️</span>
            <div>
                <div style="font-weight: 600; color: {COLORS['semantic']['info']};">
                    {title}
                </div>
                <div style="color: {COLORS['neutrals']['dark_gray']};">
                    {message}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("OK", key="info_modal_close", use_container_width=True):
        if on_close:
            on_close()