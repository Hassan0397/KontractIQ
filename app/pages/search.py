"""
KontractIQ - Search Page
Hybrid Search across all contracts with superior UI/UX
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from ..core.search_engine import SearchEngine
from ..utils.constants import COLORS
from ..models.contract import Contract


# Helper function to safely get color values
def get_color(key1, key2):
    """Safely get color value from COLORS dict"""
    try:
        return COLORS[key1][key2]
    except KeyError:
        return "#475569"  # Default fallback


def render_search():
    """Render the search page with superior UI/UX"""
    
    # Page Header with Hero Section
    render_hero_section()
    
    # Check if there are any contracts
    if not st.session_state.contracts:
        render_empty_state()
        return
    
    # Quick Stats Cards
    render_stats_cards()
    
    # Add spacing between stats and instructions
    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
    
    # Step-by-Step Instructions for New Users
    render_instructions()
    
    # Main Search Interface
    render_search_interface()
    
    # Search Results Section
    if 'search_results' in st.session_state and st.session_state.search_results:
        render_search_results()
    
    # Recent Searches
    render_recent_searches()


def render_hero_section():
    """Render the hero section with branding and search count"""
    total_contracts = len(st.session_state.contracts)
    total_clauses = len(st.session_state.clauses)
    total_words = sum(c.word_count for c in st.session_state.contracts)
    
    # Get colors
    navy = get_color('primary', 'deepest_navy')
    rich_navy = get_color('primary', 'rich_navy')
    white = get_color('neutrals', 'white')
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {navy} 0%, {rich_navy} 100%);
        padding: 28px 36px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(10, 38, 71, 0.12);
        border: 1px solid rgba(255,255,255,0.08);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="
                    width: 52px;
                    height: 52px;
                    background: rgba(255,255,255,0.12);
                    border-radius: 14px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 26px;
                    backdrop-filter: blur(8px);
                    border: 1px solid rgba(255,255,255,0.08);
                ">🔍</div>
                <div>
                    <h1 style="
                        color: {white};
                        font-size: 24px;
                        font-weight: 700;
                        margin: 0;
                        letter-spacing: -0.3px;
                        line-height: 1.2;
                    ">
                        KontractIQ Find
                    </h1>
                    <p style="
                        color: rgba(255,255,255,0.7);
                        margin: 2px 0 0 0;
                        font-size: 13px;
                        font-weight: 400;
                    ">
                        Hybrid TF-IDF + BM25 search across your contract portfolio
                    </p>
                </div>
            </div>
            <div style="
                display: flex;
                gap: 24px;
                background: rgba(255,255,255,0.06);
                padding: 10px 24px;
                border-radius: 12px;
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255,255,255,0.05);
            ">
                <div style="text-align: center;">
                    <div style="color: {white}; font-size: 20px; font-weight: 700; line-height: 1.2;">{total_contracts}</div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 11px; font-weight: 400; letter-spacing: 0.3px; text-transform: uppercase;">Contracts</div>
                </div>
                <div style="width: 1px; background: rgba(255,255,255,0.12);"></div>
                <div style="text-align: center;">
                    <div style="color: {white}; font-size: 20px; font-weight: 700; line-height: 1.2;">{total_clauses}</div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 11px; font-weight: 400; letter-spacing: 0.3px; text-transform: uppercase;">Clauses</div>
                </div>
                <div style="width: 1px; background: rgba(255,255,255,0.12);"></div>
                <div style="text-align: center;">
                    <div style="color: {white}; font-size: 20px; font-weight: 700; line-height: 1.2;">{total_words:,}</div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 11px; font-weight: 400; letter-spacing: 0.3px; text-transform: uppercase;">Words</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats_cards():
    """Render quick stats cards similar to dashboard"""
    
    # Get search statistics
    total_searches = st.session_state.get('total_searches', 0)
    avg_results = st.session_state.get('avg_results', 0)
    search_count = st.session_state.get('search_count', 0)
    
    # Calculate search success rate
    if search_count > 0:
        success_rate = int((st.session_state.get('successful_searches', 0) / search_count) * 100)
    else:
        success_rate = 0
    
    # Get colors
    corporate_blue = get_color('primary', 'corporate_blue')
    success = get_color('semantic', 'success')
    info = get_color('semantic', 'info')
    warning = get_color('semantic', 'warning')
    white = get_color('neutrals', 'white')
    navy = get_color('primary', 'deepest_navy')
    dark_gray = get_color('neutrals', 'dark_gray')
    medium_gray = get_color('neutrals', 'medium_gray')
    
    # Use columns with gap
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    stats_config = [
        {"icon": "🔍", "value": total_searches, "label": "Total Searches", "sub": "Session searches", "color": corporate_blue},
        {"icon": "📊", "value": f"{avg_results:.0f}" if avg_results > 0 else "—", "label": "Avg Results", "sub": "Per search query", "color": success},
        {"icon": "🎯", "value": f"{success_rate}%", "label": "Success Rate", "sub": "Searches with results", "color": info},
        {"icon": "⚡", "value": "< 1s", "label": "Avg Speed", "sub": "Response time", "color": warning},
    ]
    
    for idx, (col, config) in enumerate(zip([col1, col2, col3, col4], stats_config)):
        with col:
            st.markdown(f"""
            <div style="
                background: {white};
                border-radius: 12px;
                padding: 14px 16px;
                box-shadow: 0 2px 8px rgba(10, 38, 71, 0.05);
                border-left: 3px solid {config['color']};
                display: flex;
                align-items: center;
                gap: 12px;
                height: 72px;
                max-width: 100%;
                box-sizing: border-box;
            ">
                <div style="
                    width: 38px;
                    height: 38px;
                    background: {config['color']}0f;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                    flex-shrink: 0;
                ">{config['icon']}</div>
                <div style="flex: 1; min-width: 0; overflow: hidden;">
                    <div style="font-size: 18px; font-weight: 700; color: {navy}; line-height: 1.2; white-space: nowrap;">
                        {config['value']}
                    </div>
                    <div style="font-size: 12px; color: {dark_gray}; font-weight: 500; line-height: 1.2; white-space: nowrap;">
                        {config['label']}
                    </div>
                    <div style="font-size: 10px; color: {medium_gray}; line-height: 1.2; white-space: nowrap;">
                        {config['sub']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_instructions():
    """Render step-by-step instructions for new users"""
    
    # Check if user has performed searches
    has_searched = st.session_state.get('search_count', 0) > 0
    
    # Get colors
    corporate_blue = get_color('primary', 'corporate_blue')
    success = get_color('semantic', 'success')
    warning = get_color('semantic', 'warning')
    info = get_color('semantic', 'info')
    navy = get_color('primary', 'deepest_navy')
    dark_gray = get_color('neutrals', 'dark_gray')
    info_bg = get_color('semantic', 'info_bg')
    warning_bg = get_color('semantic', 'warning_bg')
    white = get_color('neutrals', 'white')
    light_gray = get_color('neutrals', 'light_gray')
    
    with st.expander(
        "📖 Search Tips" if not has_searched else "📖 Search Tips",
        expanded=not has_searched
    ):
        # Step cards - Using 3 columns
        col1, col2, col3 = st.columns(3, gap="medium")
        
        steps = [
            {"num": "1", "title": "Enter Your Query", "desc": 'Type specific terms like "payment terms 30 days" or "liability cap". Use quotes for exact phrases.', "color": corporate_blue},
            {"num": "2", "title": "Apply Filters", "desc": "Narrow results by selecting specific contracts or file types. Perfect for targeted analysis.", "color": success},
            {"num": "3", "title": "Review & Export", "desc": "Click on any result to preview the full contract. Export results as CSV for offline analysis.", "color": warning},
        ]
        
        for idx, (col, step) in enumerate(zip([col1, col2, col3], steps)):
            with col:
                st.markdown(f"""
                <div style="
                    background: {white};
                    padding: 16px 14px;
                    border-radius: 12px;
                    border: 1px solid {light_gray};
                    height: 100%;
                    box-shadow: 0 2px 4px rgba(10, 38, 71, 0.04);
                    box-sizing: border-box;
                    max-width: 100%;
                ">
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                        <div style="
                            background: {step['color']};
                            color: {white};
                            border-radius: 50%;
                            width: 30px;
                            height: 30px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 14px;
                            font-weight: 700;
                            flex-shrink: 0;
                            box-shadow: 0 4px 10px {step['color']}35;
                        ">{step['num']}</div>
                        <div style="flex: 1; min-width: 0;">
                            <strong style="color: {navy}; font-size: 14px; display: block; margin-bottom: 4px;">{step['title']}</strong>
                            <p style="color: {dark_gray}; font-size: 12px; margin: 0; line-height: 1.6;">
                                {step['desc']}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Advanced tips section - 2 columns
        st.markdown(f"""
        <div style="margin-top: 16px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                <div style="
                    background: {info_bg};
                    padding: 14px 18px;
                    border-radius: 12px;
                    border-left: 4px solid {info};
                ">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 16px;">💡</span>
                        <strong style="color: {navy}; font-size: 14px;">Pro Tips</strong>
                    </div>
                    <ul style="color: {dark_gray}; font-size: 13px; margin: 0; padding-left: 20px; line-height: 2;">
                        <li>Use <code style="background: {white}; padding: 1px 8px; border-radius: 4px; font-size: 12px;">OR</code> for multiple terms: <code style="background: {white}; padding: 1px 8px; border-radius: 4px; font-size: 12px;">liability OR indemnification</code></li>
                        <li>Be specific: <code style="background: {white}; padding: 1px 8px; border-radius: 4px; font-size: 12px;">termination notice period 30 days</code></li>
                        <li>Try common variations and synonyms</li>
                    </ul>
                </div>
                <div style="
                    background: {warning_bg};
                    padding: 14px 18px;
                    border-radius: 12px;
                    border-left: 4px solid {warning};
                ">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 16px;">📊</span>
                        <strong style="color: {navy}; font-size: 14px;">What You Can Find</strong>
                    </div>
                    <ul style="color: {dark_gray}; font-size: 13px; margin: 0; padding-left: 20px; line-height: 2;">
                        <li>Specific clauses across all contracts</li>
                        <li>Payment terms and liability caps</li>
                        <li>Governing law and jurisdiction</li>
                        <li>Confidentiality and renewal terms</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_search_interface():
    """Render the main search interface"""
    
    st.divider()
    st.markdown("### 🔍 Search Contracts")
    
    # Get the current query from session state or use default
    default_query = st.session_state.get('search_query_input', '')
    
    # Search input with enhanced UI
    col1, col2, col3 = st.columns([5, 1.2, 1], gap="small")
    
    with col1:
        query = st.text_input(
            "Search Query",
            placeholder="e.g., payment terms 30 days, liability cap, termination notice period",
            key="search_query_input",
            value=default_query,
            label_visibility="collapsed"
        )
    
    with col2:
        top_k = st.selectbox(
            "Results",
            options=[5, 10, 20, 30, 50],
            index=1,
            key="top_k_select",
            label_visibility="collapsed"
        )
    
    with col3:
        search_clicked = st.button(
            "🔍 Search",
            key="search_btn_main",
            use_container_width=True,
            type="primary"
        )
    
    # Advanced filters in expandable section
    with st.expander("🔧 Advanced Filters", expanded=False):
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            contract_names = ["All"] + [c.name for c in st.session_state.contracts]
            selected_contract = st.selectbox(
                "📄 Filter by Contract",
                options=contract_names,
                key="filter_contract_advanced"
            )
        
        with col2:
            file_types = ["All"] + list(set([c.file_type for c in st.session_state.contracts]))
            selected_file_type = st.selectbox(
                "📂 Filter by File Type",
                options=file_types,
                key="filter_type_advanced"
            )
        
        with col3:
            clause_types = ["All"] + sorted(list(set([c.type for c in st.session_state.clauses])))
            selected_clause_type = st.selectbox(
                "📋 Filter by Clause Type",
                options=clause_types,
                key="filter_clause_advanced"
            )
    
    # Process search
    if search_clicked and query.strip():
        perform_search(query, top_k, selected_contract, selected_file_type, selected_clause_type)
    elif search_clicked and not query.strip():
        st.warning("⚠️ Please enter a search query")
    
    # Quick search buttons
    st.markdown("### 🚀 Quick Searches")
    quick_queries = [
        "payment terms",
        "liability cap",
        "termination notice",
        "governing law",
        "confidentiality",
        "indemnification",
        "force majeure",
        "renewal"
    ]
    
    cols = st.columns(4, gap="small")
    for i, q in enumerate(quick_queries):
        with cols[i % 4]:
            if st.button(f"🔍 {q}", key=f"quick_{q}", use_container_width=True):
                st.session_state.quick_search_query = q
                st.session_state.trigger_search = True
                st.rerun()
    
    # Check for quick search trigger
    if st.session_state.get('trigger_search', False):
        query = st.session_state.get('quick_search_query', '')
        if query:
            contract_filter = selected_contract if 'selected_contract' in locals() else "All"
            file_filter = selected_file_type if 'selected_file_type' in locals() else "All"
            clause_filter = selected_clause_type if 'selected_clause_type' in locals() else "All"
            perform_search(query, top_k, contract_filter, file_filter, clause_filter)
        st.session_state.trigger_search = False


def perform_search(query: str, top_k: int, selected_contract: str, selected_file_type: str, selected_clause_type: str):
    """Execute the search and store results"""
    
    # Update search stats
    st.session_state.total_searches = st.session_state.get('total_searches', 0) + 1
    st.session_state.search_count = st.session_state.get('search_count', 0) + 1
    
    # Initialize search engine
    search_engine = SearchEngine()
    
    # Prepare documents for indexing
    documents = []
    for contract in st.session_state.contracts:
        documents.append({
            'id': contract.id,
            'name': contract.name,
            'text': contract.text,
            'file_type': contract.file_type,
            'pages': contract.pages,
            'clause_count': contract.clause_count,
            'clauses': contract.clauses,
            'risks': contract.risks,
            'vendor': contract.vendor,
            'word_count': contract.word_count,
            'overall_health': contract.overall_health
        })
    
    # Index documents
    with st.spinner("🔍 Indexing and searching..."):
        search_engine.index_documents(documents)
        
        # Apply filters
        filtered_contracts = st.session_state.contracts
        
        if selected_contract != "All":
            filtered_contracts = [c for c in filtered_contracts if c.name == selected_contract]
        
        if selected_file_type != "All":
            filtered_contracts = [c for c in filtered_contracts if c.file_type == selected_file_type]
        
        if selected_clause_type != "All":
            filtered_contracts = [c for c in filtered_contracts if selected_clause_type in c.clause_types]
        
        # Perform search
        try:
            if len(filtered_contracts) < len(st.session_state.contracts):
                results = search_engine.search(
                    query=query,
                    top_k=top_k,
                    contracts=filtered_contracts
                )
            else:
                results = search_engine.search(
                    query=query,
                    top_k=top_k,
                    contracts=None
                )
            
            # Store results
            st.session_state.search_results = results
            st.session_state.search_query = query
            st.session_state.search_top_k = top_k
            
            # Update stats
            if results:
                st.session_state.successful_searches = st.session_state.get('successful_searches', 0) + 1
                st.session_state.avg_results = (st.session_state.get('avg_results', 0) * (st.session_state.search_count - 1) + len(results)) / st.session_state.search_count
            
            # Store recent search
            if 'recent_searches' not in st.session_state:
                st.session_state.recent_searches = []
            if query not in [s['query'] for s in st.session_state.recent_searches]:
                st.session_state.recent_searches.insert(0, {
                    'query': query,
                    'timestamp': datetime.now(),
                    'results_count': len(results)
                })
                st.session_state.recent_searches = st.session_state.recent_searches[:10]
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Search error: {str(e)}")
            return


def render_search_results():
    """Render search results with enhanced UI"""
    
    results = st.session_state.search_results
    query = st.session_state.get('search_query', '')
    
    if not results:
        st.info("🔍 No results found. Try adjusting your search query or filters.")
        return
    
    # Results header with metrics
    st.divider()
    st.markdown("### 📊 Search Results")
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.metric("📊 Total Results", len(results))
    
    with col2:
        unique_contracts = len(set(r['document']['name'] for r in results))
        st.metric("📄 Unique Contracts", unique_contracts)
    
    with col3:
        avg_score = sum(r['score'] for r in results) / len(results) * 100
        st.metric("🎯 Avg Relevance", f"{avg_score:.1f}%")
    
    with col4:
        st.metric("⚡ Speed", "< 1s")
    
    # Create enhanced results table
    result_data = []
    for result in results:
        doc = result['document']
        
        health = doc.get('overall_health', '')
        health_emoji = {
            'healthy': '✅',
            'warning': '⚠️',
            'critical': '🔴',
            'scanned': '📄'
        }.get(health, '📄')
        
        result_data.append({
            "Contract": doc['name'],
            "File Type": doc['file_type'].upper(),
            "Pages": doc.get('pages', 0),
            "Clauses": doc.get('clause_count', 0),
            "Risks": len(doc.get('risks', [])),
            "Relevance": f"{result['score'] * 100:.1f}%",
            "Status": health_emoji,
            "Preview": doc['text'][:200] + "..." if len(doc.get('text', '')) > 200 else doc.get('text', '')
        })
    
    df = pd.DataFrame(result_data)
    
    # Display results table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Contract": st.column_config.TextColumn("📄 Contract", width="medium"),
            "File Type": st.column_config.TextColumn("📂 Type", width="small"),
            "Pages": st.column_config.NumberColumn("📄 Pages", width="small"),
            "Clauses": st.column_config.NumberColumn("📝 Clauses", width="small"),
            "Risks": st.column_config.NumberColumn("⚠️ Risks", width="small"),
            "Relevance": st.column_config.TextColumn("🎯 Relevance", width="small"),
            "Status": st.column_config.TextColumn("📊 Status", width="small"),
            "Preview": st.column_config.TextColumn("📖 Preview", width="large"),
        }
    )
    
    # Export and actions section
    st.divider()
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Export Results as CSV",
            data=csv_data,
            file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="export_search_results",
            use_container_width=True
        )
    
    with col2:
        if st.button("📋 Copy Results", key="copy_results_btn", use_container_width=True):
            st.code(df.to_string(index=False), language="text")
            st.success("✅ Results copied! You can now copy them from the code block above.")
    
    with col3:
        if st.button("📊 View in Report", key="view_report_btn", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()
    
    with col4:
        if st.button("🗑️ Clear Results", key="clear_results_btn", use_container_width=True):
            st.session_state.search_results = None
            st.rerun()
    
    # Detailed preview section
    st.divider()
    st.markdown("### 📄 Detailed Contract Preview")
    
    contract_options = [
        f"{r['document']['name']} ({r['score'] * 100:.1f}%)" 
        for r in results[:20]
    ]
    
    if contract_options:
        selected_idx = st.selectbox(
            "Select a contract to preview",
            options=list(range(len(contract_options))),
            format_func=lambda x: contract_options[x],
            key="result_detail_select"
        )
        
        selected_result = results[selected_idx]
        selected_doc = selected_result['document']
        
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Overview", "📝 Clauses", "⚠️ Risks", "🔍 Matches"])
        
        with tab1:
            render_contract_overview(selected_doc, selected_result)
        
        with tab2:
            render_contract_clauses(selected_doc)
        
        with tab3:
            render_contract_risks(selected_doc)
        
        with tab4:
            render_search_matches(selected_doc, query)


def render_contract_overview(doc: Dict[str, Any], result: Dict[str, Any]):
    """Render contract overview tab"""
    
    navy = get_color('primary', 'deepest_navy')
    dark_gray = get_color('neutrals', 'dark_gray')
    off_white = get_color('neutrals', 'off_white')
    light_gray = get_color('neutrals', 'light_gray')
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.metric("📄 Contract", doc['name'])
    with col2:
        st.metric("📝 Clauses", doc.get('clause_count', 0))
    with col3:
        st.metric("⚠️ Risks", len(doc.get('risks', [])))
    with col4:
        st.metric("🎯 Relevance", f"{result['score'] * 100:.1f}%")
    
    health = doc.get('overall_health', 'unknown')
    health_labels = {
        'healthy': '✅ Healthy',
        'warning': '⚠️ Needs Review',
        'critical': '🔴 Critical Issues',
        'scanned': '📄 Scanned Document'
    }
    
    st.markdown(f"""
    <div style="
        background: {off_white};
        padding: 12px 16px;
        border-radius: 10px;
        margin: 8px 0 16px 0;
        border: 1px solid {light_gray};
    ">
        <span style="font-weight: 600; color: {navy}; font-size: 14px;">Health Status:</span>
        <span style="color: {dark_gray}; font-size: 14px; margin-left: 6px;">{health_labels.get(health, 'Unknown')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.text_area(
        "Contract Text Preview",
        doc.get('text', '')[:2000] + "..." if len(doc.get('text', '')) > 2000 else doc.get('text', ''),
        height=200,
        disabled=True
    )


def render_contract_clauses(doc: Dict[str, Any]):
    """Render contract clauses tab"""
    
    off_white = get_color('neutrals', 'off_white')
    dark_gray = get_color('neutrals', 'dark_gray')
    corporate_blue = get_color('primary', 'corporate_blue')
    
    clauses = doc.get('clauses', [])
    if not clauses:
        st.info("No clauses extracted from this contract")
        return
    
    clauses_by_type = {}
    for clause in clauses:
        clause_type = clause.type if hasattr(clause, 'type') else clause.get('type', 'Unknown')
        if clause_type not in clauses_by_type:
            clauses_by_type[clause_type] = []
        clauses_by_type[clause_type].append(clause)
    
    for clause_type, clause_list in clauses_by_type.items():
        with st.expander(f"📋 {clause_type} ({len(clause_list)})"):
            for clause in clause_list[:5]:
                text = clause.text if hasattr(clause, 'text') else clause.get('text', '')
                st.markdown(f"""
                <div style="
                    background: {off_white};
                    padding: 10px 14px;
                    border-radius: 8px;
                    margin-bottom: 6px;
                    font-size: 13px;
                    color: {dark_gray};
                    border-left: 3px solid {corporate_blue};
                    line-height: 1.6;
                ">
                    {text[:200]}{'...' if len(text) > 200 else ''}
                </div>
                """, unsafe_allow_html=True)
            if len(clause_list) > 5:
                st.caption(f"... and {len(clause_list) - 5} more {clause_type} clauses")


def render_contract_risks(doc: Dict[str, Any]):
    """Render contract risks tab"""
    
    navy = get_color('primary', 'deepest_navy')
    dark_gray = get_color('neutrals', 'dark_gray')
    danger = get_color('semantic', 'danger')
    danger_bg = get_color('semantic', 'danger_bg')
    warning = get_color('semantic', 'warning')
    warning_bg = get_color('semantic', 'warning_bg')
    info = get_color('semantic', 'info')
    info_bg = get_color('semantic', 'info_bg')
    medium_gray = get_color('neutrals', 'medium_gray')
    off_white = get_color('neutrals', 'off_white')
    white = get_color('neutrals', 'white')
    
    risks = doc.get('risks', [])
    if not risks:
        st.success("✅ No risks found in this contract")
        return
    
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    sorted_risks = sorted(risks, key=lambda r: severity_order.get(r.severity if hasattr(r, 'severity') else r.get('severity', 'low'), 4))
    
    for risk in sorted_risks[:10]:
        severity = risk.severity if hasattr(risk, 'severity') else risk.get('severity', 'low')
        
        if severity == 'critical':
            sev_color = danger
            sev_bg = danger_bg
        elif severity == 'high':
            sev_color = warning
            sev_bg = warning_bg
        elif severity == 'medium':
            sev_color = warning
            sev_bg = warning_bg
        elif severity == 'low':
            sev_color = info
            sev_bg = info_bg
        else:
            sev_color = medium_gray
            sev_bg = off_white
        
        risk_type = risk.type if hasattr(risk, 'type') else risk.get('type', 'Unknown Risk')
        description = risk.description if hasattr(risk, 'description') else risk.get('description', 'No description')
        
        st.markdown(f"""
        <div style="
            background: {sev_bg};
            padding: 12px 16px;
            border-radius: 10px;
            border-left: 4px solid {sev_color};
            margin-bottom: 8px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: {navy}; font-size: 14px;">{risk_type.replace('_', ' ').title()}</strong>
                <span style="
                    color: {sev_color};
                    font-weight: 600;
                    font-size: 12px;
                    background: {white};
                    padding: 2px 10px;
                    border-radius: 12px;
                    border: 1px solid {sev_color}30;
                ">
                    {severity.upper()}
                </span>
            </div>
            <div style="color: {dark_gray}; font-size: 13px; margin-top: 6px; line-height: 1.6;">
                {description}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if len(risks) > 10:
        st.caption(f"... and {len(risks) - 10} more risks")


def render_search_matches(doc: Dict[str, Any], query: str):
    """Render search matches tab"""
    
    navy = get_color('primary', 'deepest_navy')
    dark_gray = get_color('neutrals', 'dark_gray')
    info_bg = get_color('semantic', 'info_bg')
    corporate_blue = get_color('primary', 'corporate_blue')
    medium_gray = get_color('neutrals', 'medium_gray')
    
    text = doc.get('text', '')
    if not query or not text:
        st.info("No search matches to display")
        return
    
    query_lower = query.lower()
    matches = []
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if query_lower in line.lower():
            matches.append({
                'line_num': i + 1,
                'text': line.strip(),
                'context': lines[max(0, i-1):min(len(lines), i+3)]
            })
    
    if not matches:
        st.info(f"ℹ️ '{query}' not found in this contract")
        return
    
    st.caption(f"Found {len(matches)} matches for '{query}'")
    
    for match in matches[:10]:
        st.markdown(f"""
        <div style="
            background: {info_bg};
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 6px;
            border-left: 3px solid {corporate_blue};
        ">
            <div style="color: {medium_gray}; font-size: 11px; font-weight: 500; margin-bottom: 2px;">
                Line {match['line_num']}
            </div>
            <div style="color: {navy}; font-size: 13px; line-height: 1.6;">
                {match['text'][:300]}{'...' if len(match['text']) > 300 else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if len(matches) > 10:
        st.caption(f"... and {len(matches) - 10} more matches")


def render_recent_searches():
    """Render recent searches section"""
    
    if 'recent_searches' not in st.session_state or not st.session_state.recent_searches:
        return
    
    st.divider()
    st.markdown("### 🕐 Recent Searches")
    
    cols = st.columns(4, gap="small")
    for i, search in enumerate(st.session_state.recent_searches[:8]):
        with cols[i % 4]:
            time_ago = (datetime.now() - search['timestamp']).seconds
            if time_ago < 60:
                time_str = f"{time_ago}s ago"
            elif time_ago < 3600:
                time_str = f"{time_ago // 60}m ago"
            else:
                time_str = f"{time_ago // 3600}h ago"
            
            if st.button(
                f"🔍 {search['query']} ({search['results_count']})",
                key=f"recent_{i}",
                use_container_width=True
            ):
                st.session_state.quick_search_query = search['query']
                st.session_state.trigger_search = True
                st.rerun()
            
            st.caption(time_str)


def render_empty_state():
    """Render empty state with helpful guidance"""
    
    off_white = get_color('neutrals', 'off_white')
    light_gray = get_color('neutrals', 'light_gray')
    navy = get_color('primary', 'deepest_navy')
    dark_gray = get_color('neutrals', 'dark_gray')
    corporate_blue = get_color('primary', 'corporate_blue')
    white = get_color('neutrals', 'white')
    
    st.markdown(f"""
    <div style="
        background: {off_white};
        border-radius: 16px;
        padding: 56px 40px;
        text-align: center;
        border: 2px dashed {light_gray};
        margin: 16px 0;
    ">
        <div style="font-size: 64px; margin-bottom: 20px;">🔍</div>
        <h2 style="color: {navy}; margin: 0 0 8px 0; font-size: 24px; font-weight: 700;">
            No Contracts to Search
        </h2>
        <p style="color: {dark_gray}; font-size: 15px; max-width: 480px; margin: 0 auto 28px auto; line-height: 1.6;">
            Upload contracts or load demo data to start searching for specific clauses and terms.
        </p>
        <div style="display: flex; gap: 14px; justify-content: center; flex-wrap: wrap;">
            <a href="#" onclick="window.location.href='?page=Upload+Contracts'" style="
                background: {corporate_blue};
                color: white;
                padding: 12px 28px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                font-size: 14px;
                display: inline-block;
                cursor: pointer;
                box-shadow: 0 4px 12px {corporate_blue}40;
            ">📤 Upload Contracts</a>
            <a href="#" onclick="window.location.href='?page=Dashboard'" style="
                background: {white};
                color: {corporate_blue};
                padding: 12px 28px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                font-size: 14px;
                display: inline-block;
                border: 2px solid {corporate_blue};
                cursor: pointer;
            ">🎯 Load Demo Data</a>
        </div>
    </div>
    """, unsafe_allow_html=True)