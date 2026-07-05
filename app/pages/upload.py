"""
KontractIQ - Upload Page
Multi-Contract Upload with Advanced Features
Production-Ready with Superior UX
"""

import streamlit as st
import os
import time
import hashlib
from datetime import datetime
from typing import List, Optional, Tuple
import pandas as pd

from ..core.parser import DocumentParser
from ..core.extractor import ClauseExtractor
from ..core.risk_scanner import RiskScanner
from ..models.contract import Contract
from ..utils.helpers import generate_id, format_file_size, truncate_text
from ..utils.validators import validate_file, validate_contract_count, validate_file_batch
from ..utils.constants import LIMITS, COLORS, FILE_TYPE_ICONS


def render_upload():
    """Render the upload page with Premium UX"""
    
    # ===== PAGE HEADER =====
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']['deepest_navy']} 0%, {COLORS['primary']['corporate_blue']} 100%);
        padding: 32px 40px;
        border-radius: 24px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(10, 38, 71, 0.15);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: white; font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                    📤 Upload Contracts
                </h1>
                <p style="color: rgba(255,255,255,0.85); font-size: 15px; margin: 6px 0 0 0;">
                    Securely upload and process contracts with AI-powered intelligence
                </p>
            </div>
            <div style="display: flex; gap: 16px; align-items: center;">
                <span style="
                    background: rgba(255,255,255,0.15);
                    color: white;
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    backdrop-filter: blur(10px);
                ">
                    ⚡ Batch Processing
                </span>
                <span style="
                    background: rgba(255,255,255,0.15);
                    color: white;
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 13px;
                    backdrop-filter: blur(10px);
                ">
                    🔒 100% Private
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== QUICK STATS =====
    current_count = len(st.session_state.contracts)
    remaining = LIMITS["max_contracts"] - current_count
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📄 Contracts Loaded", current_count)
    
    with col2:
        color = "green" if remaining > 5 else "orange" if remaining > 0 else "red"
        st.metric("📊 Remaining Slots", remaining)
    
    with col3:
        total_clauses = len(st.session_state.clauses)
        st.metric("📝 Clauses Extracted", total_clauses)
    
    with col4:
        total_risks = len(st.session_state.risks)
        st.metric("⚠️ Risks Detected", total_risks)
    
    with col5:
        memory_usage = get_memory_usage()
        st.metric("💾 Memory Used", f"{memory_usage:.0f}%")
    
    st.divider()
    
    # ===== BATCH UPLOAD WITH ADVANCED FEATURES =====
    if current_count >= LIMITS["max_contracts"]:
        render_contracts_full()
        return
    
    # Enhanced File Uploader
    uploaded_files = st.file_uploader(
        "📁 Drop your contract files here or click to browse",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        key="contract_uploader",
        help=f"Supported: PDF, DOCX, TXT | Max {LIMITS['max_file_size_mb']}MB per file | Max {LIMITS['max_contracts']} contracts"
    )
    
    # File upload status with smart preview
    if uploaded_files:
        # Validate batch
        is_valid, validation_message = validate_file_batch(
            uploaded_files, 
            current_count, 
            LIMITS["max_contracts"],
            LIMITS["max_file_size_mb"] * 1024 * 1024
        )
        
        if not is_valid:
            st.error(f"❌ {validation_message}")
            st.stop()
        
        # Show file preview with details
        render_file_preview(uploaded_files)
        
        # Process with advanced progress
        if st.button("🚀 Process Contracts", key="process_btn", type="primary", use_container_width=True):
            process_contracts_with_advanced_ui(uploaded_files)
    
    st.divider()
    
    # ===== SMART CONTRACT MANAGEMENT =====
    if st.session_state.contracts:
        render_contract_management()
    else:
        render_empty_state()


