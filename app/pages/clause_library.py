"""
KontractIQ - Clause Library Page
Browse, search, filter, and export extracted clauses
"""

import streamlit as st
import pandas as pd
from typing import List, Optional
from ..utils.constants import CLAUSE_TYPES, COLORS, CLAUSE_TYPE_ICONS, CLAUSE_TYPE_COLORS
from ..models.clause import Clause


def render_clause_library():
    """
    Render the clause library page with premium UI/UX
    Features: Filtering, Searching, Card/Table Views, Export, Detailed View
    """
    
    # =========================================================================
    # HERO / HEADER SECTION
    # =========================================================================
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['rich_navy']} 100%);
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(10, 38, 71, 0.15);
    ">
        <div style="display: flex; align-items: center; gap: 16px;">
            <span style="font-size: 36px;">📚</span>
            <div style="flex: 1;">
                <div style="color: #FFFFFF; font-size: 26px; font-weight: 600; margin: 0; letter-spacing: -0.3px;">
                    Clause Library
                </div>
                <div style="color: rgba(255,255,255,0.85); font-size: 14px; margin: 4px 0 0 0;">
                    Browse, search, and analyze all extracted clauses across your contract portfolio
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 12px; text-align: center;">
                <div style="color: #FFFFFF; font-size: 24px; font-weight: 600; line-height: 1.2;">
                    {len(st.session_state.clauses)}
                </div>
                <div style="color: rgba(255,255,255,0.7); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">
                    Total Clauses
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # INSTRUCTION / ONBOARDING SECTION
    # =========================================================================
    with st.expander("ℹ️ How to Use This Page", expanded=False):
        st.markdown(f"""
        <div style="
            background: {COLORS['primary']['ice_blue']};
            padding: 20px 24px;
            border-radius: 16px;
            border-left: 4px solid {COLORS['primary']['corporate_blue']};
        ">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <div>
                    <strong style="color: {COLORS['primary']['deepest_navy']}; font-size: 15px;">🔍 Filter & Search</strong>
                    <ul style="color: {COLORS['neutrals']['dark_gray']}; font-size: 13px; margin: 6px 0 0 0; padding-left: 20px; line-height: 1.8;">
                        <li>Select a <strong>Clause Type</strong> to view specific clauses</li>
                        <li>Filter by <strong>Contract</strong> to focus on one document</li>
                        <li>Use the <strong>Search</strong> bar to find keywords within clauses</li>
                        <li>Adjust <strong>Confidence</strong> slider to show only high-quality matches</li>
                    </ul>
                </div>
                <div>
                    <strong style="color: {COLORS['primary']['deepest_navy']}; font-size: 15px;">📊 View & Export</strong>
                    <ul style="color: {COLORS['neutrals']['dark_gray']}; font-size: 13px; margin: 6px 0 0 0; padding-left: 20px; line-height: 1.8;">
                        <li>Toggle between <strong>Table</strong> and <strong>Card</strong> views</li>
                        <li>Sort clauses by <strong>Confidence</strong>, <strong>Type</strong>, or <strong>Contract</strong></li>
                        <li>Click a clause to view <strong>full text details</strong></li>
                        <li><strong>Export</strong> all filtered clauses as CSV</li>
                    </ul>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid {COLORS['neutrals']['light_gray']};">
                <span style="color: {COLORS['neutrals']['medium_gray']}; font-size: 12px;">
                    💡 <strong>Pro Tip:</strong> Use the confidence filter to focus on high-confidence clauses (70%+) for critical review
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # CHECK FOR CLAUSES
    # =========================================================================
    if not st.session_state.clauses:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: {COLORS['neutrals']['off_white']};
            border-radius: 20px;
            border: 2px dashed {COLORS['neutrals']['light_gray']};
        ">
            <div style="font-size: 56px; margin-bottom: 16px;">📭</div>
            <div style="font-size: 22px; font-weight: 600; color: {COLORS['primary']['deepest_navy']}; margin: 0;">No Clauses Extracted Yet</div>
            <div style="color: {COLORS['neutrals']['dark_gray']}; margin: 8px 0 16px 0;">
                Upload contracts first to extract and view clauses
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Upload Contracts", use_container_width=True):
                st.session_state.page = "Upload Contracts"
                st.rerun()
        with col2:
            if st.button("🏠 Go to Dashboard", use_container_width=True):
                st.session_state.page = "Dashboard"
                st.rerun()
        return

    # =========================================================================
    # PREMIUM METRICS CARDS (Blue Theme - Matching Dashboard)
    # =========================================================================
    all_clauses = st.session_state.clauses
    total_clauses = len(all_clauses)
    unique_types = len(set(c.type for c in all_clauses))
    high_confidence = len([c for c in all_clauses if c.confidence >= 0.8])
    avg_confidence = sum(c.confidence for c in all_clauses) / total_clauses if total_clauses > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']}, {COLORS['primary']['rich_navy']});
            border-radius: 16px;
            padding: 18px 16px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(10, 38, 71, 0.12);
        ">
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF;">{total_clauses}</div>
            <div style="font-size: 13px; color: rgba(255,255,255,0.8);">Total Clauses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['primary']['corporate_blue']}, {COLORS['primary']['vibrant_blue']});
            border-radius: 16px;
            padding: 18px 16px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(44, 95, 138, 0.2);
        ">
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF;">{unique_types}</div>
            <div style="font-size: 13px; color: rgba(255,255,255,0.8);">Clause Types</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['semantic']['success']}, {COLORS['semantic']['success_dark']});
            border-radius: 16px;
            padding: 18px 16px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2);
        ">
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF;">{high_confidence}</div>
            <div style="font-size: 13px; color: rgba(255,255,255,0.8);">High Confidence (≥80%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['semantic']['info']}, {COLORS['semantic']['info_dark']});
            border-radius: 16px;
            padding: 18px 16px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        ">
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF;">{avg_confidence * 100:.0f}%</div>
            <div style="font-size: 13px; color: rgba(255,255,255,0.8);">Avg Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # =========================================================================
    # FILTERS SECTION
    # =========================================================================
    # Use st.container for the filter section instead of raw HTML
    with st.container():
        st.markdown("### 🔍 Filter Clauses")
        st.caption(f"{len(all_clauses)} total clauses available")
        
        col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1.5])

        with col1:
            clause_types = ["All Types"] + CLAUSE_TYPES
            selected_type = st.selectbox(
                "📋 Clause Type",
                options=clause_types,
                key="clause_type_filter",
                help="Filter by specific clause type"
            )

        with col2:
            contract_names = ["All Contracts"] + sorted(list(set([c.contract_name for c in all_clauses])))
            selected_contract = st.selectbox(
                "📄 Contract",
                options=contract_names,
                key="contract_filter",
                help="Filter by specific contract"
            )

        with col3:
            min_confidence = st.slider(
                "🎯 Min Confidence",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                key="confidence_filter",
                help="Show only clauses with confidence above this threshold"
            )

        with col4:
            view_mode = st.radio(
                "📊 View Mode",
                options=["Table", "Cards"],
                horizontal=True,
                key="view_mode",
                help="Switch between table and card view"
            )

    # =========================================================================
    # SORT OPTIONS
    # =========================================================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sort_by = st.selectbox(
            "📊 Sort By",
            options=[
                "Confidence (High → Low)",
                "Confidence (Low → High)",
                "Clause Type (A → Z)",
                "Clause Type (Z → A)",
                "Contract Name (A → Z)",
                "Contract Name (Z → A)"
            ],
            key="sort_by",
            help="Sort the displayed clauses"
        )

    with col2:
        show_count = st.number_input(
            "📄 Show",
            min_value=5,
            max_value=100,
            value=50,
            step=5,
            key="show_count",
            help="Number of clauses to display"
        )

    # =========================================================================
    # APPLY FILTERS
    # =========================================================================
    filtered_clauses = all_clauses.copy()

    if selected_type != "All Types":
        filtered_clauses = [c for c in filtered_clauses if c.type == selected_type]

    if selected_contract != "All Contracts":
        filtered_clauses = [c for c in filtered_clauses if c.contract_name == selected_contract]

    if min_confidence > 0:
        filtered_clauses = [c for c in filtered_clauses if c.confidence >= min_confidence]

    # Apply sorting
    if sort_by == "Confidence (High → Low)":
        filtered_clauses.sort(key=lambda c: c.confidence, reverse=True)
    elif sort_by == "Confidence (Low → High)":
        filtered_clauses.sort(key=lambda c: c.confidence)
    elif sort_by == "Clause Type (A → Z)":
        filtered_clauses.sort(key=lambda c: c.type)
    elif sort_by == "Clause Type (Z → A)":
        filtered_clauses.sort(key=lambda c: c.type, reverse=True)
    elif sort_by == "Contract Name (A → Z)":
        filtered_clauses.sort(key=lambda c: c.contract_name)
    elif sort_by == "Contract Name (Z → A)":
        filtered_clauses.sort(key=lambda c: c.contract_name, reverse=True)

    # Limit display
    display_clauses = filtered_clauses[:show_count]

    # =========================================================================
    # RESULTS HEADER - FIXED WITH PROPER STREAMLIT COMPONENTS
    # =========================================================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**📊 Results:** {len(filtered_clauses)} clauses found" + 
                   (f" (showing {len(display_clauses)})" if len(filtered_clauses) > show_count else ""))
    
    with col2:
        type_count = len(set(c.type for c in display_clauses))
        high_conf_count = len([c for c in display_clauses if c.confidence >= 0.8])
        
        # Create badge HTML safely
        badge_html = f"""
        <div style="display: flex; gap: 8px; justify-content: flex-end;">
            <span style="background: {COLORS['primary']['ice_blue']}; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: {COLORS['primary']['corporate_blue']};">
                {type_count} types
            </span>
            <span style="background: {COLORS['semantic']['success_bg']}; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: {COLORS['semantic']['success']};">
                {high_conf_count} high confidence
            </span>
        </div>
        """
        st.markdown(badge_html, unsafe_allow_html=True)

    st.divider()

    # =========================================================================
    # DISPLAY CLAUSES - TABLE VIEW
    # =========================================================================
    if not display_clauses:
        st.info("🔍 No clauses match your filters. Try adjusting your search criteria.")
        return

    if view_mode == "Table":
        # Prepare data for DataFrame
        data = []
        for clause in display_clauses:
            # Determine confidence level
            if clause.confidence >= 0.8:
                conf_label = "High"
            elif clause.confidence >= 0.6:
                conf_label = "Medium"
            else:
                conf_label = "Low"
            
            data.append({
                "Contract": clause.contract_name,
                "Type": f"{clause.type_icon} {clause.type}",
                "Clause": clause.text[:250] + "..." if len(clause.text) > 250 else clause.text,
                "Confidence": f"{clause.confidence * 100:.0f}%",
                "Level": conf_label,
                "Words": clause.word_count
            })

        df = pd.DataFrame(data)

        # Display as table with enhanced styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Contract": st.column_config.TextColumn("📄 Contract", width="medium"),
                "Type": st.column_config.TextColumn("📋 Type", width="medium"),
                "Clause": st.column_config.TextColumn("📝 Clause Text", width="large"),
                "Confidence": st.column_config.TextColumn("🎯 Confidence", width="small"),
                "Level": st.column_config.TextColumn("📊 Level", width="small"),
                "Words": st.column_config.NumberColumn("📝 Words", width="small"),
            }
        )

    # =========================================================================
    # DISPLAY CLAUSES - CARD VIEW (Premium Cards)
    # =========================================================================
    else:
        # Display as premium cards
        cards_per_row = 2
        rows = [display_clauses[i:i + cards_per_row] for i in range(0, len(display_clauses), cards_per_row)]

        for row in rows:
            cols = st.columns(cards_per_row)
            for idx, clause in enumerate(row):
                with cols[idx]:
                    # Determine card color based on clause type
                    card_color = CLAUSE_TYPE_COLORS.get(clause.type, COLORS['primary']['corporate_blue'])
                    
                    # Determine confidence badge
                    if clause.confidence >= 0.8:
                        badge_color = COLORS['semantic']['success']
                        badge_bg = COLORS['semantic']['success_bg']
                        badge_text = "High"
                    elif clause.confidence >= 0.6:
                        badge_color = COLORS['semantic']['warning']
                        badge_bg = COLORS['semantic']['warning_bg']
                        badge_text = "Medium"
                    else:
                        badge_color = COLORS['semantic']['danger']
                        badge_bg = COLORS['semantic']['danger_bg']
                        badge_text = "Low"

                    st.markdown(f"""
                    <div style="
                        background: {COLORS['neutrals']['white']};
                        border-radius: 16px;
                        padding: 16px 18px;
                        box-shadow: 0 2px 12px rgba(10, 38, 71, 0.06);
                        border-left: 4px solid {card_color};
                        height: 100%;
                        transition: all 0.25s ease;
                        margin-bottom: 12px;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
                            <div style="flex: 1; min-width: 0;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 18px;">{clause.type_icon}</span>
                                    <span style="font-size: 14px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">
                                        {clause.type}
                                    </span>
                                </div>
                                <div style="
                                    font-size: 13px;
                                    color: {COLORS['neutrals']['dark_gray']};
                                    margin: 8px 0;
                                    line-height: 1.6;
                                    max-height: 80px;
                                    overflow: hidden;
                                    text-overflow: ellipsis;
                                ">
                                    {clause.text[:200]}{'...' if len(clause.text) > 200 else ''}
                                </div>
                                <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px;">
                                    <span style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']};">
                                        📄 {clause.contract_name[:30]}{'...' if len(clause.contract_name) > 30 else ''}
                                    </span>
                                    <span style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']};">
                                        📝 {clause.word_count} words
                                    </span>
                                </div>
                            </div>
                            <div style="text-align: right; flex-shrink: 0;">
                                <span style="
                                    background: {badge_bg};
                                    color: {badge_color};
                                    padding: 2px 12px;
                                    border-radius: 12px;
                                    font-size: 11px;
                                    font-weight: 600;
                                    display: inline-block;
                                    white-space: nowrap;
                                ">
                                    {badge_text} {clause.confidence * 100:.0f}%
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # =========================================================================
    # EXPORT SECTION
    # =========================================================================
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📊 Export Filtered Data as CSV", key="export_filtered_btn", use_container_width=True):
            # Export only filtered data
            export_data = []
            for clause in filtered_clauses:
                export_data.append({
                    "Contract": clause.contract_name,
                    "Clause Type": clause.type,
                    "Clause Text": clause.text,
                    "Confidence (%)": f"{clause.confidence * 100:.1f}",
                    "Confidence Level": "High" if clause.confidence >= 0.8 else "Medium" if clause.confidence >= 0.6 else "Low",
                    "Word Count": clause.word_count,
                    "Character Count": clause.char_count
                })
            export_df = pd.DataFrame(export_data)
            csv_data = export_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"clauses_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_filtered_btn",
                use_container_width=True
            )

    with col2:
        if st.button("📤 Export All Clauses", key="export_all_btn", use_container_width=True):
            export_data = []
            for clause in all_clauses:
                export_data.append({
                    "Contract": clause.contract_name,
                    "Clause Type": clause.type,
                    "Clause Text": clause.text,
                    "Confidence (%)": f"{clause.confidence * 100:.1f}",
                    "Word Count": clause.word_count
                })
            export_df = pd.DataFrame(export_data)
            csv_data = export_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download All CSV",
                data=csv_data,
                file_name=f"all_clauses_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_all_btn",
                use_container_width=True
            )

    with col3:
        if st.button("📋 Copy to Clipboard", key="copy_all_btn", use_container_width=True):
            text_data = "=" * 60 + "\n"
            text_data += "KONTRACTIQ - CLAUSE LIBRARY EXPORT\n"
            text_data += f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            text_data += f"Total Clauses: {len(filtered_clauses)}\n"
            text_data += "=" * 60 + "\n\n"
            
            for clause in filtered_clauses[:20]:
                text_data += f"📋 {clause.type}\n"
                text_data += f"📄 {clause.contract_name}\n"
                text_data += f"🎯 Confidence: {clause.confidence * 100:.0f}%\n"
                text_data += f"📝 {clause.text}\n"
                text_data += "-" * 40 + "\n"
            
            if len(filtered_clauses) > 20:
                text_data += f"\n... and {len(filtered_clauses) - 20} more clauses\n"
            
            st.code(text_data, language="text")
            st.success("✅ Data copied to code block above! Select and copy it.")

    # =========================================================================
    # DETAILED VIEW SECTION
    # =========================================================================
    st.divider()
    
    # Use st.container for the detailed view section
    with st.container():
        st.markdown("### 📄 Clause Details")
        st.caption("Select a clause below to view its full text")

        # Clause selector for detailed view
        clause_options = [f"{c.type_icon} {c.type} - {c.contract_name} ({c.confidence * 100:.0f}%)" 
                          for c in display_clauses[:100]]
        
        if clause_options:
            selected_idx = st.selectbox(
                "Select a clause to view details",
                options=list(range(len(clause_options))),
                format_func=lambda x: clause_options[x] if x < len(clause_options) else "Select...",
                key="clause_detail_select"
            )
            
            if selected_idx is not None and selected_idx < len(display_clauses):
                selected_clause = display_clauses[selected_idx]
                
                # Display full clause with premium styling
                card_color = CLAUSE_TYPE_COLORS.get(selected_clause.type, COLORS['primary']['corporate_blue'])
                
                st.markdown(f"""
                <div style="
                    background: {COLORS['neutrals']['off_white']};
                    padding: 20px 24px;
                    border-radius: 16px;
                    border-left: 6px solid {card_color};
                    margin: 12px 0;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 24px;">{selected_clause.type_icon}</span>
                                <span style="font-size: 18px; font-weight: 600; color: {COLORS['primary']['deepest_navy']};">
                                    {selected_clause.type}
                                </span>
                            </div>
                            <div style="color: {COLORS['neutrals']['dark_gray']}; font-size: 14px; margin-top: 4px;">
                                📄 {selected_clause.contract_name}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span style="
                                background: {COLORS['semantic']['success_bg'] if selected_clause.confidence >= 0.8 else COLORS['semantic']['warning_bg'] if selected_clause.confidence >= 0.6 else COLORS['semantic']['danger_bg']};
                                color: {COLORS['semantic']['success'] if selected_clause.confidence >= 0.8 else COLORS['semantic']['warning'] if selected_clause.confidence >= 0.6 else COLORS['semantic']['danger']};
                                padding: 4px 16px;
                                border-radius: 20px;
                                font-size: 13px;
                                font-weight: 600;
                                display: inline-block;
                            ">
                                🎯 {selected_clause.confidence * 100:.0f}% Confidence
                            </span>
                            <div style="font-size: 12px; color: {COLORS['neutrals']['medium_gray']}; margin-top: 4px;">
                                📝 {selected_clause.word_count} words • {selected_clause.char_count} characters
                            </div>
                        </div>
                    </div>
                    <div style="
                        background: {COLORS['neutrals']['white']};
                        padding: 16px 20px;
                        border-radius: 12px;
                        font-size: 14px;
                        line-height: 1.8;
                        color: {COLORS['neutrals']['dark_gray']};
                        white-space: pre-wrap;
                        word-wrap: break-word;
                        max-height: 400px;
                        overflow-y: auto;
                    ">
                        {selected_clause.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons for selected clause
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("📋 Copy This Clause", key="copy_selected_btn", use_container_width=True):
                        st.code(selected_clause.text, language="text")
                        st.success("✅ Clause copied to code block above!")
                
                with col2:
                    # Create mini export of just this clause
                    clause_data = pd.DataFrame([{
                        "Contract": selected_clause.contract_name,
                        "Clause Type": selected_clause.type,
                        "Clause Text": selected_clause.text,
                        "Confidence": f"{selected_clause.confidence * 100:.1f}%",
                        "Words": selected_clause.word_count,
                        "Characters": selected_clause.char_count
                    }])
                    csv_data = clause_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download This Clause",
                        data=csv_data,
                        file_name=f"clause_{selected_clause.type}_{selected_clause.contract_name}.csv",
                        mime="text/csv",
                        key="download_selected_btn",
                        use_container_width=True
                    )
                
                with col3:
                    # Find similar clauses
                    similar_clauses = [c for c in all_clauses if c.type == selected_clause.type and c.id != selected_clause.id]
                    if similar_clauses:
                        st.markdown(f"""
                        <div style="
                            background: {COLORS['primary']['ice_blue']};
                            padding: 8px 16px;
                            border-radius: 12px;
                            font-size: 13px;
                            color: {COLORS['primary']['corporate_blue']};
                            text-align: center;
                        ">
                            🔗 {len(similar_clauses)} similar clauses found
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="
                            background: {COLORS['neutrals']['off_white']};
                            padding: 8px 16px;
                            border-radius: 12px;
                            font-size: 13px;
                            color: {COLORS['neutrals']['medium_gray']};
                            text-align: center;
                        ">
                            ℹ️ No similar clauses found
                        </div>
                        """, unsafe_allow_html=True)

    # =========================================================================
    # FOOTER / TIPS SECTION
    # =========================================================================
    st.divider()
    
    # Use streamlit columns for footer instead of raw HTML
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.caption(f"📊 {len(filtered_clauses)} clauses shown • 📁 {len(set(c.contract_name for c in filtered_clauses))} contracts • 📋 {len(set(c.type for c in filtered_clauses))} types")
    
    with col2:
        st.caption("💡 Tip: Use filters to narrow down results")


# =============================================================================
# ALTERNATIVE SIMPLE VERSION (For backward compatibility)
# =============================================================================
def render_clause_library_simple():
    """
    Simpler version of clause library - maintained for backward compatibility
    """
    st.markdown("### 📚 Clause Library")
    st.caption("Browse and search through all extracted clauses")
    
    if not st.session_state.clauses:
        st.info("📭 No clauses extracted yet. Upload contracts first!")
        return
    
    all_clauses = st.session_state.clauses
    
    # Simple filters
    col1, col2 = st.columns(2)
    
    with col1:
        clause_types = ["All"] + CLAUSE_TYPES
        selected_type = st.selectbox("Clause Type", options=clause_types, key="simple_type_filter")
    
    with col2:
        contract_names = ["All"] + sorted(list(set([c.contract_name for c in all_clauses])))
        selected_contract = st.selectbox("Contract", options=contract_names, key="simple_contract_filter")
    
    # Apply filters
    filtered_clauses = all_clauses.copy()
    
    if selected_type != "All":
        filtered_clauses = [c for c in filtered_clauses if c.type == selected_type]
    
    if selected_contract != "All":
        filtered_clauses = [c for c in filtered_clauses if c.contract_name == selected_contract]
    
    st.markdown(f"**Found {len(filtered_clauses)} clauses**")
    
    # Display clauses in expanders
    for idx, clause in enumerate(filtered_clauses[:50]):
        with st.expander(f"{clause.type} - {clause.contract_name}"):
            st.write("**Clause Text:**")
            st.write(clause.text)
            st.write(f"**Confidence:** {clause.confidence * 100:.0f}%")
            
            if st.button("📋 Copy", key=f"copy_clause_{idx}"):
                st.code(clause.text, language="text")
                st.success("Clause copied to code block above!")