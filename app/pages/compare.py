"""
KontractIQ - Compare Page
contract comparison with premium UI/UX
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from ..core.comparator import ContractComparator
from ..utils.constants import COLORS, BORDER_RADIUS, SHADOWS, SPACING
from ..models.contract import Contract


def render_compare():
    """Render the enhanced compare page with premium UI/UX"""
    
    # ========================================================================
    # PAGE HEADER WITH PREMIUM CARD
    # ========================================================================
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
        border-radius: {BORDER_RADIUS['xxl']}px;
        padding: {SPACING['xxxl']}px {SPACING['xxxl']}px;
        margin-bottom: {SPACING['xxl']}px;
        color: white;
        box-shadow: {SHADOWS['xl']};
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
            <div>
                <div style="display: flex; align-items: center; gap: {SPACING['md']}px;">
                    <span style="font-size: 36px;">📊</span>
                    <h1 style="font-size: 28px; font-weight: 700; margin: 0; color: white;">
                        KontractIQ Compare
                    </h1>
                </div>
                <p style="font-size: 16px; opacity: 0.9; margin: {SPACING['sm']}px 0 0 0;">
                    Intelligent version-to-version contract comparison with visual diff highlighting
                </p>
            </div>
            <div style="
                background: rgba(255,255,255,0.15);
                border-radius: {BORDER_RADIUS['lg']}px;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
            ">
                <span style="font-size: 14px;">⚡ Enterprise Grade</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # PREMIUM METRICS CARDS (Like Dashboard)
    # ========================================================================
    
    total_contracts = len(st.session_state.contracts)
    
    # Use st.columns with proper gap
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        render_premium_metric_card(
            "📄",
            "Total Contracts",
            str(total_contracts),
            "Available for comparison",
            COLORS['primary']['corporate_blue']
        )
    
    with col2:
        render_premium_metric_card(
            "🔄",
            "Comparable Pairs",
            str(total_contracts * (total_contracts - 1) // 2 if total_contracts >= 2 else 0),
            "Unique combinations",
            COLORS['semantic']['success']
        )
    
    with col3:
        render_premium_metric_card(
            "⚡",
            "Ready to Compare",
            "✅" if total_contracts >= 2 else "❌",
            f"{'Ready' if total_contracts >= 2 else 'Upload at least 2 contracts'}",
            COLORS['semantic']['success'] if total_contracts >= 2 else COLORS['semantic']['warning']
        )
    
    with col4:
        render_premium_metric_card(
            "📈",
            "Health Impact",
            "Smart Analysis",
            "AI-powered comparison",
            COLORS['semantic']['info']
        )
    
    st.divider()
    
    # ========================================================================
    # QUICK START INSTRUCTIONS - PREMIUM REDESIGNED
    # ========================================================================
    
    with st.expander("📖 How to Use Compare - Quick Start Guide", expanded=False):
        # Header with gradient
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0A2647 0%, #1B3A5C 100%);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 20px;
            color: white;
        ">
            <h4 style="margin: 0; font-size: 20px;">🚀 Get Started in 3 Easy Steps</h4>
            <p style="margin: 4px 0 0 0; opacity: 0.8; font-size: 14px;">Follow these simple steps to compare your contracts</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step cards with proper spacing - using 3 columns
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 4px 16px rgba(10, 38, 71, 0.08);
                border-top: 4px solid #2C5F8A;
                height: 100%;
                transition: transform 0.2s ease;
            ">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <div style="
                        background: linear-gradient(135deg, #2C5F8A, #4A7FA5);
                        color: white;
                        border-radius: 50%;
                        width: 36px;
                        height: 36px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        font-size: 16px;
                        flex-shrink: 0;
                    ">1</div>
                    <span style="font-size: 16px; font-weight: 600; color: #0A2647;">Select Versions</span>
                </div>
                <p style="color: #475569; font-size: 14px; margin: 8px 0 0 0; line-height: 1.5;">
                    Choose two contracts from the dropdowns below. Compare different versions or similar contracts.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 4px 16px rgba(10, 38, 71, 0.08);
                border-top: 4px solid #0D9488;
                height: 100%;
                transition: transform 0.2s ease;
            ">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <div style="
                        background: linear-gradient(135deg, #0D9488, #0A7A70);
                        color: white;
                        border-radius: 50%;
                        width: 36px;
                        height: 36px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        font-size: 16px;
                        flex-shrink: 0;
                    ">2</div>
                    <span style="font-size: 16px; font-weight: 600; color: #0A2647;">Compare</span>
                </div>
                <p style="color: #475569; font-size: 14px; margin: 8px 0 0 0; line-height: 1.5;">
                    Click "Compare Versions" to analyze differences. Our AI will highlight all changes instantly.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 4px 16px rgba(10, 38, 71, 0.08);
                border-top: 4px solid #3B82F6;
                height: 100%;
                transition: transform 0.2s ease;
            ">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <div style="
                        background: linear-gradient(135deg, #3B82F6, #2563EB);
                        color: white;
                        border-radius: 50%;
                        width: 36px;
                        height: 36px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        font-size: 16px;
                        flex-shrink: 0;
                    ">3</div>
                    <span style="font-size: 16px; font-weight: 600; color: #0A2647;">Review & Export</span>
                </div>
                <p style="color: #475569; font-size: 14px; margin: 8px 0 0 0; line-height: 1.5;">
                    Review changes by tab and export your report. Download as Text, CSV, or copy to clipboard.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pro Tip and Badges Section
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #EFF6FF 0%, #E8F1F8 100%);
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 16px;
            border: 1px solid #B8D4E8;
        ">
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">💡</span>
                    <span style="font-size: 14px; color: #1B3A5C;">
                        <strong>Pro Tip:</strong> Compare different versions of the same contract or similar contracts from different vendors.
                    </span>
                </div>
                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-left: auto;">
                    <span style="
                        background: #E6F7F5;
                        color: #0D9488;
                        padding: 4px 14px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 500;
                        border: 1px solid #0D9488;
                    ">✅ Added</span>
                    <span style="
                        background: #FEE2E2;
                        color: #DC2626;
                        padding: 4px 14px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 500;
                        border: 1px solid #DC2626;
                    ">❌ Removed</span>
                    <span style="
                        background: #FEF3C7;
                        color: #D97706;
                        padding: 4px 14px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 500;
                        border: 1px solid #D97706;
                    ">✏️ Modified</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========================================================================
    # MAIN COMPARE INTERFACE
    # ========================================================================
    
    # Check if there are enough contracts
    if len(st.session_state.contracts) < 2:
        st.warning("⚠️ Need at least 2 contracts to compare. Upload more contracts!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Go to Upload", use_container_width=True):
                st.session_state.page = "Upload Contracts"
                st.rerun()
        with col2:
            if st.button("🎯 Load Demo Data", use_container_width=True):
                from ..data.demo_data import load_demo_contracts
                load_demo_contracts()
                st.rerun()
        return
    
    # ========================================================================
    # CONTRACT SELECTION WITH ENHANCED UI
    # ========================================================================
    
    # Check if we have suggestion selections to apply
    if 'suggest_a' in st.session_state and 'suggest_b' in st.session_state:
        suggest_a = st.session_state.suggest_a
        suggest_b = st.session_state.suggest_b
        # Clear the suggestion flags
        del st.session_state.suggest_a
        del st.session_state.suggest_b
    else:
        suggest_a = None
        suggest_b = None
    
    st.markdown("### 🔄 Select Contracts to Compare")
    st.caption("Choose two contract versions for detailed comparison")
    
    contract_options = [c.name for c in st.session_state.contracts]
    
    # Add contract metadata to options with health icons
    contract_display = {}
    for c in st.session_state.contracts:
        health_icon = "✅" if c.overall_health == "healthy" else "⚠️" if c.overall_health == "warning" else "🔴"
        contract_display[c.name] = f"{health_icon} {c.name} ({c.clause_count} clauses, {c.pages} pages)"
    
    # Use two columns with proper spacing
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            border-radius: {BORDER_RADIUS['lg']}px;
            padding: {SPACING['lg']}px;
            border: 2px solid {COLORS['primary']['corporate_blue']};
            box-shadow: {SHADOWS['sm']};
            margin-bottom: {SPACING['md']}px;
        ">
            <div style="display: flex; align-items: center; gap: {SPACING['sm']}px; margin-bottom: {SPACING['sm']}px;">
                <span style="font-size: 20px;">📄</span>
                <span style="font-weight: 600; color: {COLORS['primary']['deepest_navy']};">Version A (Original)</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Use a different key for the selectbox to avoid session state conflicts
        # And set the default value if we have a suggestion
        default_a = suggest_a if suggest_a and suggest_a in contract_options else contract_options[0]
        
        contract_a = st.selectbox(
            "Select Original Version",
            options=contract_options,
            format_func=lambda x: contract_display.get(x, x),
            key="compare_a_select",
            label_visibility="collapsed",
            index=contract_options.index(default_a) if default_a in contract_options else 0
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show selected contract info with proper spacing
        contract_a_obj = next((c for c in st.session_state.contracts if c.name == contract_a), None)
        if contract_a_obj:
            render_contract_mini_info(contract_a_obj, "Version A")
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['white']};
            border-radius: {BORDER_RADIUS['lg']}px;
            padding: {SPACING['lg']}px;
            border: 2px solid {COLORS['semantic']['success']};
            box-shadow: {SHADOWS['sm']};
            margin-bottom: {SPACING['md']}px;
        ">
            <div style="display: flex; align-items: center; gap: {SPACING['sm']}px; margin-bottom: {SPACING['sm']}px;">
                <span style="font-size: 20px;">📄</span>
                <span style="font-weight: 600; color: {COLORS['primary']['deepest_navy']};">Version B (Revised)</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Use a different key for the selectbox to avoid session state conflicts
        default_b = suggest_b if suggest_b and suggest_b in contract_options else contract_options[-1] if len(contract_options) > 1 else contract_options[0]
        
        contract_b = st.selectbox(
            "Select Revised Version",
            options=contract_options,
            format_func=lambda x: contract_display.get(x, x),
            key="compare_b_select",
            label_visibility="collapsed",
            index=contract_options.index(default_b) if default_b in contract_options else (1 if len(contract_options) > 1 else 0)
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        contract_b_obj = next((c for c in st.session_state.contracts if c.name == contract_b), None)
        if contract_b_obj:
            render_contract_mini_info(contract_b_obj, "Version B")
    
    # ========================================================================
    # COMPARE BUTTON WITH PROPER SPACING
    # ========================================================================
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1], gap="medium")
    with col2:
        if st.button("🔄 Compare Versions", key="compare_btn", use_container_width=True, type="primary"):
            if contract_a == contract_b:
                st.warning("⚠️ Please select two different contracts to compare")
            else:
                perform_comparison(contract_a_obj, contract_b_obj)
    
    # ========================================================================
    # SMART SUGGESTIONS
    # ========================================================================
    
    if len(st.session_state.contracts) >= 2:
        st.divider()
        st.markdown("### 💡 Smart Suggestions")
        st.caption("Click a suggestion below to auto-select contracts for comparison")
        
        # Find similar contract names (potential versions)
        contract_names = [c.name for c in st.session_state.contracts]
        suggestions = find_similar_contracts(contract_names)
        
        if suggestions:
            # Use columns with proper spacing
            num_cols = min(len(suggestions), 4)
            cols = st.columns(num_cols, gap="small")
            
            for idx, (name_a, name_b) in enumerate(suggestions[:4]):
                with cols[idx % num_cols]:
                    # Use a different approach - store suggestion in session state and rerun
                    if st.button(f"🔄 {name_a} ↔ {name_b}", key=f"suggest_{idx}", use_container_width=True):
                        # Store the suggestion in session state
                        st.session_state.suggest_a = name_a
                        st.session_state.suggest_b = name_b
                        # Rerun to apply the suggestion
                        st.rerun()
        else:
            st.info("💡 No similar contracts found. Try uploading multiple versions of the same contract.")


# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def render_premium_metric_card(icon: str, label: str, value: str, subtitle: str, color: str):
    """Render a premium metric card with proper spacing"""
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['xl']}px;
        padding: {SPACING['lg']}px {SPACING['lg']}px;
        box-shadow: {SHADOWS['md']};
        border-top: 4px solid {color};
        transition: all 0.3s ease;
        text-align: center;
        margin-bottom: {SPACING['sm']}px;
        height: 100%;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <div style="font-size: 32px; margin-bottom: {SPACING['xs']}px;">{icon}</div>
        <div style="font-size: 24px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{value}</div>
        <div style="font-size: 14px; font-weight: 600; color: {COLORS['neutrals']['dark_gray']};">{label}</div>
        <div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']}; margin-top: {SPACING['xs']}px;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_contract_mini_info(contract, label: str):
    """Render a mini info card for a contract with proper spacing"""
    health_color = {
        'healthy': COLORS['semantic']['success'],
        'warning': COLORS['semantic']['warning'],
        'critical': COLORS['semantic']['danger'],
        'scanned': COLORS['semantic']['info']
    }.get(contract.overall_health, COLORS['neutrals']['medium_gray'])
    
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px {SPACING['lg']}px;
        margin-top: {SPACING['sm']}px;
        border-left: 4px solid {health_color};
        font-size: 13px;
        color: {COLORS['neutrals']['dark_gray']};
        box-shadow: {SHADOWS['sm']};
    ">
        <div style="display: flex; flex-wrap: wrap; gap: {SPACING['md']}px; align-items: center;">
            <span style="display: flex; align-items: center; gap: 4px;">📄 <strong>{contract.pages}</strong> pages</span>
            <span style="display: flex; align-items: center; gap: 4px;">📝 <strong>{contract.clause_count}</strong> clauses</span>
            <span style="display: flex; align-items: center; gap: 4px;">⚠️ <strong>{contract.risk_count}</strong> risks</span>
            <span style="
                background: {health_color}22;
                color: {health_color};
                padding: 2px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            ">{contract.health_label}</span>
        </div>
        <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 6px;">
            📅 Uploaded: {contract.upload_date.strftime('%Y-%m-%d %H:%M')}
        </div>
    </div>
    """, unsafe_allow_html=True)