def render_file_preview(files):
    """Render file preview with advanced details"""
    st.markdown("### 📁 Files Ready for Processing")
    st.caption(f"{len(files)} files selected")
    
    for idx, file in enumerate(files):
        file_size_kb = file.size / 1024
        file_size_mb = file_size_kb / 1024
        size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{file_size_mb:.1f} MB"
        icon = FILE_TYPE_ICONS.get(file.name.split('.')[-1].lower(), "📄")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{icon} {file.name}")
        with col2:
            st.caption(size_str)


def process_contracts_with_advanced_ui(files):
    """Process contracts with advanced UI progress"""
    
    # Setup progress tracking
    total_files = len(files)
    
    # Progress bar with percentage
    progress_text = st.empty()
    progress_bar = st.progress(0)
    status_container = st.empty()
    results_container = st.empty()
    
    processed = []
    failed = []
    skipped = []
    
    for idx, file in enumerate(files):
        # Update progress
        progress = (idx + 1) / total_files
        progress_bar.progress(progress)
        progress_text.text(f"Processing {idx + 1} of {total_files}: {file.name}")
        
        # Show processing status
        status_container.info(f"🔄 Processing: {truncate_text(file.name, 40)}")
        
        # Process file with enhanced error handling
        try:
            result = process_single_contract_advanced(file)
            if result:
                processed.append(file.name)
            else:
                failed.append(file.name)
        except Exception as e:
            failed.append(file.name)
            st.error(f"❌ Error processing {file.name}: {str(e)}")
        
        # Update results
        with results_container:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"✅ {len(processed)} processed")
            with col2:
                st.caption(f"❌ {len(failed)} failed")
            with col3:
                st.caption(f"⏭️ {len(skipped)} skipped")
    
    # Final progress
    progress_bar.progress(1.0)
    progress_text.success("✅ Processing Complete!")
    
    # Final results summary
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ Successfully Processed", len(processed), delta=f"{len(processed)/total_files*100:.0f}%")
    with col2:
        st.metric("❌ Failed", len(failed), delta_color="inverse")
    with col3:
        st.metric("📊 Total", total_files)
    
    if failed:
        with st.expander("⚠️ Failed Files Details"):
            for f in failed:
                st.write(f"❌ {f}")
    
    if len(processed) > 0:
        st.success(f"🎉 Successfully processed {len(processed)} contract(s)!")
        time.sleep(0.5)
        st.rerun()


