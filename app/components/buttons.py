"""
KontractIQ - Reusable Button Components
"""

import streamlit as st
from ..utils.constants import COLORS, BORDER_RADIUS

def primary_button(label: str, key: str = None, disabled: bool = False):
    """Render a primary button with custom styling"""
    return st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=False,
    )

def secondary_button(label: str, key: str = None, disabled: bool = False):
    """Render a secondary button with custom styling"""
    return st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=False,
    )

def danger_button(label: str, key: str = None, disabled: bool = False):
    """Render a danger button"""
    return st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=False,
    )

def success_button(label: str, key: str = None, disabled: bool = False):
    """Render a success button"""
    return st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=False,
    )