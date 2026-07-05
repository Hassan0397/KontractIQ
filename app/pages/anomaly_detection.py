"""
KontractIQ - Anomaly Detection Page
Find unusual contract terms and patterns 
"""

import streamlit as st
import pandas as pd
import re
import plotly.express as px
from collections import Counter
from datetime import datetime
from typing import List, Dict, Any

from ..utils.constants import COLORS
from ..models.contract import Contract


def render_anomaly_detection():
    """Render the premium anomaly detection page"""
    
    # ========================================================================
    # HERO SECTION
    # ========================================================================
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(10, 38, 71, 0.15);
    ">
        <div style="display: flex; align-items: center; gap: 16px;">
            <span style="font-size: 40px;">🔍</span>
            <div>
                <h1 style="color: white; font-size: 26px; font-weight: 700; margin: 0; letter-spacing: -0.3px;">
                    Anomaly Detection
                </h1>
                <p style="color: rgba(255,255,255,0.85); font-size: 15px; margin: 4px 0 0 0;">
                    Identify unusual patterns, outliers, and inconsistencies across your contract portfolio
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # CHECK CONTRACTS
    # ========================================================================
    if not st.session_state.contracts:
        st.info("📭 No contracts uploaded yet. Upload contracts first to detect anomalies!")
        return
    
    # ========================================================================
    # QUICK STATS - PREMIUM CARDS
    # ========================================================================
    total_contracts = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    total_risks = len(st.session_state.risks)
    
    # Get anomaly count from session state if available
    anomaly_count = 0
    if 'anomaly_results' in st.session_state and st.session_state.anomaly_results:
        anomaly_count = len(st.session_state.anomaly_results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_premium_card("📄", "Total Contracts", str(total_contracts), COLORS['primary']['corporate_blue'])
    
    with col2:
        render_premium_card("📋", "Total Clauses", str(total_clauses), COLORS['semantic']['success'])
    
    with col3:
        render_premium_card("⚠️", "Total Risks", str(total_risks), COLORS['semantic']['warning'])
    
    with col4:
        render_premium_card("🔍", "Anomalies Found", str(anomaly_count), COLORS['semantic']['danger'] if anomaly_count > 0 else COLORS['primary']['corporate_blue'])
    
    st.divider()
    
    # ========================================================================
    # INSTRUCTION SECTION
    # ========================================================================
    with st.expander("📖 How It Works - Anomaly Detection Guide", expanded=False):
        st.markdown("""
        ### 🎯 What is Anomaly Detection?
        
        Anomaly detection identifies **unusual patterns, outliers, and inconsistencies** across your contract portfolio. 
        It helps you quickly spot contracts that deviate from the norm.
        
        ### 🔍 What We Detect
        
        | Anomaly Type | Description | Why It Matters |
        |--------------|-------------|----------------|
        | **Payment Terms** | Unusual payment periods (e.g., 7 days vs 30 days) | Affects cash flow and vendor relationships |
        | **Liability Caps** | Significantly higher/lower liability limits | Indicates risk exposure differences |
        | **Governing Law** | Uncommon jurisdictions | Compliance and legal risk |
        | **Clause Coverage** | Missing or excessive clauses | Contract completeness assessment |
        | **Risk Density** | Unusual concentration of risks | Risk management prioritization |
        | **Contract Length** | Unusually short or long contracts | Contract complexity assessment |
        
        ### 📊 How to Use
        
        1. Click the **"🔍 Detect Anomalies"** button below
        2. Review the **Anomaly Dashboard** with key metrics
        3. Examine **detailed findings** for each anomaly
        4. Use **filters** to focus on specific anomaly types
        5. **Export reports** for stakeholder sharing
        
        ### 💡 Pro Tips
        
        - 🎯 **More contracts = better baselines** for anomaly detection
        - 🔄 **Run detection regularly** to track changes over time
        - 📊 **Export reports** to share findings with your team
        - 🚨 **Focus on high-severity anomalies** first for maximum impact
        """)
    
    st.divider()
    
    # ========================================================================
    # DETECTION CONTROLS
    # ========================================================================
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 🔍 Detection Controls")
    
    with col2:
        # FIXED: Use a flag-based approach instead of st.rerun()
        if st.button("🔍 Detect Anomalies", key="detect_anomalies_btn", use_container_width=True):
            with st.spinner("🔍 Analyzing contracts for anomalies..."):
                anomalies = detect_comprehensive_anomalies()
                st.session_state.anomaly_results = anomalies
                st.session_state.anomaly_timestamp = datetime.now()
                st.session_state.anomaly_detection_run = True
            st.success(f"✅ Detection complete! Found {len(anomalies)} anomalies.")
    
    with col3:
        if 'anomaly_results' in st.session_state and st.session_state.anomaly_results:
            if st.button("🗑️ Clear Results", key="clear_anomaly_results", use_container_width=True):
                st.session_state.anomaly_results = []
                st.session_state.anomaly_timestamp = None
                st.session_state.anomaly_detection_run = False
                st.rerun()
    
    st.divider()
    
    # ========================================================================
    # RESULTS DISPLAY
    # ========================================================================
    # FIXED: Check if we have results to display
    has_results = (
        'anomaly_results' in st.session_state and 
        st.session_state.anomaly_results is not None and
        len(st.session_state.anomaly_results) > 0
    )
    
    if has_results:
        render_anomaly_results()
    else:
        # Check if detection was run but no anomalies found
        if 'anomaly_detection_run' in st.session_state and st.session_state.anomaly_detection_run:
            st.info("🎉 No anomalies detected! All contracts appear consistent.")
        else:
            render_anomaly_intro()


def render_premium_card(icon: str, label: str, value: str, color: str):
    """Render a premium card similar to dashboard"""
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['white']};
        border-radius: 16px;
        padding: 18px 20px;
        border-left: 5px solid {color};
        box-shadow: 0 2px 12px rgba(10, 38, 71, 0.06);
        transition: all 0.3s ease;
        height: 100%;
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 28px;">{icon}</span>
            <div>
                <div style="font-size: 26px; font-weight: 700; color: {COLORS['primary']['deepest_navy']}; line-height: 1.2;">
                    {value}
                </div>
                <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']}; margin-top: 2px;">
                    {label}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def detect_comprehensive_anomalies() -> List[Dict[str, Any]]:
    """
    Detect anomalies across multiple dimensions - PREMIUM ENHANCED
    
    Returns:
        List of anomaly dictionaries with comprehensive details
    """
    anomalies = []
    contracts = st.session_state.contracts
    
    if len(contracts) < 2:
        return [{
            'type': 'Insufficient Data',
            'contract': 'N/A',
            'severity': 'info',
            'description': 'Need at least 2 contracts for anomaly detection',
            'details': f'Currently have {len(contracts)} contract(s). Upload more contracts for better analysis.',
            'recommendation': 'Upload at least 2-3 contracts to enable anomaly detection',
            'metric': f'{len(contracts)} contracts',
            'baseline': '2+ contracts recommended'
        }]
    
    # ========================================================================
    # 1. PAYMENT TERMS ANOMALY DETECTION
    # ========================================================================
    payment_anomalies = detect_payment_term_anomalies(contracts)
    anomalies.extend(payment_anomalies)
    
    # ========================================================================
    # 2. LIABILITY CAP ANOMALY DETECTION
    # ========================================================================
    liability_anomalies = detect_liability_cap_anomalies(contracts)
    anomalies.extend(liability_anomalies)
    
    # ========================================================================
    # 3. GOVERNING LAW ANOMALY DETECTION
    # ========================================================================
    law_anomalies = detect_governing_law_anomalies(contracts)
    anomalies.extend(law_anomalies)
    
    # ========================================================================
    # 4. CLAUSE COVERAGE ANOMALY DETECTION
    # ========================================================================
    coverage_anomalies = detect_clause_coverage_anomalies(contracts)
    anomalies.extend(coverage_anomalies)
    
    # ========================================================================
    # 5. RISK DENSITY ANOMALY DETECTION
    # ========================================================================
    risk_density_anomalies = detect_risk_density_anomalies(contracts)
    anomalies.extend(risk_density_anomalies)
    
    # ========================================================================
    # 6. CONTRACT LENGTH ANOMALY DETECTION
    # ========================================================================
    length_anomalies = detect_contract_length_anomalies(contracts)
    anomalies.extend(length_anomalies)
    
    # Sort anomalies by severity (critical first, then high, medium, low)
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
    anomalies.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 5))
    
    return anomalies


