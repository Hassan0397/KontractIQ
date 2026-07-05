"""
KontractIQ - Reusable Card Components
"""

import streamlit as st
from ..utils.constants import COLORS, BORDER_RADIUS, SHADOWS, SPACING

def render_info_card(title: str, value: str, icon: str = "", color: str = None, subtitle: str = None):
    """
    Render an information card with icon and value
    
    Args:
        title: Card title/label
        value: Main value to display
        icon: Emoji or icon
        color: Border color
        subtitle: Optional subtitle text
    """
    if color is None:
        color = COLORS['primary']['corporate_blue']
    
    st.markdown(f"""
    <div style="
        background-color: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['lg']}px;
        padding: {SPACING['lg']}px;
        box-shadow: {SHADOWS['md']};
        border-left: 4px solid {color};
        transition: box-shadow 0.3s ease;
        height: 100%;
    ">
        <div style="display: flex; align-items: center; gap: {SPACING['sm']}px;">
            {f'<span style="font-size: 24px;">{icon}</span>' if icon else ''}
            <div>
                <div style="font-size: 28px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">
                    {value}
                </div>
                <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">
                    {title}
                </div>
                {f'<div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, change: str = None, icon: str = "", color: str = None):
    """
    Render a metric card with optional change indicator
    
    Args:
        label: Metric label
        value: Metric value
        change: Change indicator (e.g., "+12%")
        icon: Emoji or icon
        color: Border color
    """
    if color is None:
        color = COLORS['primary']['corporate_blue']
    
    change_color = COLORS['semantic']['success'] if change and '+' in change else COLORS['semantic']['danger'] if change and '-' in change else COLORS['neutrals']['medium_gray']
    
    st.markdown(f"""
    <div style="
        background-color: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        box-shadow: {SHADOWS['sm']};
        text-align: center;
        border-top: 3px solid {color};
        transition: box-shadow 0.3s ease;
    ">
        <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']}; margin-bottom: 4px;">
            {icon} {label}
        </div>
        <div style="font-size: 28px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">
            {value}
        </div>
        {f'<div style="font-size: 13px; color: {change_color}; margin-top: 4px;">{change}</div>' if change else ''}
    </div>
    """, unsafe_allow_html=True)


def render_clause_card(clause_text: str, clause_type: str, contract_name: str, confidence: float = 1.0):
    """
    Render a clause card with type and contract info
    
    Args:
        clause_text: The clause text
        clause_type: Type of clause
        contract_name: Contract name
        confidence: Confidence score (0-1)
    """
    confidence_color = COLORS['semantic']['success'] if confidence >= 0.8 else COLORS['semantic']['warning'] if confidence >= 0.5 else COLORS['semantic']['danger']
    
    st.markdown(f"""
    <div style="
        background-color: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        box-shadow: {SHADOWS['sm']};
        border-left: 4px solid {COLORS['primary']['corporate_blue']};
        margin-bottom: {SPACING['sm']}px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="font-size: 13px; color: {COLORS['neutrals']['medium_gray']};">
                    {clause_type}
                </div>
                <div style="font-size: 14px; color: {COLORS['primary']['deepest_navy']}; margin: 4px 0;">
                    {clause_text[:200]}{'...' if len(clause_text) > 200 else ''}
                </div>
                <div style="font-size: 12px; color: {COLORS['neutrals']['dark_gray']};">
                    📄 {contract_name}
                </div>
            </div>
            <div style="text-align: right; min-width: 80px;">
                <div style="font-size: 12px; color: {confidence_color};">
                    {f'{confidence * 100:.0f}%' if confidence else 'N/A'}
                </div>
                <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']};">
                    Confidence
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_card(risk_type: str, severity: str, description: str, contract_name: str, recommendation: str = None):
    """
    Render a risk card with severity indicator
    
    Args:
        risk_type: Type of risk
        severity: critical, high, medium, low
        description: Risk description
        contract_name: Contract name
        recommendation: Optional recommendation
    """
    severity_colors = {
        'critical': {'color': COLORS['semantic']['danger'], 'bg': COLORS['semantic']['danger_bg']},
        'high': {'color': COLORS['semantic']['warning'], 'bg': COLORS['semantic']['warning_bg']},
        'medium': {'color': COLORS['semantic']['warning'], 'bg': COLORS['semantic']['warning_bg']},
        'low': {'color': COLORS['semantic']['info'], 'bg': COLORS['semantic']['info_bg']}
    }
    
    colors = severity_colors.get(severity, {'color': COLORS['neutrals']['medium_gray'], 'bg': COLORS['neutrals']['off_white']})
    
    st.markdown(f"""
    <div style="
        background-color: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        box-shadow: {SHADOWS['sm']};
        border-left: 4px solid {colors['color']};
        margin-bottom: {SPACING['sm']}px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="display: flex; gap: {SPACING['sm']}px; align-items: center; margin-bottom: 4px;">
                    <span style="
                        background-color: {colors['bg']};
                        color: {colors['color']};
                        padding: 2px 10px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: 600;
                    ">{severity.upper()}</span>
                    <span style="font-size: 14px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">
                        {risk_type.replace('_', ' ').title()}
                    </span>
                </div>
                <div style="font-size: 14px; color: {COLORS['neutrals']['dark_gray']};">
                    {description}
                </div>
                <div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">
                    📄 {contract_name}
                </div>
                {f'<div style="font-size: 13px; color: {COLORS['primary']['corporate_blue']}; margin-top: 8px; padding: 8px; background-color: {COLORS['primary']['ice_blue']}; border-radius: {BORDER_RADIUS['sm']}px;">💡 {recommendation}</div>' if recommendation else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_contract_card(contract):
    """
    Render a contract card with summary information
    
    Args:
        contract: Contract object
    """
    st.markdown(f"""
    <div style="
        background-color: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px;
        box-shadow: {SHADOWS['sm']};
        margin-bottom: {SPACING['sm']}px;
        transition: box-shadow 0.3s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <div style="font-size: 16px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">
                    {contract.name}
                </div>
                <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">
                    {contract.file_type.upper()} • {contract.pages} pages • {contract.upload_date.strftime('%Y-%m-%d')}
                    {f' • ⚠️ Scanned' if contract.is_scanned else ''}
                </div>
            </div>
            <div style="display: flex; gap: {SPACING['lg']}px;">
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: 600; color: {COLORS['primary']['corporate_blue']};">
                        {contract.clause_count}
                    </div>
                    <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']};">
                        Clauses
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: 600; color: {COLORS['semantic']['danger'] if contract.risk_count > 0 else COLORS['semantic']['success']};">
                        {contract.risk_count}
                    </div>
                    <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']};">
                        Risks
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)