def find_similar_contracts(contract_names: List[str]) -> List[tuple]:
    """Find similar contract names for smart suggestions"""
    suggestions = []
    
    # Look for similar names (potential versions)
    for i, name_a in enumerate(contract_names):
        for j, name_b in enumerate(contract_names):
            if i >= j:  # Avoid duplicates and self-comparison
                continue
            
            # Remove common extensions and normalize
            clean_a = name_a.replace('.pdf', '').replace('.docx', '').replace('.txt', '').lower()
            clean_b = name_b.replace('.pdf', '').replace('.docx', '').replace('.txt', '').lower()
            
            # Check if names share significant parts
            parts_a = set(clean_a.replace('_', ' ').split())
            parts_b = set(clean_b.replace('_', ' ').split())
            
            common_parts = parts_a & parts_b
            if len(common_parts) >= 2:  # Share at least 2 meaningful words
                suggestions.append((name_a, name_b))
    
    return suggestions[:6]  # Return up to 6 suggestions


def perform_comparison(contract_a: Contract, contract_b: Contract):
    """Perform and display the comparison results"""
    
    # ========================================================================
    # EXECUTE COMPARISON
    # ========================================================================
    
    with st.spinner("🔍 Analyzing contract differences..."):
        comparator = ContractComparator()
        result = comparator.compare(contract_a.text, contract_b.text)
    
    # ========================================================================
    # COMPARISON SUMMARY WITH PREMIUM CARDS
    # ========================================================================
    
    st.divider()
    st.markdown("### 📊 Comparison Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    
    with col1:
        render_comparison_metric(
            "📝",
            "Added",
            str(result['stats']['total_added']),
            "Lines added in new version",
            COLORS['semantic']['success']
        )
    
    with col2:
        render_comparison_metric(
            "🗑️",
            "Removed",
            str(result['stats']['total_removed']),
            "Lines removed in new version",
            COLORS['semantic']['danger']
        )
    
    with col3:
        render_comparison_metric(
            "✏️",
            "Modified",
            str(result['stats']['total_modified']),
            "Lines changed between versions",
            COLORS['semantic']['warning']
        )
    
    with col4:
        similarity = result['stats']['similarity'] * 100
        render_comparison_metric(
            "📊",
            "Similarity",
            f"{similarity:.1f}%",
            "Overall text similarity",
            COLORS['primary']['corporate_blue']
        )
    
    with col5:
        total_changed = result['stats']['total_changed']
        change_type = "Minor" if total_changed < 10 else "Moderate" if total_changed < 50 else "Major"
        change_color = COLORS['semantic']['success'] if total_changed < 10 else COLORS['semantic']['warning'] if total_changed < 50 else COLORS['semantic']['danger']
        render_comparison_metric(
            "🔄",
            "Change Type",
            change_type,
            f"{total_changed} total changes",
            change_color
        )
    
    # ========================================================================
    # VISUAL CHANGE OVERVIEW
    # ========================================================================
    
    st.divider()
    
    # Create a visual representation of changes
    st.markdown("### 📈 Change Visualization")
    
    change_data = {
        "Added": result['stats']['total_added'],
        "Removed": result['stats']['total_removed'],
        "Modified": result['stats']['total_modified']
    }
    
    # Display as bar chart using Streamlit
    chart_df = pd.DataFrame({
        "Change Type": list(change_data.keys()),
        "Count": list(change_data.values())
    })
    
    st.bar_chart(chart_df.set_index("Change Type"))
    
    # ========================================================================
    # DETAILED CHANGES WITH TABS
    # ========================================================================
    
    st.divider()
    st.markdown("### 🔍 Detailed Changes")
    st.caption("Review all changes categorized by type")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📝 Added ({result['stats']['total_added']})",
        f"🗑️ Removed ({result['stats']['total_removed']})",
        f"✏️ Modified ({result['stats']['total_modified']})",
        "📋 Full Comparison"
    ])
    
    with tab1:
        render_added_changes(result['changes']['added'])
    
    with tab2:
        render_removed_changes(result['changes']['removed'])
    
    with tab3:
        render_modified_changes(result['changes']['modified'])
    
    with tab4:
        render_full_comparison(result['changes'], contract_a, contract_b)
    
    # ========================================================================
    # EXPORT OPTIONS
    # ========================================================================
    
    st.divider()
    st.markdown("### 📥 Export Report")
    st.caption("Download the comparison report in various formats")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        if st.button("📄 Export as Text", key="export_text_btn", use_container_width=True):
            report = generate_comparison_report(result, contract_a, contract_b, "text")
            st.download_button(
                label="📥 Download Text Report",
                data=report,
                file_name=f"comparison_{contract_a.name}_{contract_b.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                key="download_text_report",
                use_container_width=True
            )
    
    with col2:
        if st.button("📊 Export as CSV", key="export_csv_btn", use_container_width=True):
            csv_data = generate_comparison_report(result, contract_a, contract_b, "csv")
            st.download_button(
                label="📥 Download CSV Report",
                data=csv_data,
                file_name=f"comparison_{contract_a.name}_{contract_b.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key="download_csv_report",
                use_container_width=True
            )
    
    with col3:
        if st.button("📋 Copy to Clipboard", key="copy_btn", use_container_width=True):
            report = generate_comparison_report(result, contract_a, contract_b, "text")
            st.code(report, language="text")
            st.success("✅ Report copied! You can now copy it from the code block above.")