def detect_payment_term_anomalies(contracts: List[Contract]) -> List[Dict[str, Any]]:
    """Detect unusual payment terms using statistical analysis"""
    anomalies = []
    payment_terms = []
    contract_payment = {}
    
    for contract in contracts:
        matches = re.findall(r'(\d+)\s*(?:days|day)', contract.text, re.IGNORECASE)
        if matches:
            try:
                term = int(matches[0])
                # Only consider reasonable payment terms (1-180 days)
                if 1 <= term <= 180:
                    payment_terms.append(term)
                    contract_payment[contract.name] = term
            except ValueError:
                continue
    
    if len(payment_terms) >= 2:
        avg = sum(payment_terms) / len(payment_terms)
        std = (sum((x - avg) ** 2 for x in payment_terms) / len(payment_terms)) ** 0.5
        
        # Identify anomalies (more than 1.5 standard deviations)
        for contract_name, term in contract_payment.items():
            if std > 0:
                deviation = abs(term - avg)
                z_score = deviation / std
                
                if z_score > 1.5:
                    # Determine severity based on deviation
                    if z_score > 3.0:
                        severity = 'critical'
                        description = f"Extreme outlier: {term} days (3+ standard deviations from avg {avg:.0f} days)"
                    elif z_score > 2.0:
                        severity = 'high'
                        description = f"Significant outlier: {term} days (2+ standard deviations from avg {avg:.0f} days)"
                    else:
                        severity = 'medium'
                        description = f"Moderate outlier: {term} days ({z_score:.1f} std dev from avg {avg:.0f} days)"
                    
                    anomalies.append({
                        'type': 'Unusual Payment Term',
                        'contract': contract_name,
                        'severity': severity,
                        'description': description,
                        'details': f"Average: {avg:.0f} days | This contract: {term} days | Deviation: {deviation:.0f} days | Z-Score: {z_score:.2f}",
                        'recommendation': f'Review payment terms and consider standardizing to {avg:.0f} days' if term < avg else f'Review payment terms - unusually long payment period of {term} days',
                        'metric': f'{term} days',
                        'baseline': f'{avg:.0f} days (avg)'
                    })
    
    return anomalies


