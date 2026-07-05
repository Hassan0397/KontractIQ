"""
KontractIQ - Vendor Consistency Page
Premium Enterprise-Grade Vendor Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import the Contract class
from ..models.contract import Contract

# Premium Design System
DESIGN = {
    'colors': {
        'primary': {
            'deepest_navy': '#0B1A2F',
            'rich_navy': '#1B3A5C',
            'corporate_blue': '#2B6CB0',
            'light_blue': '#EBF4FF'
        },
        'semantic': {
            'success': '#38A169',
            'success_bg': '#F0FFF4',
            'warning': '#D69E2E',
            'warning_bg': '#FFFFF0',
            'danger': '#E53E3E',
            'danger_bg': '#FFF5F5',
            'info': '#3182CE',
            'info_bg': '#EBF8FF'
        },
        'neutrals': {
            'white': '#FFFFFF',
            'off_white': '#F7FAFC',
            'light_gray': '#EDF2F7',
            'medium_gray': '#A0AEC0',
            'dark_gray': '#4A5568',
            'text_primary': '#1A202C',
            'text_secondary': '#4A5568'
        }
    },
    'spacing': {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48
    },
    'border_radius': {
        'sm': 6,
        'md': 10,
        'lg': 16,
        'xl': 20,
        'xxl': 24
    },
    'shadows': {
        'sm': '0 1px 3px rgba(0,0,0,0.08)',
        'md': '0 4px 12px rgba(0,0,0,0.08)',
        'lg': '0 8px 24px rgba(0,0,0,0.10)',
        'xl': '0 12px 40px rgba(0,0,0,0.12)'
    },
    'typography': {
        'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'heading_1': {'size': 28, 'weight': 700, 'line_height': 1.2},
        'heading_2': {'size': 22, 'weight': 600, 'line_height': 1.3},
        'heading_3': {'size': 18, 'weight': 600, 'line_height': 1.4},
        'body': {'size': 14, 'weight': 400, 'line_height': 1.6},
        'caption': {'size': 12, 'weight': 400, 'line_height': 1.5}
    }
}


def render_vendor_consistency():
    """Render the vendor consistency page with Premium UI"""
    
    # ========================================================================
    # PAGE HEADER WITH HERO SECTION
    # ========================================================================
    
    st.markdown(f"""
    <style>
        /* Reset and base styles */
        .main .block-container {{
            padding: 1.5rem 2rem 2rem 2rem !important;
            max-width: 1400px !important;
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: {DESIGN['colors']['neutrals']['off_white']};
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb {{
            background: {DESIGN['colors']['neutrals']['medium_gray']};
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {DESIGN['colors']['primary']['corporate_blue']};
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {DESIGN['colors']['primary']['deepest_navy']} 0%, {DESIGN['colors']['primary']['rich_navy']} 100%);
        padding: 32px 40px;
        border-radius: {DESIGN['border_radius']['xl']}px;
        margin-bottom: 28px;
        box-shadow: {DESIGN['shadows']['xl']};
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: rgba(43, 108, 176, 0.1); border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -40%; left: -5%; width: 300px; height: 300px; background: rgba(43, 108, 176, 0.08); border-radius: 50%;"></div>
        <div style="display: flex; align-items: center; gap: 20px; position: relative; z-index: 1;">
            <div style="background: rgba(255,255,255,0.12); padding: 14px; border-radius: {DESIGN['border_radius']['lg']}px; backdrop-filter: blur(10px);">
                <span style="font-size: 36px;">🏢</span>
            </div>
            <div>
                <h1 style="color: #FFFFFF; font-size: 30px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                    Vendor Consistency Analysis
                </h1>
                <p style="color: rgba(255,255,255,0.85); font-size: 15px; margin: 6px 0 0 0; font-weight: 400; opacity: 0.9;">
                    Enterprise-grade vendor contract analysis and risk management
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # USER INSTRUCTION SECTION
    # ========================================================================
    
    render_instructions()
    
    # ========================================================================
    # CHECK CONTRACTS
    # ========================================================================
    
    if not st.session_state.contracts:
        render_empty_state()
        return
    
    # ========================================================================
    # EXTRACT VENDOR DATA
    # ========================================================================
    
    vendor_data = extract_vendor_data(st.session_state.contracts)
    
    if not vendor_data:
        st.info("📭 No vendors could be identified in your contracts. Try uploading contracts with vendor information.")
        return
    
    # ========================================================================
    # STATISTICS CARDS - PREMIUM
    # ========================================================================
    
    render_vendor_statistics(vendor_data)
    
    # ========================================================================
    # VENDOR SUMMARY TABLE
    # ========================================================================
    
    st.divider()
    render_vendor_summary(vendor_data)
    
    # ========================================================================
    # VENDOR DETAILED ANALYSIS
    # ========================================================================
    
    st.divider()
    render_vendor_detail_analysis(vendor_data)
    
    # ========================================================================
    # VENDOR COMPARISON CHARTS
    # ========================================================================
    
    st.divider()
    render_vendor_charts(vendor_data)
    
    # ========================================================================
    # EXPORT SECTION
    # ========================================================================
    
    st.divider()
    render_export_section(vendor_data)


# ============================================================================
# INSTRUCTION COMPONENT
# ============================================================================

def render_instructions():
    """Render user instructions with premium styling"""
    
    with st.expander("📖 How to Use Vendor Consistency", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔍 What This Page Does**
            - Groups contracts by vendor automatically
            - Shows contract counts and metrics per vendor
            - Identifies inconsistencies across vendor contracts
            - Provides risk distribution analysis
            - Helps standardize vendor contract terms
            """)
        
        with col2:
            st.markdown("""
            **💡 How to Use**
            - **Upload contracts** with vendor information
            - View the **Vendor Summary** table for overview
            - Select a vendor for **detailed analysis**
            - Review **risk distributions** by vendor
            - **Export** vendor analysis reports
            """)
        
        st.info("💡 **Tip:** Vendor names are automatically extracted from contract filenames and text. Ensure your contracts include vendor names in the filename or content for best results.")


# ============================================================================
# EMPTY STATE
# ============================================================================

def render_empty_state():
    """Render empty state with action buttons"""
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 80px 40px;
        background: {DESIGN['colors']['neutrals']['white']};
        border-radius: {DESIGN['border_radius']['xl']}px;
        box-shadow: {DESIGN['shadows']['md']};
        border: 2px dashed {DESIGN['colors']['neutrals']['light_gray']};
    ">
        <span style="font-size: 72px;">📭</span>
        <h2 style="color: {DESIGN['colors']['primary']['deepest_navy']}; margin: 20px 0 12px 0; font-weight: 600;">
            No Contracts Found
        </h2>
        <p style="color: {DESIGN['colors']['neutrals']['dark_gray']}; font-size: 16px; margin-bottom: 28px;">
            Upload contracts to start analyzing vendor consistency
        </p>
        <div style="display: flex; gap: 12px; justify-content: center;">
            <button onclick="parent.postMessage('navigate:Upload Contracts', '*')" style="
                background: {DESIGN['colors']['primary']['corporate_blue']};
                color: white;
                padding: 12px 28px;
                border: none;
                border-radius: {DESIGN['border_radius']['md']}px;
                font-weight: 500;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.2s;
            ">📤 Upload Contracts</button>
            <button onclick="parent.postMessage('navigate:Dashboard', '*')" style="
                background: {DESIGN['colors']['neutrals']['off_white']};
                color: {DESIGN['colors']['primary']['deepest_navy']};
                padding: 12px 28px;
                border: 1px solid {DESIGN['colors']['neutrals']['light_gray']};
                border-radius: {DESIGN['border_radius']['md']}px;
                font-weight: 500;
                cursor: pointer;
                font-size: 14px;
            ">🏠 Go to Dashboard</button>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# VENDOR DATA EXTRACTION
# ============================================================================

def extract_vendor_data(contracts: List[Contract]) -> Dict[str, Dict[str, Any]]:
    """
    Extract and group contracts by vendor
    
    Returns:
        Dict mapping vendor name to vendor data
    """
    vendors = {}
    
    for contract in contracts:
        # Use contract.vendor property if available (from enhanced model)
        if hasattr(contract, 'vendor') and contract.vendor:
            vendor_name = contract.vendor
        else:
            # Fallback: extract from filename
            name_parts = contract.name.replace('.pdf', '').replace('.docx', '').replace('.txt', '').split('_')
            vendor_name = name_parts[0] if name_parts else "Unknown"
            
            # Try to extract from text using patterns
            if vendor_name == "Unknown" and hasattr(contract, 'text') and contract.text:
                import re
                patterns = [
                    r'between\s+([A-Z][a-zA-Z\s]+?)(?:\s+and\s+|\s*\(|\s*$)',
                    r'by and between\s+([A-Z][a-zA-Z\s]+?)(?:\s+and\s+|\s*\(|\s*$)',
                ]
                for pattern in patterns:
                    match = re.search(pattern, contract.text, re.IGNORECASE)
                    if match:
                        vendor_name = match.group(1).strip()
                        break
        
        if vendor_name not in vendors:
            vendors[vendor_name] = {
                'name': vendor_name,
                'contracts': [],
                'total_clauses': 0,
                'total_risks': 0,
                'critical_risks': 0,
                'high_risks': 0,
                'medium_risks': 0,
                'low_risks': 0,
                'clause_types': set(),
                'risk_types': set(),
                'contract_values': [],
                'total_risk_score': 0
            }
        
        # Add contract to vendor
        vendors[vendor_name]['contracts'].append(contract)
        
        # Aggregate metrics - use getattr to handle missing attributes
        vendors[vendor_name]['total_clauses'] += getattr(contract, 'clause_count', 0)
        vendors[vendor_name]['total_risks'] += getattr(contract, 'risk_count', 0)
        
        # Aggregate risk severities
        if hasattr(contract, 'risk_severity_summary'):
            for severity, count in contract.risk_severity_summary.items():
                if severity == 'critical':
                    vendors[vendor_name]['critical_risks'] += count
                elif severity == 'high':
                    vendors[vendor_name]['high_risks'] += count
                elif severity == 'medium':
                    vendors[vendor_name]['medium_risks'] += count
                elif severity == 'low':
                    vendors[vendor_name]['low_risks'] += count
        
        # Collect clause types
        if hasattr(contract, 'clause_types'):
            vendors[vendor_name]['clause_types'].update(contract.clause_types)
        
        # Collect risk types
        if hasattr(contract, 'risks'):
            for risk in contract.risks:
                if hasattr(risk, 'type'):
                    vendors[vendor_name]['risk_types'].add(risk.type)
        
        # Collect contract values
        if hasattr(contract, 'contract_value') and contract.contract_value:
            vendors[vendor_name]['contract_values'].append(contract.contract_value)
        
        # Total risk score
        vendors[vendor_name]['total_risk_score'] += getattr(contract, 'total_risk_score', 0)
    
    # Calculate derived metrics
    for vendor_name, data in vendors.items():
        contract_count = len(data['contracts'])
        data['contract_count'] = contract_count
        data['avg_clauses'] = data['total_clauses'] / contract_count if contract_count > 0 else 0
        data['avg_risks'] = data['total_risks'] / contract_count if contract_count > 0 else 0
        data['avg_risk_score'] = data['total_risk_score'] / contract_count if contract_count > 0 else 0
        data['clause_type_count'] = len(data['clause_types'])
        data['risk_type_count'] = len(data['risk_types'])
        data['avg_contract_value'] = sum(data['contract_values']) / len(data['contract_values']) if data['contract_values'] else None
        data['has_contract_values'] = len(data['contract_values']) > 0
        
        # Health status based on risk score
        if data['total_risk_score'] == 0:
            data['health'] = 'healthy'
        elif data['total_risk_score'] < 10:
            data['health'] = 'warning'
        elif data['total_risk_score'] < 25:
            data['health'] = 'scanned'
        else:
            data['health'] = 'critical'
    
    return vendors


# ============================================================================
# VENDOR STATISTICS CARDS 
# ============================================================================

def render_vendor_statistics(vendor_data: Dict[str, Dict[str, Any]]):
    """Render premium enterprise-grade statistics cards"""
    
    total_vendors = len(vendor_data)
    total_contracts = sum(d['contract_count'] for d in vendor_data.values())
    total_clauses = sum(d['total_clauses'] for d in vendor_data.values())
    total_risks = sum(d['total_risks'] for d in vendor_data.values())
    
    # Find vendor with most contracts
    top_vendor = max(vendor_data.items(), key=lambda x: x[1]['contract_count'])
    top_vendor_name = top_vendor[0]
    top_vendor_count = top_vendor[1]['contract_count']
    
    # Premium card styling with CSS
    st.markdown("""
    <style>
        .stat-card {
            background: white;
            padding: 20px 24px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid #EDF2F7;
            transition: all 0.2s ease;
            height: 100%;
        }
        .stat-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transform: translateY(-2px);
            border-color: #CBD5E0;
        }
        .stat-label {
            font-size: 13px;
            font-weight: 500;
            color: #718096;
            letter-spacing: 0.3px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #1A202C;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }
        .stat-sub {
            font-size: 12px;
            color: #A0AEC0;
            margin-top: 4px;
        }
        .stat-icon {
            font-size: 20px;
            margin-right: 8px;
        }
        .stat-divider {
            display: inline-block;
            width: 3px;
            height: 28px;
            background: #E2E8F0;
            margin: 0 12px;
            border-radius: 2px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🏢 Total Vendors</div>
            <div class="stat-value">{total_vendors}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📄 Total Contracts</div>
            <div class="stat-value">{total_contracts}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📝 Total Clauses</div>
            <div class="stat-value">{total_clauses}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">⚠️ Total Risks</div>
            <div class="stat-value">{total_risks}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🏆 Top Vendor</div>
            <div class="stat-value" style="font-size: 22px;">{top_vendor_name[:20]}{'...' if len(top_vendor_name) > 20 else ''}</div>
            <div class="stat-sub">{top_vendor_count} contract{'s' if top_vendor_count != 1 else ''}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# VENDOR SUMMARY TABLE
# ============================================================================

def render_vendor_summary(vendor_data: Dict[str, Dict[str, Any]]):
    """Render vendor summary with premium table"""
    
    st.markdown(f"""
    <h2 style="font-size: 22px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin-bottom: 16px;">
        📊 Vendor Summary
    </h2>
    """, unsafe_allow_html=True)
    
    # Prepare data for table
    table_data = []
    for vendor_name, data in vendor_data.items():
        health_icon = {
            'healthy': '✅',
            'warning': '⚠️',
            'scanned': '📄',
            'critical': '🔴'
        }.get(data['health'], '❓')
        
        table_data.append({
            'Vendor': vendor_name,
            'Contracts': data['contract_count'],
            'Clauses': data['total_clauses'],
            'Risks': data['total_risks'],
            'Critical': data['critical_risks'],
            'High': data['high_risks'],
            'Health': f"{health_icon} {data['health'].title()}",
            'Avg Clauses': f"{data['avg_clauses']:.1f}",
            'Avg Risks': f"{data['avg_risks']:.1f}",
            'Clause Types': data['clause_type_count'],
            'Risk Types': data['risk_type_count']
        })
    
    df = pd.DataFrame(table_data)
    
    # Apply styling with Streamlit's column config
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Vendor": st.column_config.TextColumn("🏢 Vendor", width="medium"),
            "Contracts": st.column_config.NumberColumn("📄 Contracts", width="small"),
            "Clauses": st.column_config.NumberColumn("📝 Clauses", width="small"),
            "Risks": st.column_config.NumberColumn("⚠️ Risks", width="small"),
            "Critical": st.column_config.NumberColumn("🔴 Critical", width="small"),
            "High": st.column_config.NumberColumn("🟠 High", width="small"),
            "Health": st.column_config.TextColumn("💚 Health", width="small"),
            "Avg Clauses": st.column_config.TextColumn("📊 Avg Clauses", width="small"),
            "Avg Risks": st.column_config.TextColumn("📊 Avg Risks", width="small"),
            "Clause Types": st.column_config.NumberColumn("📋 Clause Types", width="small"),
            "Risk Types": st.column_config.NumberColumn("⚠️ Risk Types", width="small"),
        }
    )


# ============================================================================
# VENDOR DETAIL ANALYSIS - PREMIUM ENTERPRISE
# ============================================================================

def render_vendor_detail_analysis(vendor_data: Dict[str, Dict[str, Any]]):
    """Render detailed vendor analysis with Premium UI"""
    
    st.markdown(f"""
    <h2 style="font-size: 22px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin-bottom: 16px;">
        🔍 Vendor Detail Analysis
    </h2>
    """, unsafe_allow_html=True)
    
    vendor_names = sorted(vendor_data.keys())
    selected_vendor = st.selectbox(
        "Select a vendor for detailed analysis",
        options=vendor_names,
        key="vendor_detail_select"
    )
    
    if selected_vendor:
        data = vendor_data[selected_vendor]
        contracts = data['contracts']
        
        # Premium Vendor Profile Card
        health = data['health']
        health_icon = {
            'healthy': '✅',
            'warning': '⚠️',
            'scanned': '📄',
            'critical': '🔴'
        }.get(health, '❓')
        
        health_color = {
            'healthy': '#38A169',
            'warning': '#D69E2E',
            'scanned': '#3182CE',
            'critical': '#E53E3E'
        }.get(health, '#A0AEC0')
        
        health_bg = {
            'healthy': '#F0FFF4',
            'warning': '#FFFFF0',
            'scanned': '#EBF8FF',
            'critical': '#FFF5F5'
        }.get(health, '#F7FAFC')
        
        # Vendor Profile Card
        st.markdown(f"""
        <div style="
            background: {DESIGN['colors']['neutrals']['white']};
            padding: 24px 28px;
            border-radius: {DESIGN['border_radius']['lg']}px;
            box-shadow: {DESIGN['shadows']['md']};
            margin-bottom: 24px;
            border: 1px solid {DESIGN['colors']['neutrals']['light_gray']};
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
                        <span style="font-size: 28px; font-weight: 700; color: {DESIGN['colors']['primary']['deepest_navy']};">
                            {selected_vendor}
                        </span>
                        <span style="
                            background: {health_bg};
                            color: {health_color};
                            padding: 4px 14px;
                            border-radius: 20px;
                            font-size: 13px;
                            font-weight: 600;
                        ">
                            {health_icon} {health.title()}
                        </span>
                    </div>
                    <div style="font-size: 14px; color: {DESIGN['colors']['neutrals']['dark_gray']};">
                        📊 {data['contract_count']} contracts • 📝 {data['total_clauses']} clauses • ⚠️ {data['total_risks']} risks
                    </div>
                </div>
                <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                    <div style="text-align: center; padding: 8px 16px; background: {DESIGN['colors']['neutrals']['off_white']}; border-radius: {DESIGN['border_radius']['md']}px;">
                        <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['primary']['corporate_blue']};">{data['clause_type_count']}</div>
                        <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Clause Types</div>
                    </div>
                    <div style="text-align: center; padding: 8px 16px; background: {DESIGN['colors']['neutrals']['off_white']}; border-radius: {DESIGN['border_radius']['md']}px;">
                        <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['semantic']['warning']};">{data['risk_type_count']}</div>
                        <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Risk Types</div>
                    </div>
                    <div style="text-align: center; padding: 8px 16px; background: {DESIGN['colors']['neutrals']['off_white']}; border-radius: {DESIGN['border_radius']['md']}px;">
                        <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['semantic']['danger']};">{data['critical_risks']}</div>
                        <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Critical Risks</div>
                    </div>
                    <div style="text-align: center; padding: 8px 16px; background: {DESIGN['colors']['neutrals']['off_white']}; border-radius: {DESIGN['border_radius']['md']}px;">
                        <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['semantic']['success']};">{'$' + f'{data["avg_contract_value"]:,.0f}' if data['has_contract_values'] and data['avg_contract_value'] else 'N/A'}</div>
                        <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Avg Value</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contract Cards Section - USING NATIVE STREAMLIT COMPONENTS
        st.markdown(f"""
        <h3 style="font-size: 18px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin: 20px 0 16px 0;">
            📄 Contracts ({len(contracts)})
        </h3>
        """, unsafe_allow_html=True)
        
        for contract in contracts:
            render_contract_card_native(contract)


# ============================================================================
# CONTRACT CARD COMPONENT - NATIVE STREAMLIT (NO HTML RENDERING ISSUES)
# ============================================================================

def render_contract_card_native(contract: Contract):
    """Render a premium contract card using native Streamlit components - NO HTML"""
    
    # Get contract attributes
    health = getattr(contract, 'overall_health', 'scanned')
    health_icon = {
        'healthy': '✅',
        'warning': '⚠️',
        'critical': '🔴',
        'scanned': '📄'
    }.get(health, '❓')
    
    # Collect clause types
    clause_types_list = getattr(contract, 'clause_types', [])
    clause_types_display = ', '.join(clause_types_list[:5])
    if len(clause_types_list) > 5:
        clause_types_display += f' +{len(clause_types_list) - 5} more'
    if not clause_types_display:
        clause_types_display = 'No clauses extracted'
    
    # Contract details
    pages = getattr(contract, 'pages', 0)
    clause_count = getattr(contract, 'clause_count', 0)
    risk_count = getattr(contract, 'risk_count', 0)
    health_score = getattr(contract, 'health_score', 0)
    
    # Upload date
    upload_date = getattr(contract, 'upload_date', datetime.now())
    date_str = upload_date.strftime('%Y-%m-%d') if hasattr(upload_date, 'strftime') else str(upload_date)
    
    # Contract value
    value_display = ""
    if hasattr(contract, 'contract_value') and contract.contract_value:
        value_display = f"💰 ${contract.contract_value:,.0f}"
    
    # Use a container with a border using st.markdown for the card background
    st.markdown("""
    <div style="
        background: #FFFFFF;
        padding: 2px;
        border-radius: 10px;
        margin-bottom: 12px;
        border: 1px solid #EDF2F7;
    ">
    </div>
    """, unsafe_allow_html=True)
    
    # Now use native Streamlit components inside the card
    with st.container():
        # First row: Contract name and health status
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{contract.name}** {health_icon}")
        
        with col2:
            # Health status badge using colored text
            health_color_map = {
                'healthy': ('#38A169', '#F0FFF4'),
                'warning': ('#D69E2E', '#FFFFF0'),
                'critical': ('#E53E3E', '#FFF5F5'),
                'scanned': ('#3182CE', '#EBF8FF')
            }
            health_color, health_bg = health_color_map.get(health, ('#A0AEC0', '#F7FAFC'))
            st.markdown(f'<span style="background: {health_bg}; color: {health_color}; padding: 4px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; float: right;">{health.title()}</span>', unsafe_allow_html=True)
        
        # Second row: Contract metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.caption(f"📄 {pages} pages")
        with col2:
            st.caption(f"📝 {clause_count} clauses")
        with col3:
            st.caption(f"⚠️ {risk_count} risks")
        with col4:
            st.caption(f"📅 {date_str}")
        with col5:
            if value_display:
                st.caption(value_display)
        
        # Third row: Clause types
        st.caption(f"📋 {clause_types_display}")
        
        # Fourth row: Health score
        st.caption(f"Score: {health_score}/100")
        
        # Add a subtle divider
        st.divider()


# ============================================================================
# VENDOR RISK DISTRIBUTION - PREMIUM
# ============================================================================

def render_vendor_risk_distribution(data: Dict[str, Any]):
    """Render risk distribution charts with premium styling"""
    
    st.markdown(f"""
    <h3 style="font-size: 18px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin-bottom: 16px;">
        ⚠️ Risk Distribution
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create risk distribution chart
        severity_data = {
            'Critical': data['critical_risks'],
            'High': data['high_risks'],
            'Medium': data['medium_risks'],
            'Low': data['low_risks']
        }
        
        df_risks = pd.DataFrame({
            'Severity': list(severity_data.keys()),
            'Count': list(severity_data.values())
        })
        
        if sum(severity_data.values()) > 0:
            color_map = {
                'Critical': '#E53E3E',
                'High': '#D69E2E',
                'Medium': '#ED8936',
                'Low': '#3182CE'
            }
            
            fig = px.bar(
                df_risks,
                x='Severity',
                y='Count',
                color='Severity',
                color_discrete_map=color_map,
                text='Count',
                title='Risk Distribution by Severity'
            )
            
            fig.update_traces(
                textposition='outside',
                textfont=dict(size=14, family='Inter, sans-serif'),
                marker=dict(line=dict(width=1, color='white'))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=DESIGN['colors']['neutrals']['dark_gray'],
                font_family="Inter, sans-serif",
                showlegend=False,
                height=350,
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis=dict(
                    gridcolor='rgba(0,0,0,0)',
                    tickfont=dict(size=13)
                ),
                yaxis=dict(
                    gridcolor='rgba(0,0,0,0.05)',
                    tickfont=dict(size=12)
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("✅ No risks found for this vendor")
    
    with col2:
        # Risk metrics summary with premium styling
        st.markdown(f"""
        <div style="
            background: {DESIGN['colors']['neutrals']['white']};
            padding: 20px;
            border-radius: {DESIGN['border_radius']['md']}px;
            border: 1px solid {DESIGN['colors']['neutrals']['light_gray']};
        ">
            <div style="font-size: 14px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin-bottom: 16px;">
                📊 Risk Summary
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="text-align: center; padding: 12px; background: {DESIGN['colors']['semantic']['danger_bg']}; border-radius: {DESIGN['border_radius']['sm']}px;">
                    <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['semantic']['danger']};">{data['critical_risks']}</div>
                    <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Critical</div>
                </div>
                <div style="text-align: center; padding: 12px; background: {DESIGN['colors']['semantic']['warning_bg']}; border-radius: {DESIGN['border_radius']['sm']}px;">
                    <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['semantic']['warning']};">{data['high_risks']}</div>
                    <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">High</div>
                </div>
                <div style="text-align: center; padding: 12px; background: #FFFAF0; border-radius: {DESIGN['border_radius']['sm']}px;">
                    <div style="font-size: 24px; font-weight: 700; color: #ED8936;">{data['medium_risks']}</div>
                    <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Medium</div>
                </div>
                <div style="text-align: center; padding: 12px; background: {DESIGN['colors']['semantic']['info_bg']}; border-radius: {DESIGN['border_radius']['sm']}px;">
                    <div style="font-size: 24px; font-weight: 700; color: {DESIGN['colors']['semantic']['info']};">{data['low_risks']}</div>
                    <div style="font-size: 11px; color: {DESIGN['colors']['neutrals']['medium_gray']};">Low</div>
                </div>
            </div>
            <div style="margin-top: 14px; padding: 14px; background: {DESIGN['colors']['primary']['light_blue']}; border-radius: {DESIGN['border_radius']['sm']}px; text-align: center;">
                <div style="font-size: 12px; font-weight: 500; color: {DESIGN['colors']['neutrals']['dark_gray']};">Total Risk Score</div>
                <div style="font-size: 28px; font-weight: 700; color: {DESIGN['colors']['primary']['corporate_blue']};">{data['total_risk_score']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# VENDOR COMPARISON CHARTS
# ============================================================================

def render_vendor_charts(vendor_data: Dict[str, Dict[str, Any]]):
    """Render comparison charts with premium styling"""
    
    st.markdown(f"""
    <h2 style="font-size: 22px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin-bottom: 16px;">
        📊 Vendor Comparison
    </h2>
    """, unsafe_allow_html=True)
    
    # Prepare data
    chart_data = []
    for vendor_name, data in vendor_data.items():
        chart_data.append({
            'Vendor': vendor_name,
            'Contracts': data['contract_count'],
            'Clauses': data['total_clauses'],
            'Risks': data['total_risks'],
            'Critical': data['critical_risks'],
            'High': data['high_risks'],
            'Avg Risk Score': data['avg_risk_score'],
            'Health': data['health']
        })
    
    df_chart = pd.DataFrame(chart_data)
    df_chart = df_chart.sort_values('Contracts', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Contracts by Vendor
        fig1 = px.bar(
            df_chart,
            x='Vendor',
            y='Contracts',
            title='📄 Contracts by Vendor',
            color='Contracts',
            color_continuous_scale='Blues',
            text='Contracts'
        )
        fig1.update_traces(
            textposition='outside',
            textfont=dict(size=13, family='Inter, sans-serif'),
            marker=dict(line=dict(width=1, color='white'))
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=DESIGN['colors']['neutrals']['dark_gray'],
            font_family="Inter, sans-serif",
            coloraxis_showscale=False,
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(gridcolor='rgba(0,0,0,0)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        # Risks by Vendor
        fig2 = px.bar(
            df_chart,
            x='Vendor',
            y='Risks',
            title='⚠️ Risks by Vendor',
            color='Risks',
            color_continuous_scale='Reds',
            text='Risks'
        )
        fig2.update_traces(
            textposition='outside',
            textfont=dict(size=13, family='Inter, sans-serif'),
            marker=dict(line=dict(width=1, color='white'))
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=DESIGN['colors']['neutrals']['dark_gray'],
            font_family="Inter, sans-serif",
            coloraxis_showscale=False,
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(gridcolor='rgba(0,0,0,0)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    
    # Additional comparison: Risk Score by Vendor
    st.markdown(f"""
    <h4 style="font-size: 16px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin: 16px 0 12px 0;">
        📈 Risk Score Comparison
    </h4>
    """, unsafe_allow_html=True)
    
    # Color by health status
    health_colors = {
        'healthy': '#38A169',
        'warning': '#D69E2E',
        'scanned': '#3182CE',
        'critical': '#E53E3E'
    }
    
    fig3 = px.bar(
        df_chart,
        x='Vendor',
        y='Avg Risk Score',
        title='📊 Average Risk Score by Vendor',
        color='Health',
        color_discrete_map=health_colors,
        text='Avg Risk Score'
    )
    fig3.update_traces(
        textposition='outside',
        texttemplate='%{text:.1f}',
        textfont=dict(size=13, family='Inter, sans-serif'),
        marker=dict(line=dict(width=1, color='white'))
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=DESIGN['colors']['neutrals']['dark_gray'],
        font_family="Inter, sans-serif",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})


# ============================================================================
# EXPORT SECTION
# ============================================================================

def render_export_section(vendor_data: Dict[str, Dict[str, Any]]):
    """Render export functionality"""
    
    st.markdown(f"""
    <h2 style="font-size: 22px; font-weight: 600; color: {DESIGN['colors']['primary']['deepest_navy']}; margin-bottom: 16px;">
        📥 Export Analysis
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📊 Export as CSV", key="export_vendor_csv", use_container_width=True):
            # Prepare export data
            export_data = []
            for vendor_name, data in vendor_data.items():
                export_data.append({
                    'Vendor': vendor_name,
                    'Contracts': data['contract_count'],
                    'Total Clauses': data['total_clauses'],
                    'Total Risks': data['total_risks'],
                    'Critical Risks': data['critical_risks'],
                    'High Risks': data['high_risks'],
                    'Medium Risks': data['medium_risks'],
                    'Low Risks': data['low_risks'],
                    'Avg Clauses': f"{data['avg_clauses']:.1f}",
                    'Avg Risks': f"{data['avg_risks']:.1f}",
                    'Clause Types': data['clause_type_count'],
                    'Risk Types': data['risk_type_count'],
                    'Total Risk Score': data['total_risk_score'],
                    'Health Status': data['health']
                })
            
            df_export = pd.DataFrame(export_data)
            csv_data = df_export.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"vendor_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key="download_vendor_csv"
            )
    
    with col2:
        if st.button("📊 Export as JSON", key="export_vendor_json", use_container_width=True):
            import json
            # Clean data for JSON export
            json_export = {}
            for vendor_name, data in vendor_data.items():
                json_export[vendor_name] = {
                    'contract_count': data['contract_count'],
                    'total_clauses': data['total_clauses'],
                    'total_risks': data['total_risks'],
                    'risk_severity': {
                        'critical': data['critical_risks'],
                        'high': data['high_risks'],
                        'medium': data['medium_risks'],
                        'low': data['low_risks']
                    },
                    'clause_types': list(data['clause_types']),
                    'risk_types': list(data['risk_types']),
                    'total_risk_score': data['total_risk_score'],
                    'health': data['health']
                }
            
            json_data = json.dumps(json_export, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"vendor_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="download_vendor_json"
            )
    
    with col3:
        st.caption("💡 Export vendor analysis data for reporting and compliance documentation.")