def process_single_contract_advanced(file) -> bool:
    """
    Process a single contract with enhanced validation and error handling
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Start timing for performance tracking
        start_time = time.time()
        
        # 1. Enhanced validation
        is_valid, message = validate_file(file)
        if not is_valid:
            st.warning(f"⚠️ Skipping {file.name}: {message}")
            return False
        
        # 2. Check for duplicates with content hash
        file_content = file.read()
        file_hash = hashlib.md5(file_content).hexdigest()
        file.seek(0)  # Reset file pointer
        
        for existing in st.session_state.contracts:
            if hasattr(existing, 'file_hash') and existing.file_hash == file_hash:
                st.warning(f"⚠️ Skipping {file.name}: Duplicate content detected")
                return False
        
        # 3. Parse document
        file_extension = os.path.splitext(file.name)[1].lower().replace('.', '')
        file_size = len(file_content)
        
        parser = DocumentParser()
        text, pages, is_scanned = parser.parse_file(file_content, file_extension)
        
        # 4. Validate extracted text
        if not text or len(text.strip()) < 10:
            st.error(f"❌ {file.name}: Could not extract text. This may be a scanned document.")
            return False
        
        # 5. Create contract with enhanced metadata
        contract_id = generate_id(f"{file.name}_{int(time.time())}")
        
        contract = Contract(
            id=contract_id,
            name=file.name,
            file_type=file_extension,
            file_size=file_size,
            upload_date=datetime.now(),
            text=text,
            pages=pages,
            is_scanned=is_scanned,
            file_hash=file_hash,
            metadata={
                'processing_time': time.time() - start_time,
                'word_count': len(text.split()),
                'character_count': len(text)
            }
        )
        
        # 6. Extract clauses with progress
        extractor = ClauseExtractor()
        clauses = extractor.extract_all_clauses(text, contract.id, contract.name)
        for clause in clauses:
            contract.add_clause(clause)
            st.session_state.clauses.append(clause)
        
        # 7. Scan for risks
        scanner = RiskScanner(st.session_state.risk_rules)
        risks = scanner.scan_contract(contract)
        for risk in risks:
            contract.add_risk(risk)
            st.session_state.risks.append(risk)
        
        # 8. Store contract
        st.session_state.contracts.append(contract)
        st.session_state.upload_count += 1
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error processing {file.name}: {str(e)}")
        return False


def render_contract_management():
    """Render smart contract management interface"""
    st.markdown("### 📋 Uploaded Contracts")
    st.caption(f"{len(st.session_state.contracts)} contracts loaded")
    
    # Search and filter
    search_col, filter_col, sort_col = st.columns([3, 1, 1])
    
    with search_col:
        search_term = st.text_input("🔍 Search contracts", placeholder="Search by name...", key="contract_search")
    
    with filter_col:
        file_type_filter = st.selectbox(
            "📁 Type",
            ["All", "PDF", "DOCX", "TXT"],
            key="file_type_filter"
        )
    
    with sort_col:
        sort_by = st.selectbox(
            "↕️ Sort",
            ["Newest First", "Oldest First", "Name A-Z", "Size", "Clauses"],
            key="sort_contracts"
        )
    
    # Filter and sort
    filtered_contracts = st.session_state.contracts.copy()
    
    if search_term:
        filtered_contracts = [c for c in filtered_contracts if search_term.lower() in c.name.lower()]
    
    if file_type_filter != "All":
        filtered_contracts = [c for c in filtered_contracts if c.file_type.upper() == file_type_filter]
    
    if sort_by == "Newest First":
        filtered_contracts.sort(key=lambda c: c.upload_date, reverse=True)
    elif sort_by == "Oldest First":
        filtered_contracts.sort(key=lambda c: c.upload_date)
    elif sort_by == "Name A-Z":
        filtered_contracts.sort(key=lambda c: c.name.lower())
    elif sort_by == "Size":
        filtered_contracts.sort(key=lambda c: c.file_size, reverse=True)
    elif sort_by == "Clauses":
        filtered_contracts.sort(key=lambda c: c.clause_count, reverse=True)
    
    # Display contracts in a clean list
    for contract in filtered_contracts:
        render_contract_item(contract)
    
    # Bulk actions
    if len(st.session_state.contracts) > 1:
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
                if st.session_state.contracts:
                    st.session_state.contracts = []
                    st.session_state.clauses = []
                    st.session_state.risks = []
                    st.success("✅ All contracts cleared")
                    st.rerun()
        with col2:
            if st.button("📊 Export Summary", use_container_width=True):
                export_contract_summary()


def render_contract_item(contract):
    """Render a single contract item with clean UI"""
    
    # Determine status
    risk_count = contract.risk_count
    if risk_count == 0:
        risk_status = "✅ Low Risk"
        risk_color = "green"
    elif risk_count < 3:
        risk_status = "⚠️ Medium Risk"
        risk_color = "orange"
    else:
        risk_status = "🔴 High Risk"
        risk_color = "red"
    
    icon = FILE_TYPE_ICONS.get(contract.file_type, "📄")
    
    # Use columns for clean layout
    with st.container():
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{icon} {contract.name}**")
            st.caption(f"📄 {contract.pages} pages • 📝 {contract.clause_count} clauses")
            if contract.is_scanned:
                st.caption("📷 Scanned PDF")
        
        with col2:
            st.caption(f"Risk: {risk_status}")
        
        with col3:
            if st.button("📄 View", key=f"view_{contract.id}", use_container_width=True):
                with st.expander(f"📄 {contract.name}", expanded=True):
                    st.text_area("Contract Text", contract.text[:1000] + ("..." if len(contract.text) > 1000 else ""), height=200)
        
        with col4:
            if st.button("📋 Clauses", key=f"clauses_{contract.id}", use_container_width=True):
                st.session_state.page = "Clause Library"
                st.session_state.filter_contract = contract.id
                st.rerun()
        
        with col5:
            if st.button("🗑️", key=f"delete_{contract.id}", use_container_width=True):
                st.session_state.contracts.remove(contract)
                st.session_state.clauses = [c for c in st.session_state.clauses if c.contract_id != contract.id]
                st.session_state.risks = [r for r in st.session_state.risks if r.contract_id != contract.id]
                st.success(f"✅ Deleted: {contract.name}")
                st.rerun()


def render_contracts_full():
    """Render when contract limit is reached"""
    st.warning(f"⚠️ You have reached the maximum limit of {LIMITS['max_contracts']} contracts.")
    
    st.markdown("### 📋 Current Contracts")
    for idx, contract in enumerate(st.session_state.contracts):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"📄 {contract.name}")
        with col2:
            st.caption(f"{contract.clause_count} clauses")
        with col3:
            st.caption(f"{contract.risk_count} risks")
        with col4:
            if st.button("🗑️", key=f"delete_full_{contract.id}_{idx}"):
                st.session_state.contracts.pop(idx)
                st.session_state.clauses = [c for c in st.session_state.clauses if c.contract_id != contract.id]
                st.session_state.risks = [r for r in st.session_state.risks if r.contract_id != contract.id]
                st.success(f"✅ Deleted: {contract.name}")
                st.rerun()
    
    if st.button("🗑️ Clear All Contracts", type="secondary", use_container_width=True):
        st.session_state.contracts = []
        st.session_state.clauses = []
        st.session_state.risks = []
        st.success("✅ All contracts cleared")
        st.rerun()


def render_empty_state():
    """Render empty state with guidance"""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 60px 20px;
        background: #FFFFFF;
        border-radius: 24px;
        border: 2px dashed #E2E8F0;
        margin: 20px 0;
    ">
        <div style="font-size: 64px; margin-bottom: 16px;">📭</div>
        <h3 style="color: #0A2647; margin: 0;">No Contracts Uploaded Yet</h3>
        <p style="color: #475569; margin: 8px 0;">
            Upload your first contract to get started with AI-powered contract intelligence
        </p>
        <div style="display: flex; gap: 12px; justify-content: center; margin-top: 16px;">
            <span style="
                background: #E8F1F8;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 13px;
                color: #2C5F8A;
            ">📄 PDF</span>
            <span style="
                background: #E8F1F8;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 13px;
                color: #2C5F8A;
            ">📝 DOCX</span>
            <span style="
                background: #E8F1F8;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 13px;
                color: #2C5F8A;
            ">📃 TXT</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Load Demo Contracts", use_container_width=True):
            from ..data.demo_data import load_demo_contracts
            load_demo_contracts()
            st.session_state.demo_mode = True
            st.success("✅ Demo contracts loaded successfully!")
            st.rerun()


def export_contract_summary():
    """Export contract summary as CSV"""
    data = []
    for contract in st.session_state.contracts:
        data.append({
            'Name': contract.name,
            'Type': contract.file_type.upper(),
            'Pages': contract.pages,
            'Clauses': contract.clause_count,
            'Risks': contract.risk_count,
            'Size': format_file_size(contract.file_size),
            'Uploaded': contract.upload_date.strftime('%Y-%m-%d %H:%M'),
            'Scanned': 'Yes' if contract.is_scanned else 'No'
        })
    
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Summary CSV",
        data=csv,
        file_name=f"contract_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )


def get_memory_usage() -> float:
    """Estimate memory usage percentage"""
    try:
        import psutil
        import os
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        limit_mb = LIMITS.get('max_memory_mb', 1024)
        return (memory_mb / limit_mb) * 100
    except:
        # Fallback estimation based on contract count
        total = len(st.session_state.contracts)
        return min((total / LIMITS["max_contracts"]) * 100, 95)