def detect_liability_cap_anomalies(contracts: List[Contract]) -> List[Dict[str, Any]]:
    """Detect unusual liability caps using statistical analysis"""
    anomalies = []
    caps = []
    contract_caps = {}
    
    for contract in contracts:
        # Find dollar amounts with liability indicators
        patterns = [
            r'\$\s*([\d,]+\.?\d*)\s*(?:million|M|m)',
            r'\$\s*([\d,]+\.?\d*)\s*(?:billion|B|b)',
            r'\$\s*([\d,]+\.?\d*)\s*(?:thousand|K|k)',
            r'\$\s*([\d,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, contract.text, re.IGNORECASE)
            if matches:
                try:
                    cap_str = matches[0].replace(',', '')
                    cap = float(cap_str)
                    
                    # Convert to standard units
                    if 'million' in pattern.lower() or 'm' in pattern.lower():
                        cap = cap * 1000000
                    elif 'billion' in pattern.lower() or 'b' in pattern.lower():
                        cap = cap * 1000000000
                    elif 'thousand' in pattern.lower() or 'k' in pattern.lower():
                        cap = cap * 1000
                    
                    # Only consider reasonable caps (>= $10,000)
                    if cap >= 10000:
                        caps.append(cap)
                        contract_caps[contract.name] = cap
                        break
                except:
                    continue
    
    if len(caps) >= 2:
        avg = sum(caps) / len(caps)
        std = (sum((x - avg) ** 2 for x in caps) / len(caps)) ** 0.5
        
        for contract_name, cap in contract_caps.items():
            if std > 0:
                deviation = abs(cap - avg)
                z_score = deviation / std
                
                if z_score > 1.5:
                    if z_score > 3.0:
                        severity = 'critical'
                        description = f"Extreme outlier: ${cap:,.0f} (3+ standard deviations from avg ${avg:,.0f})"
                    elif z_score > 2.0:
                        severity = 'high'
                        description = f"Significant outlier: ${cap:,.0f} (2+ standard deviations from avg ${avg:,.0f})"
                    else:
                        severity = 'medium'
                        description = f"Moderate outlier: ${cap:,.0f} ({z_score:.1f} std dev from avg ${avg:,.0f})"
                    
                    anomalies.append({
                        'type': 'Unusual Liability Cap',
                        'contract': contract_name,
                        'severity': severity,
                        'description': description,
                        'details': f"Average: ${avg:,.0f} | This contract: ${cap:,.0f} | Deviation: ${deviation:,.0f} | Z-Score: {z_score:.2f}",
                        'recommendation': f'Review liability cap - {cap:,.0f} is unusual compared to average ${avg:,.0f}',
                        'metric': f'${cap:,.0f}',
                        'baseline': f'${avg:,.0f} (avg)'
                    })
    
    return anomalies


def detect_governing_law_anomalies(contracts: List[Contract]) -> List[Dict[str, Any]]:
    """Detect uncommon governing law choices"""
    anomalies = []
    laws = []
    contract_law = {}
    
    common_laws = {'california', 'new york', 'delaware', 'texas', 'florida', 'illinois'}
    
    for contract in contracts:
        # Extract governing law
        match = re.search(r'(?:governing law|choice of law)[\s\S]{0,200}?(?:california|new york|delaware|texas|florida|illinois|pennsylvania|ohio|georgia|north carolina|michigan|new jersey|virginia|washington|massachusetts|arizona|tennessee|indiana|missouri|maryland|wisconsin|colorado|minnesota|south carolina|alabama|louisiana|kentucky|oregon|oklahoma|connecticut|iowa|mississippi|arkansas|kansas|utah|nevada)', contract.text, re.IGNORECASE)
        
        if match:
            law = match.group(0).lower()
            # Extract state name
            state_match = re.search(r'(california|new york|delaware|texas|florida|illinois|pennsylvania|ohio|georgia|north carolina|michigan|new jersey|virginia|washington|massachusetts|arizona|tennessee|indiana|missouri|maryland|wisconsin|colorado|minnesota|south carolina|alabama|louisiana|kentucky|oregon|oklahoma|connecticut|iowa|mississippi|arkansas|kansas|utah|nevada)', law)
            if state_match:
                state = state_match.group(1).lower()
                laws.append(state)
                contract_law[contract.name] = state
    
    if len(laws) >= 2:
        law_counts = Counter(laws)
        most_common = law_counts.most_common(1)[0][0] if law_counts else None
        
        for contract_name, state in contract_law.items():
            if state not in common_laws:
                anomalies.append({
                    'type': 'Uncommon Governing Law',
                    'contract': contract_name,
                    'severity': 'medium',
                    'description': f"Governing law '{state.title()}' is uncommon in your contract portfolio",
                    'details': f"State: {state.title()} | Most common: {most_common.title() if most_common else 'Unknown'}",
                    'recommendation': f'Consider whether {state.title()} law is appropriate for your business needs',
                    'metric': state.title(),
                    'baseline': f'{most_common.title() if most_common else "Unknown"} (most common)'
                })
    
    return anomalies


def detect_clause_coverage_anomalies(contracts: List[Contract]) -> List[Dict[str, Any]]:
    """Detect contracts with unusual clause coverage (too few or too many)"""
    anomalies = []
    
    for contract in contracts:
        clause_count = contract.clause_count
        if clause_count == 0:
            anomalies.append({
                'type': 'Missing Clauses',
                'contract': contract.name,
                'severity': 'high',
                'description': f'No clauses extracted from {contract.name}',
                'details': 'The contract appears to have no detectable clauses',
                'recommendation': 'Check if the contract is properly formatted or contains the expected clauses',
                'metric': '0 clauses',
                'baseline': 'Expected 3+ clauses'
            })
    
    # Calculate average clauses per contract (excluding contracts with 0 clauses)
    all_clause_counts = [c.clause_count for c in contracts if c.clause_count > 0]
    if all_clause_counts:
        avg_clauses = sum(all_clause_counts) / len(all_clause_counts) if all_clause_counts else 0
        
        for contract in contracts:
            if contract.clause_count > 0 and contract.clause_count > avg_clauses * 2:
                anomalies.append({
                    'type': 'Excessive Clauses',
                    'contract': contract.name,
                    'severity': 'medium',
                    'description': f'Unusually high clause count: {contract.clause_count} (Avg: {avg_clauses:.1f})',
                    'details': f'This contract has more than double the average number of clauses',
                    'recommendation': 'Review if all clauses are correctly identified or if this contract is unusually complex',
                    'metric': f'{contract.clause_count} clauses',
                    'baseline': f'{avg_clauses:.1f} avg'
                })
    
    return anomalies


def detect_risk_density_anomalies(contracts: List[Contract]) -> List[Dict[str, Any]]:
    """Detect contracts with unusually high risk density"""
    anomalies = []
    
    # Calculate risk density for each contract
    risk_densities = []
    contract_density = {}
    
    for contract in contracts:
        if contract.word_count > 0:
            density = (contract.risk_count / contract.word_count) * 1000
            risk_densities.append(density)
            contract_density[contract.name] = density
    
    if len(risk_densities) >= 2:
        avg = sum(risk_densities) / len(risk_densities) if risk_densities else 0
        std = (sum((x - avg) ** 2 for x in risk_densities) / len(risk_densities)) ** 0.5 if risk_densities else 0
        
        for contract_name, density in contract_density.items():
            if std > 0 and density > avg + std * 1.5:
                if density > avg + std * 2.5:
                    severity = 'high'
                else:
                    severity = 'medium'
                
                anomalies.append({
                    'type': 'High Risk Density',
                    'contract': contract_name,
                    'severity': severity,
                    'description': f'Unusually high risk density: {density:.2f} risks per 1000 words (Avg: {avg:.2f})',
                    'details': f'This contract has significantly more risks per word than average',
                    'recommendation': 'Review this contract thoroughly - it contains an unusual concentration of risks',
                    'metric': f'{density:.2f} risks/1000 words',
                    'baseline': f'{avg:.2f} avg'
                })
    
    return anomalies


def detect_contract_length_anomalies(contracts: List[Contract]) -> List[Dict[str, Any]]:
    """Detect contracts with unusual length (too short or too long)"""
    anomalies = []
    
    lengths = [c.word_count for c in contracts if c.word_count > 0]
    if len(lengths) >= 2:
        avg = sum(lengths) / len(lengths) if lengths else 0
        std = (sum((x - avg) ** 2 for x in lengths) / len(lengths)) ** 0.5 if lengths else 0
        
        for contract in contracts:
            if contract.word_count > 0 and std > 0:
                z_score = abs(contract.word_count - avg) / std
                
                if z_score > 2.0:
                    if contract.word_count > avg:
                        severity = 'low'
                        description = f'Unusually long contract: {contract.word_count} words (Avg: {avg:.0f})'
                        recommendation = 'Consider if this contract is unusually detailed or contains excessive boilerplate'
                    else:
                        severity = 'medium'
                        description = f'Unusually short contract: {contract.word_count} words (Avg: {avg:.0f})'
                        recommendation = 'Review contract completeness - may be missing standard provisions'
                    
                    anomalies.append({
                        'type': 'Contract Length Anomaly',
                        'contract': contract.name,
                        'severity': severity,
                        'description': description,
                        'details': f'Average: {avg:.0f} words | This contract: {contract.word_count} words | Z-Score: {z_score:.2f}',
                        'recommendation': recommendation,
                        'metric': f'{contract.word_count} words',
                        'baseline': f'{avg:.0f} avg'
                    })
    
    return anomalies


def render_anomaly_results():
    """Render premium anomaly results dashboard"""
    anomalies = st.session_state.anomaly_results
    timestamp = st.session_state.get('anomaly_timestamp', datetime.now())
    
    if not anomalies:
        st.info("🎉 No anomalies detected! All contracts appear consistent.")
        return
    
    # ========================================================================
    # ANOMALY SUMMARY CARDS
    # ========================================================================
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
    for anomaly in anomalies:
        severity = anomaly.get('severity', 'low')
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    total_anomalies = len(anomalies)
    
    st.markdown("### 📊 Anomaly Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_anomaly_metric("🔴", "Critical", severity_counts['critical'], COLORS['semantic']['danger'])
    with col2:
        render_anomaly_metric("🟠", "High", severity_counts['high'], COLORS['semantic']['warning'])
    with col3:
        render_anomaly_metric("🟡", "Medium", severity_counts['medium'], COLORS['semantic']['warning'])
    with col4:
        render_anomaly_metric("🔵", "Low", severity_counts['low'], COLORS['semantic']['info'])
    with col5:
        render_anomaly_metric("📊", "Total", total_anomalies, COLORS['primary']['corporate_blue'])
    
    st.divider()
    
    # ========================================================================
    # ANOMALY TYPE DISTRIBUTION CHART
    # ========================================================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Anomaly Distribution")
        type_counts = Counter([a.get('type', 'Unknown') for a in anomalies])
        if type_counts:
            df = pd.DataFrame({
                'Anomaly Type': list(type_counts.keys()),
                'Count': list(type_counts.values())
            })
            fig = px.bar(
                df,
                x='Count',
                y='Anomaly Type',
                title='Anomaly Types Distribution',
                orientation='h',
                color='Count',
                color_continuous_scale='Blues',
                text='Count'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=COLORS['neutrals']['dark_gray'],
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                coloraxis_showscale=False
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="anomaly_distribution_chart")
    
    with col2:
        st.markdown("### 📋 Quick Stats")
        anomaly_types = list(type_counts.keys())
        if anomaly_types:
            for atype in anomaly_types[:5]:
                st.markdown(f"""
                <div style="
                    background: {COLORS['neutrals']['off_white']};
                    padding: 8px 12px;
                    border-radius: 8px;
                    margin-bottom: 6px;
                    border-left: 3px solid {COLORS['primary']['corporate_blue']};
                ">
                    <span style="font-weight: 500; color: {COLORS['primary']['deepest_navy']};">{atype}</span>
                    <span style="float: right; color: {COLORS['neutrals']['dark_gray']};">{type_counts[atype]}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Last updated
        st.caption(f"🕐 Last updated: {timestamp.strftime('%Y-%m-%d %H:%M')}")
    
    st.divider()
    
    # ========================================================================
    # SEVERITY DISTRIBUTION CHART (PIE)
    # ========================================================================
    st.markdown("### 🎯 Severity Distribution")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        severity_data = [
            ('Critical', severity_counts['critical']),
            ('High', severity_counts['high']),
            ('Medium', severity_counts['medium']),
            ('Low', severity_counts['low'])
        ]
        severity_df = pd.DataFrame(severity_data, columns=['Severity', 'Count'])
        severity_df = severity_df[severity_df['Count'] > 0]
        
        if not severity_df.empty:
            color_map = {
                'Critical': COLORS['semantic']['danger'],
                'High': COLORS['semantic']['warning'],
                'Medium': '#D97706',
                'Low': COLORS['semantic']['info']
            }
            
            fig = px.pie(
                severity_df,
                values='Count',
                names='Severity',
                title='Anomaly Severity Breakdown',
                color='Severity',
                color_discrete_map=color_map
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=COLORS['neutrals']['dark_gray'],
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True, key="severity_pie_chart")
    
    with col2:
        st.markdown("### 🏷️ Top Anomalies by Contract")
        contract_counts = Counter([a.get('contract', 'Unknown') for a in anomalies])
        top_contracts = contract_counts.most_common(5)
        
        if top_contracts:
            for contract_name, count in top_contracts:
                st.markdown(f"""
                <div style="
                    background: {COLORS['neutrals']['white']};
                    padding: 10px 14px;
                    border-radius: 8px;
                    margin-bottom: 6px;
                    box-shadow: 0 1px 4px rgba(10, 38, 71, 0.05);
                    border-left: 3px solid {COLORS['semantic']['warning']};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 500; color: {COLORS['primary']['deepest_navy']}; font-size: 13px;">
                            {contract_name[:30]}{'...' if len(contract_name) > 30 else ''}
                        </span>
                        <span style="
                            background: {COLORS['primary']['ice_blue']};
                            padding: 2px 10px;
                            border-radius: 12px;
                            font-size: 12px;
                            color: {COLORS['primary']['corporate_blue']};
                            font-weight: 600;
                        ">{count}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========================================================================
    # FILTERED ANOMALY LIST
    # ========================================================================
    st.markdown("### 📋 Detailed Anomaly Findings")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        anomaly_types = ["All"] + sorted(list(set([a.get('type', 'Unknown') for a in anomalies])))
        selected_type = st.selectbox("Filter by Anomaly Type", options=anomaly_types, key="anomaly_type_filter")
    
    with col2:
        severity_options = ["All", "critical", "high", "medium", "low", "info"]
        selected_severity = st.selectbox("Filter by Severity", options=severity_options, key="anomaly_severity_filter")
    
    # Apply filters
    filtered_anomalies = anomalies.copy()
    
    if selected_type != "All":
        filtered_anomalies = [a for a in filtered_anomalies if a.get('type') == selected_type]
    
    if selected_severity != "All":
        filtered_anomalies = [a for a in filtered_anomalies if a.get('severity') == selected_severity]
    
    st.caption(f"Showing {len(filtered_anomalies)} of {len(anomalies)} anomalies")
    
    # Display filtered anomalies
    if filtered_anomalies:
        for anomaly in filtered_anomalies:
            render_anomaly_card(anomaly)
    else:
        st.info("No anomalies match your filters. Try adjusting your filter criteria.")
    
    # ========================================================================
    # EXPORT SECTION
    # ========================================================================
    st.divider()
    st.markdown("### 📥 Export Results")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📊 Export as CSV", key="export_anomaly_csv", use_container_width=True):
            export_anomalies_csv(anomalies)
    
    with col2:
        if st.button("📋 Export as JSON", key="export_anomaly_json", use_container_width=True):
            export_anomalies_json(anomalies)
    
    with col3:
        if st.button("📄 Generate Report", key="export_anomaly_report", use_container_width=True):
            st.info("📄 Report generation coming soon!")


def render_anomaly_metric(icon: str, label: str, value: int, color: str):
    """Render a small anomaly metric card"""
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['white']};
        border-radius: 12px;
        padding: 14px 16px;
        text-align: center;
        border-top: 3px solid {color};
        box-shadow: 0 1px 4px rgba(10, 38, 71, 0.05);
        height: 100%;
    ">
        <span style="font-size: 22px;">{icon}</span>
        <div style="font-size: 24px; font-weight: 700; color: {color}; line-height: 1.2;">
            {value}
        </div>
        <div style="font-size: 12px; color: {COLORS['neutrals']['dark_gray']}; margin-top: 2px;">
            {label}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_anomaly_card(anomaly: Dict[str, Any]):
    """Render a premium anomaly card with details"""
    severity = anomaly.get('severity', 'low')
    severity_colors = {
        'critical': {'bg': '#FEE2E2', 'color': '#DC2626', 'border': '#DC2626'},
        'high': {'bg': '#FEF3C7', 'color': '#D97706', 'border': '#D97706'},
        'medium': {'bg': '#FEF3C7', 'color': '#D97706', 'border': '#D97706'},
        'low': {'bg': '#EFF6FF', 'color': '#3B82F6', 'border': '#3B82F6'},
        'info': {'bg': '#F8FAFE', 'color': '#475569', 'border': '#94A3B8'}
    }
    colors = severity_colors.get(severity, severity_colors['info'])
    
    severity_label = severity.upper() if severity != 'info' else 'INFO'
    
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['white']};
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 6px solid {colors['border']};
        box-shadow: 0 2px 8px rgba(10, 38, 71, 0.06);
        transition: all 0.3s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 8px;">
            <div style="flex: 1; min-width: 200px;">
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                    <span style="
                        background: {colors['bg']};
                        color: {colors['color']};
                        padding: 2px 12px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: 700;
                        letter-spacing: 0.3px;
                    ">{severity_label}</span>
                    <span style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; font-size: 15px;">
                        {anomaly.get('type', 'Unknown')}
                    </span>
                    <span style="color: {COLORS['neutrals']['medium_gray']}; font-size: 13px;">
                        📄 {anomaly.get('contract', 'N/A')}
                    </span>
                </div>
                <div style="margin-top: 6px; color: {COLORS['neutrals']['dark_gray']}; font-size: 14px; line-height: 1.5;">
                    {anomaly.get('description', 'No description')}
                </div>
            </div>
            <div style="text-align: right; min-width: 120px;">
                <div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']};">
                    Metric
                </div>
                <div style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; font-size: 14px;">
                    {anomaly.get('metric', 'N/A')}
                </div>
                <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']};">
                    Baseline: {anomaly.get('baseline', 'N/A')}
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid {COLORS['neutrals']['light_gray']};">
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']};">
                <strong>Details:</strong> {anomaly.get('details', 'No details available')}
            </div>
            <div style="font-size: 13px; color: {COLORS['primary']['corporate_blue']}; margin-top: 4px;">
                💡 <strong>Recommendation:</strong> {anomaly.get('recommendation', 'Review this anomaly')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_anomaly_intro():
    """Render introductory content when no detection has been run"""
    st.markdown("### 🔍 Ready to Detect Anomalies")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['off_white']};
            padding: 20px 24px;
            border-radius: 16px;
            border: 1px solid {COLORS['neutrals']['light_gray']};
        ">
            <h4 style="color: {COLORS['primary']['deepest_navy']}; margin: 0 0 12px 0;">📊 What We'll Analyze</h4>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="padding: 6px 0; border-bottom: 1px solid {COLORS['neutrals']['light_gray']};">
                    <span style="font-weight: 500;">💰 Payment Terms</span> - Unusual payment periods
                </li>
                <li style="padding: 6px 0; border-bottom: 1px solid {COLORS['neutrals']['light_gray']};">
                    <span style="font-weight: 500;">🛡️ Liability Caps</span> - Outlier liability limits
                </li>
                <li style="padding: 6px 0; border-bottom: 1px solid {COLORS['neutrals']['light_gray']};">
                    <span style="font-weight: 500;">⚖️ Governing Law</span> - Uncommon jurisdictions
                </li>
                <li style="padding: 6px 0; border-bottom: 1px solid {COLORS['neutrals']['light_gray']};">
                    <span style="font-weight: 500;">📋 Clause Coverage</span> - Missing or excessive clauses
                </li>
                <li style="padding: 6px 0; border-bottom: 1px solid {COLORS['neutrals']['light_gray']};">
                    <span style="font-weight: 500;">⚠️ Risk Density</span> - Unusual risk concentration
                </li>
                <li style="padding: 6px 0;">
                    <span style="font-weight: 500;">📄 Contract Length</span> - Unusually short/long contracts
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            padding: 20px 24px;
            border-radius: 16px;
            border: 1px solid {COLORS['neutrals']['light_gray']};
            text-align: center;
        ">
            <span style="font-size: 48px;">🚀</span>
            <h4 style="color: {COLORS['primary']['deepest_navy']}; margin: 8px 0 4px 0;">Get Started</h4>
            <p style="color: {COLORS['neutrals']['dark_gray']}; font-size: 14px; margin: 0 0 12px 0;">
                Click the button below to analyze<br>
                <strong>{len(st.session_state.contracts)}</strong> contracts for anomalies
            </p>
            <div style="
                background: {COLORS['semantic']['info_bg']};
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 13px;
                color: {COLORS['semantic']['info']};
            ">
                ⚡ Detects 6+ types of anomalies
            </div>
        </div>
        """, unsafe_allow_html=True)


def export_anomalies_csv(anomalies: List[Dict[str, Any]]):
    """Export anomalies to CSV"""
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Type', 'Contract', 'Severity', 'Description', 'Details', 'Recommendation', 'Metric', 'Baseline'])
    
    # Write data
    for anomaly in anomalies:
        writer.writerow([
            anomaly.get('type', ''),
            anomaly.get('contract', ''),
            anomaly.get('severity', ''),
            anomaly.get('description', ''),
            anomaly.get('details', ''),
            anomaly.get('recommendation', ''),
            anomaly.get('metric', ''),
            anomaly.get('baseline', '')
        ])
    
    csv_data = output.getvalue()
    
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"anomaly_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        key="download_anomaly_csv"
    )


def export_anomalies_json(anomalies: List[Dict[str, Any]]):
    """Export anomalies to JSON"""
    import json
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'total_anomalies': len(anomalies),
        'contracts_analyzed': len(st.session_state.contracts),
        'anomalies': anomalies
    }
    
    json_data = json.dumps(export_data, indent=2)
    
    st.download_button(
        label="📥 Download JSON",
        data=json_data,
        file_name=f"anomaly_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        key="download_anomaly_json"
    )