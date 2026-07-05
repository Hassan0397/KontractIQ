"""
KontractIQ - Reusable Chart Components
Optimized with caching for performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional, Dict, Any
from functools import lru_cache
from ..utils.constants import COLORS, TYPOGRAPHY


@st.cache_data(ttl=300)
def create_risk_distribution_data(risks: List[Any]) -> pd.DataFrame:
    """Cache risk distribution data"""
    severity_counts = {
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    for risk in risks:
        if risk.severity in severity_counts:
            severity_counts[risk.severity] += 1
    
    df = pd.DataFrame({
        'Severity': ['Critical', 'High', 'Medium', 'Low'],
        'Count': [
            severity_counts['critical'],
            severity_counts['high'],
            severity_counts['medium'],
            severity_counts['low']
        ]
    })
    return df


@st.cache_data(ttl=300)
def create_clause_distribution_data(clauses: List[Any]) -> pd.DataFrame:
    """Cache clause distribution data"""
    type_counts = {}
    for clause in clauses:
        type_counts[clause.type] = type_counts.get(clause.type, 0) + 1
    
    df = pd.DataFrame({
        'Clause Type': list(type_counts.keys()),
        'Count': list(type_counts.values())
    })
    return df.sort_values('Count', ascending=True)


def render_risk_distribution_chart(
    risks: List[Any],
    height: int = 350,
    show_legend: bool = True
) -> None:
    """
    Render a risk distribution chart - OPTIMIZED
    
    Args:
        risks: List of risk objects
        height: Chart height in pixels
        show_legend: Whether to show legend
    """
    if not risks:
        st.info("No risks to display")
        return
    
    df = create_risk_distribution_data(risks)
    
    # Color mapping
    color_map = {
        'Critical': COLORS['semantic']['danger'],
        'High': COLORS['semantic']['warning'],
        'Medium': COLORS['semantic']['warning'],
        'Low': COLORS['semantic']['info']
    }
    
    fig = px.bar(
        df,
        x='Severity',
        y='Count',
        color='Severity',
        color_discrete_map=color_map,
        text='Count',
        height=height
    )
    
    fig.update_traces(
        textposition='outside',
        marker=dict(
            line=dict(width=1, color='rgba(0,0,0,0.1)')
        ),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        showlegend=show_legend,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, sans-serif',
            color=COLORS['neutrals']['dark_gray'],
            size=12
        ),
        xaxis=dict(
            title=None,
            gridcolor='rgba(0,0,0,0)',
            tickfont=dict(size=13)
        ),
        yaxis=dict(
            title=None,
            gridcolor=COLORS['neutrals']['light_gray'],
            gridwidth=0.5,
            tickfont=dict(size=12)
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_clause_distribution_chart(
    clauses: List[Any],
    height: int = 350,
    max_items: int = 20
) -> None:
    """
    Render a clause type distribution chart - OPTIMIZED
    
    Args:
        clauses: List of clause objects
        height: Chart height in pixels
        max_items: Maximum number of items to show
    """
    if not clauses:
        st.info("No clauses to display")
        return
    
    df = create_clause_distribution_data(clauses)
    
    # Limit items if too many
    if len(df) > max_items:
        df = df.tail(max_items)
    
    fig = px.bar(
        df,
        x='Count',
        y='Clause Type',
        title='',
        orientation='h',
        color='Count',
        color_continuous_scale='Blues',
        text='Count',
        height=height
    )
    
    fig.update_traces(
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, sans-serif',
            color=COLORS['neutrals']['dark_gray'],
            size=12
        ),
        xaxis=dict(
            title=None,
            gridcolor=COLORS['neutrals']['light_gray'],
            gridwidth=0.5,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title=None,
            gridcolor='rgba(0,0,0,0)',
            tickfont=dict(size=13),
            categoryorder='total ascending'
        ),
        margin=dict(l=10, r=30, t=20, b=20),
        coloraxis_showscale=False,
        hovermode='y'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_contract_metrics_chart(
    contracts: List[Any],
    height: int = 350,
    max_contracts: int = 20
) -> None:
    """
    Render contract metrics comparison chart - OPTIMIZED
    
    Args:
        contracts: List of contract objects
        height: Chart height in pixels
        max_contracts: Maximum number of contracts to show
    """
    if not contracts:
        st.info("No contracts to display")
        return
    
    # Limit contracts for performance
    contracts_to_show = contracts[:max_contracts]
    
    data = []
    for contract in contracts_to_show:
        name = contract.name[:25] + '...' if len(contract.name) > 25 else contract.name
        data.append({
            'Contract': name,
            'Clauses': contract.clause_count,
            'Risks': contract.risk_count,
            'Pages': contract.pages
        })
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Contract'],
        y=df['Clauses'],
        name='Clauses',
        marker_color=COLORS['primary']['corporate_blue'],
        hovertemplate='<b>%{x}</b><br>Clauses: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=df['Contract'],
        y=df['Risks'],
        name='Risks',
        marker_color=COLORS['semantic']['warning'],
        hovertemplate='<b>%{x}</b><br>Risks: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=None,
            font=dict(size=16, color=COLORS['primary']['deepest_navy'])
        ),
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, sans-serif',
            color=COLORS['neutrals']['dark_gray'],
            size=12
        ),
        xaxis=dict(
            title=None,
            gridcolor='rgba(0,0,0,0)',
            tickfont=dict(size=11),
            tickangle=-30
        ),
        yaxis=dict(
            title=None,
            gridcolor=COLORS['neutrals']['light_gray'],
            gridwidth=0.5,
            tickfont=dict(size=11)
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=12)
        ),
        margin=dict(l=10, r=20, t=30, b=50),
        height=height,
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_payment_terms_chart(
    contracts: List[Any],
    height: int = 350
) -> None:
    """
    Render payment terms comparison chart - OPTIMIZED
    
    Args:
        contracts: List of contract objects
        height: Chart height in pixels
    """
    if not contracts:
        return
    
    import re
    
    payment_terms = []
    for contract in contracts:
        matches = re.findall(r'(\d+)\s*(?:days|day)', contract.text, re.IGNORECASE)
        if matches:
            try:
                term = int(matches[0])
                if 1 <= term <= 180:  # Reasonable range
                    name = contract.name[:20] + '...' if len(contract.name) > 20 else contract.name
                    payment_terms.append({
                        'Contract': name,
                        'Payment Term (days)': term
                    })
            except:
                pass
    
    if not payment_terms:
        st.info("No payment terms found in contracts")
        return
    
    df = pd.DataFrame(payment_terms)
    
    fig = px.bar(
        df,
        x='Contract',
        y='Payment Term (days)',
        title='',
        color='Payment Term (days)',
        color_continuous_scale='Blues',
        text='Payment Term (days)',
        height=height
    )
    
    fig.update_traces(
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Payment Term: %{y} days<extra></extra>'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, sans-serif',
            color=COLORS['neutrals']['dark_gray'],
            size=12
        ),
        xaxis=dict(
            title=None,
            gridcolor='rgba(0,0,0,0)',
            tickfont=dict(size=11),
            tickangle=-30
        ),
        yaxis=dict(
            title=None,
            gridcolor=COLORS['neutrals']['light_gray'],
            gridwidth=0.5,
            tickfont=dict(size=11)
        ),
        margin=dict(l=10, r=20, t=20, b=50),
        coloraxis_showscale=False,
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_activity_timeline(
    contracts: List[Any],
    height: int = 300,
    max_items: int = 10
) -> None:
    """
    Render a contract activity timeline - OPTIMIZED
    
    Args:
        contracts: List of contract objects
        height: Chart height in pixels
        max_items: Maximum items to show
    """
    if not contracts:
        return
    
    # Sort by upload date
    sorted_contracts = sorted(contracts, key=lambda c: c.upload_date, reverse=True)[:max_items]
    
    data = []
    for contract in sorted_contracts:
        data.append({
            'Contract': contract.name[:30] + '...' if len(contract.name) > 30 else contract.name,
            'Upload Date': contract.upload_date,
            'Clauses': contract.clause_count,
            'Risks': contract.risk_count
        })
    
    df = pd.DataFrame(data)
    
    # Create timeline with markers
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Upload Date'],
        y=[1] * len(df),
        mode='markers+text',
        text=df['Contract'],
        textposition='top center',
        marker=dict(
            size=20,
            color=COLORS['primary']['corporate_blue'],
            symbol='circle',
            line=dict(width=2, color=COLORS['neutrals']['white'])
        ),
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Clauses: %{customdata[0]}<br>Risks: %{customdata[1]}<extra></extra>',
        customdata=df[['Clauses', 'Risks']].values,
        name=''
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, sans-serif',
            color=COLORS['neutrals']['dark_gray'],
            size=12
        ),
        xaxis=dict(
            title=None,
            gridcolor='rgba(0,0,0,0)',
            showticklabels=True,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title=None,
            showticklabels=False,
            showgrid=False,
            range=[0.5, 1.5]
        ),
        margin=dict(l=10, r=20, t=60, b=30),
        height=height,
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})