def render_comparison_metric(icon: str, label: str, value: str, subtitle: str, color: str):
    """Render a comparison metric card with proper spacing"""
    st.markdown(f"""
    <div style="
        background: {COLORS['neutrals']['white']};
        border-radius: {BORDER_RADIUS['md']}px;
        padding: {SPACING['md']}px {SPACING['lg']}px;
        box-shadow: {SHADOWS['sm']};
        text-align: center;
        border-bottom: 3px solid {color};
        margin-bottom: {SPACING['sm']}px;
        height: 100%;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <div style="font-size: 24px;">{icon}</div>
        <div style="font-size: 22px; font-weight: 700; color: {COLORS['primary']['deepest_navy']};">{value}</div>
        <div style="font-size: 13px; font-weight: 600; color: {COLORS['neutrals']['dark_gray']};">{label}</div>
        <div style="font-size: 11px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 2px;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_added_changes(added_lines: List[dict]):
    """Render added changes with count and preview"""
    if not added_lines:
        st.info("✅ No lines were added in this version")
        return
    
    total_added = len(added_lines)
    st.markdown(f"**{total_added} lines added**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_lines = added_lines[:100]
    for added in display_lines:
        line = added.get('line', '') if isinstance(added, dict) else str(added)
        st.markdown(f"""
        <div style="
            background: {COLORS['semantic']['success_bg']}; 
            padding: 6px 12px; 
            margin: 3px 0; 
            border-radius: 6px; 
            color: {COLORS['semantic']['success_dark']};
            border-left: 3px solid {COLORS['semantic']['success']};
            font-family: monospace;
            font-size: 13px;
        ">
            + {line}
        </div>
        """, unsafe_allow_html=True)
    
    if total_added > 100:
        remaining = total_added - 100
        st.caption(f"... and {remaining} more added lines")


def render_removed_changes(removed_lines: List[dict]):
    """Render removed changes with count and preview"""
    if not removed_lines:
        st.info("✅ No lines were removed in this version")
        return
    
    total_removed = len(removed_lines)
    st.markdown(f"**{total_removed} lines removed**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_lines = removed_lines[:100]
    for removed in display_lines:
        line = removed.get('line', '') if isinstance(removed, dict) else str(removed)
        st.markdown(f"""
        <div style="
            background: {COLORS['semantic']['danger_bg']}; 
            padding: 6px 12px; 
            margin: 3px 0; 
            border-radius: 6px; 
            color: {COLORS['semantic']['danger_dark']};
            text-decoration: line-through;
            border-left: 3px solid {COLORS['semantic']['danger']};
            font-family: monospace;
            font-size: 13px;
        ">
            - {line}
        </div>
        """, unsafe_allow_html=True)
    
    if total_removed > 100:
        remaining = total_removed - 100
        st.caption(f"... and {remaining} more removed lines")


def render_modified_changes(modified_lines: List[dict]):
    """Render modified changes with side-by-side comparison"""
    if not modified_lines:
        st.info("✅ No lines were modified between versions")
        return
    
    total_modified = len(modified_lines)
    st.markdown(f"**{total_modified} lines modified**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_lines = modified_lines[:50]
    for mod in display_lines:
        old_line = mod.get('old', '')
        new_line = mod.get('new', '')
        similarity = mod.get('similarity', 0) * 100
        
        st.markdown(f"""
        <div style="
            background: {COLORS['semantic']['warning_bg']}; 
            padding: 8px 12px; 
            margin: 4px 0; 
            border-radius: 6px; 
            border-left: 3px solid {COLORS['semantic']['warning']};
            font-family: monospace;
            font-size: 13px;
        ">
            <div style="color: {COLORS['semantic']['danger_dark']}; text-decoration: line-through;">
                - {old_line}
            </div>
            <div style="color: {COLORS['semantic']['success_dark']}; margin-top: 4px;">
                + {new_line}
            </div>
            <div style="color: {COLORS['neutrals']['medium_gray']}; font-size: 11px; margin-top: 4px;">
                Similarity: {similarity:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if total_modified > 50:
        remaining = total_modified - 50
        st.caption(f"... and {remaining} more modified lines")


def render_full_comparison(changes: dict, contract_a: Contract, contract_b: Contract):
    """Render full side-by-side comparison"""
    st.markdown("### 📋 Full Comparison")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['off_white']};
            border-radius: {BORDER_RADIUS['md']}px;
            padding: {SPACING['md']}px;
            border-top: 4px solid {COLORS['primary']['corporate_blue']};
            max-height: 450px;
            overflow-y: auto;
        ">
            <div style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin-bottom: 8px; font-size: 15px;">
                📄 {contract_a.name}
                <span style="font-weight: 400; color: {COLORS['neutrals']['medium_gray']}; font-size: 12px; margin-left: 8px;">(Original)</span>
            </div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']}; white-space: pre-wrap; line-height: 1.6;">
                {contract_a.text[:5000]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {COLORS['neutrals']['off_white']};
            border-radius: {BORDER_RADIUS['md']}px;
            padding: {SPACING['md']}px;
            border-top: 4px solid {COLORS['semantic']['success']};
            max-height: 450px;
            overflow-y: auto;
        ">
            <div style="font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin-bottom: 8px; font-size: 15px;">
                📄 {contract_b.name}
                <span style="font-weight: 400; color: {COLORS['neutrals']['medium_gray']}; font-size: 12px; margin-left: 8px;">(Revised)</span>
            </div>
            <div style="font-size: 13px; color: {COLORS['neutrals']['dark_gray']}; white-space: pre-wrap; line-height: 1.6;">
                {contract_b.text[:5000]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if len(contract_a.text) > 5000:
        st.caption("📌 Showing first 5000 characters. Full text available in the original contract view.")


def generate_comparison_report(result: dict, contract_a: Contract, contract_b: Contract, format_type: str = "text") -> str:
    """Generate comparison report in various formats"""
    
    if format_type == "text":
        # Handle added lines
        added_lines = result['changes']['added']
        added_text = ""
        if added_lines:
            added_preview = []
            for line in added_lines[:50]:
                line_text = line.get('line', '') if isinstance(line, dict) else str(line)
                added_preview.append("+ " + line_text)
            added_text = "\n".join(added_preview)
            if len(added_lines) > 50:
                remaining = len(added_lines) - 50
                added_text += f"\n... and {remaining} more"
        
        # Handle removed lines
        removed_lines = result['changes']['removed']
        removed_text = ""
        if removed_lines:
            removed_preview = []
            for line in removed_lines[:50]:
                line_text = line.get('line', '') if isinstance(line, dict) else str(line)
                removed_preview.append("- " + line_text)
            removed_text = "\n".join(removed_preview)
            if len(removed_lines) > 50:
                remaining = len(removed_lines) - 50
                removed_text += f"\n... and {remaining} more"
        
        # Handle modified lines
        modified_lines = result['changes']['modified']
        modified_text = ""
        if modified_lines:
            modified_preview = []
            for mod in modified_lines[:20]:
                modified_preview.append("- " + mod.get('old', ''))
                modified_preview.append("+ " + mod.get('new', ''))
            modified_text = "\n".join(modified_preview)
            if len(modified_lines) > 20:
                remaining = len(modified_lines) - 20
                modified_text += f"\n... and {remaining} more"
        
        report = f"""
KONTRACTIQ COMPARISON REPORT
============================

CONTRACT INFORMATION
-------------------
Version A (Original): {contract_a.name}
  - Pages: {contract_a.pages}
  - Clauses: {contract_a.clause_count}
  - Risks: {contract_a.risk_count}
  - Health: {contract_a.health_label}

Version B (Revised): {contract_b.name}
  - Pages: {contract_b.pages}
  - Clauses: {contract_b.clause_count}
  - Risks: {contract_b.risk_count}
  - Health: {contract_b.health_label}

COMPARISON SUMMARY
------------------
Added Lines: {result['stats']['total_added']}
Removed Lines: {result['stats']['total_removed']}
Modified Lines: {result['stats']['total_modified']}
Total Changes: {result['stats']['total_changed']}
Similarity: {result['stats']['similarity'] * 100:.1f}%

CHANGE DETAILS
--------------
ADDED LINES ({len(added_lines)}):
{added_text}

REMOVED LINES ({len(removed_lines)}):
{removed_text}

MODIFIED LINES ({len(modified_lines)}):
{modified_text}

RECOMMENDATIONS
---------------
{generate_recommendations(result, contract_a, contract_b)}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
© {datetime.now().year} KontractIQ - Intelligence for every clause.
"""
        return report
    
    elif format_type == "csv":
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Change Type', 'Line'])
        
        # Write added lines
        for line in result['changes']['added']:
            line_text = line.get('line', '') if isinstance(line, dict) else str(line)
            writer.writerow(['Added', line_text])
        
        # Write removed lines
        for line in result['changes']['removed']:
            line_text = line.get('line', '') if isinstance(line, dict) else str(line)
            writer.writerow(['Removed', line_text])
        
        # Write modified lines
        for mod in result['changes']['modified']:
            writer.writerow(['Modified Old', mod.get('old', '')])
            writer.writerow(['Modified New', mod.get('new', '')])
        
        return output.getvalue()
    
    return ""


def generate_recommendations(result: dict, contract_a: Contract, contract_b: Contract) -> str:
    """Generate smart recommendations based on comparison"""
    recommendations = []
    
    # Check if there are significant changes
    total_changed = result['stats']['total_changed']
    if total_changed == 0:
        recommendations.append("✅ No changes detected - contracts are identical")
    elif total_changed < 10:
        recommendations.append("📝 Minor changes detected - review for accuracy")
    elif total_changed < 50:
        recommendations.append("📊 Moderate changes detected - thorough review recommended")
    else:
        recommendations.append("🚨 Major changes detected - comprehensive legal review recommended")
    
    # Check similarity
    similarity = result['stats']['similarity'] * 100
    if similarity > 90:
        recommendations.append("✅ High similarity - contracts are largely consistent")
    elif similarity > 70:
        recommendations.append("⚠️ Moderate similarity - review differences carefully")
    else:
        recommendations.append("🔴 Low similarity - significant revisions made")
    
    # Check health impact
    health_a = contract_a.health_score
    health_b = contract_b.health_score
    if health_b > health_a:
        recommendations.append(f"📈 Health improved from {health_a} to {health_b} - positive changes")
    elif health_b < health_a:
        recommendations.append(f"📉 Health declined from {health_a} to {health_b} - review risky changes")
    
    # Clause coverage impact
    coverage_a = contract_a.clause_type_coverage
    coverage_b = contract_b.clause_type_coverage
    if coverage_b > coverage_a:
        recommendations.append(f"📋 Clause coverage improved from {coverage_a:.0f}% to {coverage_b:.0f}%")
    elif coverage_b < coverage_a:
        recommendations.append(f"⚠️ Clause coverage decreased from {coverage_a:.0f}% to {coverage_b:.0f}%")
    
    return "\n".join([f"  {r}" for r in recommendations])