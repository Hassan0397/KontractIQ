"""
KontractIQ - Reusable Layout Components
Optimized for performance and consistency
"""

import streamlit as st
from typing import Optional, Dict, Any  # <-- ADDED MISSING IMPORTS
from ..utils.constants import (
    COLORS, SPACING, SHADOWS, BORDER_RADIUS,
    TYPOGRAPHY, ANIMATIONS
)


def apply_custom_css() -> None:
    """Apply custom CSS for consistent styling - OPTIMIZED"""
    st.markdown(f"""
    <style>
        /* ========== RESET & BASE ========== */
        .stApp {{
            background-color: {COLORS['primary']['ice_blue']};
        }}
        
        .stApp > header {{
            background-color: {COLORS['neutrals']['white']} !important;
        }}
        
        .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
        }}
        
        /* ========== TYPOGRAPHY ========== */
        h1, h2, h3, h4, h5, h6 {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: {COLORS['primary']['deepest_navy']};
            letter-spacing: -0.02em;
        }}
        
        /* ========== CARD SYSTEM ========== */
        .kontract-card {{
            background-color: {COLORS['neutrals']['white']};
            border-radius: {BORDER_RADIUS['lg']}px;
            padding: {SPACING['lg']}px;
            box-shadow: {SHADOWS['md']};
            transition: all {ANIMATIONS['medium']};
            border: 1px solid {COLORS['neutrals']['light_gray']};
            height: 100%;
            position: relative;
            overflow: hidden;
        }}
        
        .kontract-card:hover {{
            box-shadow: {SHADOWS['hover']};
            transform: translateY(-2px);
        }}
        
        .kontract-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {COLORS['primary']['corporate_blue']}, {COLORS['primary']['vibrant_blue']});
            opacity: 0;
            transition: opacity {ANIMATIONS['medium']};
        }}
        
        .kontract-card:hover::before {{
            opacity: 1;
        }}
        
        /* ========== METRIC CARDS ========== */
        .metric-card {{
            background: {COLORS['neutrals']['white']};
            border-radius: {BORDER_RADIUS['xl']}px;
            padding: {SPACING['lg']}px {SPACING['lg']}px {SPACING['lg']}px {SPACING['lg']}px;
            box-shadow: {SHADOWS['sm']};
            border: 1px solid {COLORS['neutrals']['light_gray']};
            transition: all {ANIMATIONS['medium']};
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card:hover {{
            box-shadow: {SHADOWS['md']};
            transform: translateY(-3px);
        }}
        
        .metric-card .metric-icon {{
            font-size: 28px;
            margin-bottom: {SPACING['sm']}px;
            display: block;
        }}
        
        .metric-card .metric-value {{
            font-size: {TYPOGRAPHY['display']['size']}px;
            font-weight: {TYPOGRAPHY['display']['weight']};
            color: {COLORS['primary']['deepest_navy']};
            line-height: {TYPOGRAPHY['display']['line_height']};
        }}
        
        .metric-card .metric-label {{
            font-size: {TYPOGRAPHY['caption']['size']}px;
            color: {COLORS['neutrals']['dark_gray']};
            font-weight: {TYPOGRAPHY['caption']['weight']};
            margin-top: {SPACING['xs']}px;
        }}
        
        .metric-card .metric-indicator {{
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            border-radius: {BORDER_RADIUS['sm']}px 0 0 {BORDER_RADIUS['sm']}px;
        }}
        
        /* ========== HERO SECTION ========== */
        .hero-section {{
            background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
            padding: {SPACING['xxxl']}px {SPACING['xxl']}px;
            border-radius: {BORDER_RADIUS['xxl']}px;
            color: {COLORS['neutrals']['white']};
            margin-bottom: {SPACING['xxl']}px;
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section::after {{
            content: '⚖️';
            position: absolute;
            right: -30px;
            bottom: -30px;
            font-size: 120px;
            opacity: 0.05;
        }}
        
        .hero-section h1 {{
            color: {COLORS['neutrals']['white']};
            font-size: {TYPOGRAPHY['hero']['size']}px;
            font-weight: {TYPOGRAPHY['hero']['weight']};
            margin: 0;
            line-height: {TYPOGRAPHY['hero']['line_height']};
        }}
        
        .hero-section p {{
            color: rgba(255, 255, 255, 0.85);
            font-size: {TYPOGRAPHY['body_large']['size']}px;
            margin: {SPACING['sm']}px 0 0 0;
            opacity: 0.9;
        }}
        
        .hero-section .hero-subtitle {{
            font-size: {TYPOGRAPHY['body']['size']}px;
            opacity: 0.7;
            margin-top: {SPACING['xs']}px;
        }}
        
        /* ========== SECTION HEADERS ========== */
        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: {SPACING['lg']}px;
        }}
        
        .section-header h2 {{
            font-size: {TYPOGRAPHY['title_1']['size']}px;
            font-weight: {TYPOGRAPHY['title_1']['weight']};
            color: {COLORS['primary']['deepest_navy']};
            margin: 0;
        }}
        
        .section-header .section-badge {{
            background: {COLORS['primary']['ice_blue']};
            color: {COLORS['primary']['corporate_blue']};
            padding: {SPACING['xs']}px {SPACING['md']}px;
            border-radius: {BORDER_RADIUS['full']};
            font-size: {TYPOGRAPHY['micro']['size']}px;
            font-weight: {TYPOGRAPHY['micro']['weight']};
        }}
        
        /* ========== BUTTONS ========== */
        .stButton > button {{
            border-radius: {BORDER_RADIUS['md']}px !important;
            font-weight: 500 !important;
            transition: all {ANIMATIONS['medium']} !important;
            font-size: {TYPOGRAPHY['small']['size']}px !important;
            padding: {SPACING['sm']}px {SPACING['lg']}px !important;
            height: auto !important;
            min-height: 40px !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: {SHADOWS['hover']} !important;
        }}
        
        .stButton > button:active {{
            transform: translateY(0px) !important;
        }}
        
        /* Primary button override */
        .stButton > button[kind="primary"] {{
            background-color: {COLORS['primary']['corporate_blue']} !important;
            color: {COLORS['neutrals']['white']} !important;
        }}
        
        .stButton > button[kind="primary"]:hover {{
            background-color: {COLORS['primary']['vibrant_blue']} !important;
        }}
        
        /* ========== DIVIDERS ========== */
        hr {{
            border: none;
            border-top: 1px solid {COLORS['neutrals']['light_gray']};
            margin: {SPACING['lg']}px 0;
        }}
        
        /* ========== BADGES ========== */
        .risk-badge {{
            display: inline-block;
            padding: {SPACING['xs']}px {SPACING['md']}px;
            border-radius: {BORDER_RADIUS['full']};
            font-size: {TYPOGRAPHY['micro']['size']}px;
            font-weight: {TYPOGRAPHY['micro']['weight']};
            letter-spacing: 0.02em;
        }}
        
        /* ========== STATUS INDICATORS ========== */
        .status-dot {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: {SPACING['xs']}px;
        }}
        
        .status-dot.active {{
            background-color: {COLORS['semantic']['success']};
        }}
        
        .status-dot.inactive {{
            background-color: {COLORS['neutrals']['medium_gray']};
        }}
        
        /* ========== GRID HELPERS ========== */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: {SPACING['lg']}px;
        }}
        
        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: {SPACING['lg']}px;
        }}
        
        .grid-4 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: {SPACING['lg']}px;
        }}
        
        @media (max-width: 1024px) {{
            .grid-4 {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
        
        @media (max-width: 640px) {{
            .grid-2, .grid-3, .grid-4 {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* ========== TOOLTIP ========== */
        .tooltip {{
            position: relative;
            cursor: help;
        }}
        
        .tooltip:hover::after {{
            content: attr(data-tip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: {COLORS['primary']['deepest_navy']};
            color: {COLORS['neutrals']['white']};
            padding: {SPACING['xs']}px {SPACING['md']}px;
            border-radius: {BORDER_RADIUS['sm']}px;
            font-size: {TYPOGRAPHY['micro']['size']}px;
            white-space: nowrap;
            z-index: 1000;
        }}
        
        /* ========== SCROLLBAR ========== */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLORS['neutrals']['off_white']};
            border-radius: {BORDER_RADIUS['full']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['neutrals']['medium_gray']};
            border-radius: {BORDER_RADIUS['full']};
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['neutrals']['dark_gray']};
        }}
        
        /* ========== EXPANDER ========== */
        .streamlit-expanderHeader {{
            font-weight: 500 !important;
            color: {COLORS['primary']['deepest_navy']} !important;
            background-color: {COLORS['neutrals']['off_white']} !important;
            border-radius: {BORDER_RADIUS['md']}px !important;
        }}
        
        /* ========== DATA FRAME ========== */
        .stDataFrame {{
            border-radius: {BORDER_RADIUS['md']}px !important;
            overflow: hidden !important;
        }}
        
        /* ========== TEXT AREA ========== */
        .stTextArea textarea {{
            border-radius: {BORDER_RADIUS['md']}px !important;
            border-color: {COLORS['neutrals']['light_gray']} !important;
        }}
        
        .stTextArea textarea:focus {{
            border-color: {COLORS['primary']['corporate_blue']} !important;
            box-shadow: 0 0 0 3px rgba(44, 95, 138, 0.1) !important;
        }}
        
        /* ========== SELECT BOX ========== */
        .stSelectbox [data-baseweb="select"] {{
            border-radius: {BORDER_RADIUS['md']}px !important;
        }}
        
        /* ========== LOADING SPINNER ========== */
        .stSpinner > div {{
            border-color: {COLORS['primary']['corporate_blue']} !important;
        }}
        
        /* ========== INFO BOXES ========== */
        .stAlert {{
            border-radius: {BORDER_RADIUS['md']}px !important;
            padding: {SPACING['md']}px !important;
        }}
        
        /* ========== RESPONSIVE CONTAINER ========== */
        .responsive-container {{
            padding: {SPACING['lg']}px;
        }}
        
        @media (max-width: 768px) {{
            .responsive-container {{
                padding: {SPACING['sm']}px;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


def render_metric(
    label: str,
    value: str,
    icon: str = "",
    color: Optional[str] = None,
    subtitle: Optional[str] = None,
    trend: Optional[Dict[str, Any]] = None
) -> None:
    """
    Render a metric card with icon and optional trend
    
    Args:
        label: Metric label
        value: Metric value
        icon: Emoji or icon
        color: Border color
        subtitle: Optional subtitle
        trend: Optional trend data {'value': '12%', 'direction': 'up'|'down'}
    """
    if color is None:
        color = COLORS['primary']['corporate_blue']
    
    trend_html = ""
    if trend:
        trend_color = COLORS['semantic']['success'] if trend.get('direction') == 'up' else COLORS['semantic']['danger']
        trend_icon = "↑" if trend.get('direction') == 'up' else "↓"
        trend_html = f"""
            <div style="
                font-size: {TYPOGRAPHY['caption']['size']}px;
                color: {trend_color};
                margin-top: {SPACING['xs']}px;
                font-weight: 500;
            ">
                {trend_icon} {trend.get('value', '')}
            </div>
        """
    
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div style="
            font-size: {TYPOGRAPHY['micro']['size']}px;
            color: {COLORS['neutrals']['medium_gray']};
            margin-top: {SPACING['xs']}px;
        ">
            {subtitle}
        </div>
        """
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-indicator" style="background: {color};"></div>
        <div style="padding-left: {SPACING['md']}px;">
            <span class="metric-icon">{icon}</span>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            {trend_html}
            {subtitle_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_badge(severity: str) -> str:
    """
    Render a risk severity badge
    
    Args:
        severity: critical, high, medium, low
        
    Returns:
        HTML string for the badge
    """
    from ..utils.constants import RISK_SEVERITIES
    
    data = RISK_SEVERITIES.get(severity, {})
    color = data.get('color', COLORS['neutrals']['dark_gray'])
    bg = data.get('bg', COLORS['neutrals']['off_white'])
    label = data.get('label', severity.capitalize())
    
    return f"""
    <span class="risk-badge" style="
        background-color: {bg};
        color: {color};
        border: 1px solid {color}33;
    ">
        {label}
    </span>
    """


def render_card(
    content: str,
    title: Optional[str] = None,
    icon: Optional[str] = None,
    variant: str = "default"
) -> None:
    """
    Render a card with content
    
    Args:
        content: Content HTML
        title: Optional card title
        icon: Optional icon for title
        variant: default, success, warning, danger, info
    """
    variant_colors = {
        "default": {"border": COLORS['neutrals']['light_gray']},
        "success": {"border": COLORS['semantic']['success']},
        "warning": {"border": COLORS['semantic']['warning']},
        "danger": {"border": COLORS['semantic']['danger']},
        "info": {"border": COLORS['semantic']['info']}
    }
    
    border_color = variant_colors.get(variant, variant_colors["default"])["border"]
    
    title_html = ""
    if title:
        title_html = f"""
            <div style="
                display: flex;
                align-items: center;
                gap: {SPACING['sm']}px;
                margin-bottom: {SPACING['md']}px;
                font-size: {TYPOGRAPHY['title_2']['size']}px;
                font-weight: {TYPOGRAPHY['title_2']['weight']};
                color: {COLORS['primary']['deepest_navy']};
            ">
                {f'<span>{icon}</span>' if icon else ''}
                <span>{title}</span>
            </div>
        """
    
    st.markdown(f"""
    <div class="kontract-card" style="border-left: 4px solid {border_color};">
        {title_html}
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(
    title: str,
    subtitle: str,
    description: Optional[str] = None
) -> None:
    """
    Render a hero section
    
    Args:
        title: Hero title
        subtitle: Hero subtitle
        description: Optional description
    """
    desc_html = ""
    if description:
        desc_html = f"""
        <div class="hero-subtitle">{description}</div>
        """
    
    st.markdown(f"""
    <div class="hero-section">
        <h1>{title}</h1>
        <p>{subtitle}</p>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(
    title: str,
    badge: Optional[str] = None,
    action_label: Optional[str] = None,
    action_key: Optional[str] = None
) -> None:
    """
    Render a section header with optional badge and action button
    
    Args:
        title: Section title
        badge: Optional badge text
        action_label: Optional action button label
        action_key: Optional action button key
    """
    badge_html = ""
    if badge:
        badge_html = f"""
        <span class="section-badge">{badge}</span>
        """
    
    action_html = ""
    if action_label and action_key:
        action_html = f"""
            <button class="section-action" key="{action_key}">
                {action_label}
            </button>
        """
    
    st.markdown(f"""
    <div class="section-header">
        <div style="display: flex; align-items: center; gap: {SPACING['md']}px;">
            <h2>{title}</h2>
            {badge_html}
        </div>
        {action_html}
    </div>
    """, unsafe_allow_html=True)


def render_status_dot(active: bool) -> str:
    """
    Render a status dot indicator
    
    Args:
        active: True for active, False for inactive
        
    Returns:
        HTML string for the status dot
    """
    return f"""
    <span class="status-dot {'active' if active else 'inactive'}"></span>
    """


def render_empty_state(
    message: str,
    icon: str = "📭",
    suggestion: Optional[str] = None
) -> None:
    """
    Render an empty state message
    
    Args:
        message: Main message
        icon: Icon emoji
        suggestion: Optional suggestion text
    """
    suggestion_html = ""
    if suggestion:
        suggestion_html = f"""
        <div style="
            font-size: {TYPOGRAPHY['body']['size']}px;
            color: {COLORS['neutrals']['dark_gray']};
            margin-top: {SPACING['sm']}px;
        ">
            💡 {suggestion}
        </div>
        """
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: {SPACING['xxxxl']}px {SPACING['xxl']}px;
        background: {COLORS['neutrals']['off_white']};
        border-radius: {BORDER_RADIUS['lg']}px;
        border: 2px dashed {COLORS['neutrals']['light_gray']};
    ">
        <div style="font-size: 48px; margin-bottom: {SPACING['md']}px;">{icon}</div>
        <div style="
            font-size: {TYPOGRAPHY['headline']['size']}px;
            font-weight: {TYPOGRAPHY['headline']['weight']};
            color: {COLORS['primary']['deepest_navy']};
        ">
            {message}
        </div>
        {suggestion_html}
    </div>
    """, unsafe_allow_html=True)