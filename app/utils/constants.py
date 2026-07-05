"""
KontractIQ - Application Constants
All configuration constants in one place 
"""

from typing import Dict, Any, List
from datetime import datetime  # Added for date/time operations

# ============================================================================
# COLOR SYSTEM - Complete Brand Colors
# ============================================================================

COLORS: Dict[str, Dict[str, str]] = {
    "primary": {
        "deepest_navy": "#0A2647",
        "rich_navy": "#1B3A5C",
        "corporate_blue": "#2C5F8A",
        "vibrant_blue": "#4A7FA5",
        "sky_blue": "#7BA5C4",
        "pale_blue": "#B8D4E8",
        "ice_blue": "#E8F1F8",
        "gradient_start": "#0A2647",
        "gradient_end": "#1B3A5C"
    },
    "neutrals": {
        "white": "#FFFFFF",
        "off_white": "#F8FAFE",
        "light_gray": "#E2E8F0",
        "medium_gray": "#94A3B8",
        "dark_gray": "#475569",
        "deep_navy": "#0A2647",
        "shadow": "rgba(10, 38, 71, 0.06)",
        "shadow_dark": "rgba(10, 38, 71, 0.12)"
    },
    "semantic": {
        "success": "#0D9488",
        "success_bg": "#E6F7F5",
        "success_light": "#CCF2EE",
        "success_dark": "#0A7A70",
        "warning": "#D97706",
        "warning_bg": "#FEF3C7",
        "warning_light": "#FDE68A",
        "warning_dark": "#B45309",
        "danger": "#DC2626",
        "danger_bg": "#FEE2E2",
        "danger_light": "#FCA5A5",
        "danger_dark": "#B91C1C",
        "info": "#3B82F6",
        "info_bg": "#EFF6FF",
        "info_light": "#93C5FD",
        "info_dark": "#2563EB"
    }
}

# ============================================================================
# TYPOGRAPHY SYSTEM
# ============================================================================

TYPOGRAPHY: Dict[str, Dict[str, Any]] = {
    "hero": {"size": 32, "weight": 700, "line_height": 1.2, "letter_spacing": -0.5},
    "display": {"size": 30, "weight": 600, "line_height": 1.3, "letter_spacing": -0.3},
    "title_1": {"size": 24, "weight": 600, "line_height": 1.4, "letter_spacing": -0.2},
    "title_2": {"size": 20, "weight": 600, "line_height": 1.4, "letter_spacing": -0.1},
    "headline": {"size": 18, "weight": 600, "line_height": 1.5},
    "body_large": {"size": 16, "weight": 500, "line_height": 1.6},
    "body": {"size": 14, "weight": 400, "line_height": 1.6},
    "small": {"size": 13, "weight": 500, "line_height": 1.5},
    "caption": {"size": 12, "weight": 500, "line_height": 1.4},
    "micro": {"size": 11, "weight": 400, "line_height": 1.3},
    "footer": {"size": 10, "weight": 500, "line_height": 1.2}
}

# ============================================================================
# SPACING SYSTEM
# ============================================================================

SPACING: Dict[str, int] = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 20,
    "xxl": 24,
    "xxxl": 32,
    "xxxxl": 48,
    "xxxxxl": 64
}

# ============================================================================
# BORDER RADIUS SYSTEM
# ============================================================================

BORDER_RADIUS: Dict[str, Any] = {
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 20,
    "xxl": 24,
    "xxxl": 32,
    "full": "50%"
}

# ============================================================================
# SHADOW SYSTEM
# ============================================================================

SHADOWS: Dict[str, str] = {
    "sm": "0 1px 3px rgba(10, 38, 71, 0.06)",
    "md": "0 4px 12px rgba(10, 38, 71, 0.08)",
    "lg": "0 8px 24px rgba(10, 38, 71, 0.10)",
    "xl": "0 16px 48px rgba(10, 38, 71, 0.12)",
    "xxl": "0 24px 64px rgba(10, 38, 71, 0.15)",
    "hover": "0 8px 32px rgba(10, 38, 71, 0.12)",
    "inner": "inset 0 2px 4px rgba(10, 38, 71, 0.04)"
}

# ============================================================================
# CONTRACT LIMITS
# ============================================================================

LIMITS: Dict[str, Any] = {
    "max_contracts": 20,
    "max_file_size_mb": 10,
    "max_pages": 50,
    "min_text_length": 100,
    "max_text_length": 100000,
    "max_clause_text_length": 1000,
    "max_preview_length": 200
}

# ============================================================================
# CLAUSE TYPES
# ============================================================================

CLAUSE_TYPES: List[str] = [
    "Governing Law",
    "Payment Terms",
    "Liability Cap",
    "Termination Notice",
    "Confidentiality Period",
    "Renewal Terms",
    "Indemnification",
    "Force Majeure"
]

CLAUSE_TYPE_ICONS: Dict[str, str] = {
    "Governing Law": "⚖️",
    "Payment Terms": "💰",
    "Liability Cap": "🛡️",
    "Termination Notice": "📅",
    "Confidentiality Period": "🔒",
    "Renewal Terms": "🔄",
    "Indemnification": "🛡️",
    "Force Majeure": "🌪️"
}

CLAUSE_TYPE_COLORS: Dict[str, str] = {
    "Governing Law": "#2C5F8A",
    "Payment Terms": "#0D9488",
    "Liability Cap": "#D97706",
    "Termination Notice": "#4A7FA5",
    "Confidentiality Period": "#3B82F6",
    "Renewal Terms": "#D97706",
    "Indemnification": "#1B3A5C",
    "Force Majeure": "#475569"
}

CLAUSE_TYPE_DESCRIPTIONS: Dict[str, str] = {
    "Governing Law": "Jurisdiction and applicable laws",
    "Payment Terms": "Payment schedule and due dates",
    "Liability Cap": "Maximum liability exposure",
    "Termination Notice": "Notice period for termination",
    "Confidentiality Period": "Duration of confidentiality",
    "Renewal Terms": "Automatic renewal provisions",
    "Indemnification": "Indemnity obligations",
    "Force Majeure": "Unforeseeable events"
}

# ============================================================================
# RISK SEVERITY LEVELS
# ============================================================================

RISK_SEVERITIES: Dict[str, Dict[str, str]] = {
    "critical": {
        "label": "Critical",
        "color": "#DC2626",
        "bg": "#FEE2E2",
        "border": "#FCA5A5",
        "icon": "🔴",
        "priority": 1
    },
    "high": {
        "label": "High",
        "color": "#D97706",
        "bg": "#FEF3C7",
        "border": "#FDE68A",
        "icon": "🟠",
        "priority": 2
    },
    "medium": {
        "label": "Medium",
        "color": "#D97706",
        "bg": "#FEF3C7",
        "border": "#FDE68A",
        "icon": "🟡",
        "priority": 3
    },
    "low": {
        "label": "Low",
        "color": "#3B82F6",
        "bg": "#EFF6FF",
        "border": "#93C5FD",
        "icon": "🔵",
        "priority": 4
    }
}

# ============================================================================
# CONTRACT HEALTH STATUS
# ============================================================================

CONTRACT_STATUS_COLORS: Dict[str, str] = {
    "healthy": "#0D9488",
    "warning": "#D97706",
    "critical": "#DC2626",
    "scanned": "#3B82F6"
}

CONTRACT_STATUS_ICONS: Dict[str, str] = {
    "healthy": "✅",
    "warning": "⚠️",
    "critical": "🔴",
    "scanned": "📄"
}

CONTRACT_STATUS_LABELS: Dict[str, str] = {
    "healthy": "Healthy",
    "warning": "Needs Review",
    "critical": "Critical Issues",
    "scanned": "Scanned Document"
}

# ============================================================================
# DEFAULT RISK RULES
# ============================================================================

DEFAULT_RISK_RULES: Dict[str, Dict[str, str]] = {
    "unlimited_liability": {
        "pattern": r"unlimited liability",
        "severity": "critical",
        "description": "Unlimited liability clause found - high risk exposure"
    },
    "auto_renewal": {
        "pattern": r"auto-?renew|automatic renewal",
        "severity": "high",
        "description": "Auto-renewal clause detected - may lock you in"
    },
    "no_termination_convenience": {
        "pattern": r"no termination for convenience",
        "severity": "medium",
        "description": "Lacks termination for convenience - inflexible"
    },
    "broad_indemnification": {
        "pattern": r"indemnify.*(?:against all|any and all|without limitation)",
        "severity": "medium",
        "description": "Broad indemnification - potential liability"
    },
    "short_payment_terms": {
        "pattern": r"(7|10|14|15)\s*days",
        "severity": "medium",
        "description": "Short payment terms - cash flow impact"
    },
    "missing_governing_law": {
        "pattern": r"(?i)(?!.*governing law)",
        "severity": "low",
        "description": "No governing law clause - jurisdiction uncertainty",
        "is_negative": True
    },
    "missing_confidentiality": {
        "pattern": r"(?i)(?!.*confidential)",
        "severity": "low",
        "description": "No confidentiality duration specified",
        "is_negative": True
    }
}

# ============================================================================
# REPORT TYPES
# ============================================================================

REPORT_TYPES: Dict[str, str] = {
    "full_analysis": "📊 Full Analysis Report",
    "risk_summary": "⚠️ Risk Summary Report",
    "clause_comparison": "📋 Clause Comparison Report",
    "executive_summary": "📈 Executive Summary Report"
}

# ============================================================================
# REPORT DESCRIPTIONS
# ============================================================================

REPORT_DESCRIPTIONS: Dict[str, str] = {
    "full_analysis": "Complete analysis with all contracts, clauses, and risks",
    "risk_summary": "Focused report on risk findings by severity",
    "clause_comparison": "Compare clauses across all contracts",
    "executive_summary": "High-level metrics and key recommendations"
}

# ============================================================================
# TEMPLATE TYPES
# ============================================================================

TEMPLATES: List[str] = [
    "NDA (Unilateral)",
    "NDA (Mutual)",
    "Master Services Agreement",
    "Independent Contractor Agreement",
    "Employment Offer Letter",
    "Software License Agreement"
]

TEMPLATE_DESCRIPTIONS: Dict[str, str] = {
    "NDA (Unilateral)": "One-way non-disclosure agreement",
    "NDA (Mutual)": "Two-way non-disclosure agreement",
    "Master Services Agreement": "Ongoing vendor relationship",
    "Independent Contractor Agreement": "Freelancers and consultants",
    "Employment Offer Letter": "Hiring employees",
    "Software License Agreement": "Software sales and licensing"
}

# ============================================================================
# FILE TYPES
# ============================================================================

SUPPORTED_FILE_TYPES: Dict[str, str] = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain"
}

FILE_TYPE_ICONS: Dict[str, str] = {
    "pdf": "📄",
    "docx": "📝",
    "txt": "📃"
}

FILE_TYPE_DESCRIPTIONS: Dict[str, str] = {
    "pdf": "Portable Document Format (Text-based)",
    "docx": "Microsoft Word Document",
    "txt": "Plain Text File"
}

# ============================================================================
# DEMO CONTRACT NAMES
# ============================================================================

DEMO_CONTRACT_NAMES: List[str] = [
    "Acme_Software_License_Agreement.txt",
    "Beta_MSA_Agreement.txt",
    "Gamma_NDA_Agreement.txt",
    "Delta_Service_Agreement.txt",
    "Epsilon_Supply_Contract.txt"
]

# ============================================================================
# QUICK ACTIONS
# ============================================================================

QUICK_ACTIONS: List[Dict[str, str]] = [
    {"label": "Upload Contracts", "icon": "📤", "page": "Upload Contracts"},
    {"label": "Search Contracts", "icon": "🔍", "page": "Search"},
    {"label": "Generate Report", "icon": "📊", "page": "Reports"},
    {"label": "Scan Risks", "icon": "⚠️", "page": "RiskScan"},
    {"label": "Create Contract", "icon": "📝", "page": "Create Contract"},
    {"label": "View Metrics", "icon": "📈", "page": "System Metrics"}
]

# ============================================================================
# PRO TIPS
# ============================================================================

PRO_TIPS: List[str] = [
    "💡 Upload multiple contracts at once for cross-contract analysis",
    "🎯 Use the Search feature to find specific clauses across all contracts",
    "⚠️ Run RiskScan to identify high-risk clauses automatically",
    "📊 Generate professional reports for stakeholders and compliance",
    "🎮 Load demo data to explore all features without uploading",
    "🔒 Your data stays private - all processing is session-based",
    "📈 Check System Metrics to monitor memory usage and performance"
]

# ============================================================================
# UPLOAD STATUS MESSAGES
# ============================================================================

UPLOAD_STATUS_MESSAGES: List[str] = [
    "🔍 Analyzing file structure...",
    "📖 Extracting text content...",
    "🧠 Detecting clauses with AI...",
    "⚠️ Scanning for risks...",
    "✅ Processing complete!"
]

# ============================================================================
# MEMORY THRESHOLDS
# ============================================================================

MEMORY_THRESHOLDS: Dict[str, float] = {
    "warning": 60.0,
    "danger": 80.0,
    "critical": 90.0
}

# ============================================================================
# ANIMATION CONSTANTS
# ============================================================================

ANIMATIONS: Dict[str, str] = {
    "fast": "0.15s ease",
    "medium": "0.3s ease",
    "slow": "0.5s ease",
    "bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
}

# ============================================================================
# BREAKPOINTS
# ============================================================================

BREAKPOINTS: Dict[str, int] = {
    "mobile": 480,
    "tablet": 768,
    "desktop": 1024,
    "wide": 1440
}

# ============================================================================
# BATCH CONFIGURATION
# ============================================================================

BATCH_CONFIG: Dict[str, Any] = {
    "max_batch_size": 10,
    "parallel_processing": True,
    "timeout_seconds": 60,
    "chunk_size_mb": 2
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES: Dict[str, str] = {
    "file_too_large": "File exceeds maximum size limit",
    "unsupported_format": "Unsupported file format",
    "parsing_failed": "Failed to parse document",
    "empty_file": "File is empty or contains no text",
    "scan_failed": "Risk scanning failed",
    "clause_detection_failed": "Clause detection failed"
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES: Dict[str, str] = {
    "upload_success": "Contract uploaded successfully",
    "batch_upload_success": "Batch upload completed",
    "scan_complete": "Risk scan completed",
    "report_generated": "Report generated successfully",
    "search_complete": "Search completed"
}

# ============================================================================
# PROCESSING CONSTANTS
# ============================================================================

PROCESSING: Dict[str, Any] = {
    "max_batch_size": BATCH_CONFIG["max_batch_size"],
    "chunk_size": BATCH_CONFIG["chunk_size_mb"] * 1024 * 1024,
    "timeout_seconds": BATCH_CONFIG["timeout_seconds"],
    "parallel_enabled": BATCH_CONFIG["parallel_processing"]
}

# ============================================================================
# UI TEXT CONSTANTS
# ============================================================================

UI_TEXT: Dict[str, Dict[str, str]] = {
    "contract_explorer": {
        "title": "📄 Contract Explorer",
        "subtitle": "View, search, filter, and manage your contract portfolio",
        "no_contracts": "No contracts uploaded yet",
        "upload_first": "Upload your first contract or load demo data to explore the platform"
    },
    "filters": {
        "search": "🔍 Search Contracts",
        "file_type": "📂 File Type",
        "sort": "📊 Sort By",
        "health": "Health Status",
        "clause_type": "Contains Clause Type",
        "risk_severity": "Risk Severity",
        "date_range": "Upload Date Range"
    }
}

# ============================================================================
# SEARCH CONFIGURATION
# ============================================================================

SEARCH_CONFIG: Dict[str, Any] = {
    "default_top_k": 10,
    "max_top_k": 50,
    "min_top_k": 1,
    "min_score_threshold": 0.1,
    "enable_enhanced_search": True,
    "quick_searches": [
        "payment terms",
        "liability cap",
        "termination notice",
        "governing law",
        "confidentiality",
        "indemnification",
        "force majeure",
        "renewal"
    ],
    "search_suggestions": [
        "payment terms 30 days",
        "liability cap $1M",
        "termination notice 60 days",
        "governing law California",
        "confidentiality period 5 years",
        "auto renewal clause",
        "unlimited liability",
        "indemnification provision"
    ]
}

# ============================================================================
# SEARCH STATUS MESSAGES
# ============================================================================

SEARCH_MESSAGES: Dict[str, str] = {
    "indexing": "🔍 Indexing contracts for fast retrieval...",
    "searching": "🔍 Searching across your contract portfolio...",
    "no_results": "🔍 No results found. Try adjusting your search query or filters.",
    "results_found": "🎯 Found {count} results in {time:.2f}s",
    "empty_query": "⚠️ Please enter a search query",
    "filtered_results": "📊 Showing {shown} of {total} results (filtered)",
    "export_success": "✅ Results exported successfully!",
    "copy_success": "✅ Results copied to clipboard!"
}

# ============================================================================
# SEARCH FILTER LABELS
# ============================================================================

SEARCH_FILTERS: Dict[str, Dict[str, str]] = {
    "contract": {
        "label": "📄 Filter by Contract",
        "all_option": "All",
        "placeholder": "Select a contract..."
    },
    "file_type": {
        "label": "📂 Filter by File Type",
        "all_option": "All",
        "placeholder": "Select a file type..."
    },
    "clause_type": {
        "label": "📋 Filter by Clause Type",
        "all_option": "All",
        "placeholder": "Select a clause type..."
    },
    "date_range": {
        "label": "📅 Date Range",
        "all_option": "All Time",
        "placeholder": "Select date range..."
    }
}

# ============================================================================
# COMPARE PAGE CONFIGURATION
# ============================================================================

COMPARE_CONFIG: Dict[str, Any] = {
    "max_lines_display": 100,
    "max_modified_display": 30,
    "context_lines": 3,
    "similarity_threshold_high": 0.9,
    "similarity_threshold_medium": 0.7,
    "change_impact_low": 10,
    "change_impact_medium": 30,
    "change_impact_high": 50
}

# ============================================================================
# COMPARE STATUS MESSAGES
# ============================================================================

COMPARE_MESSAGES: Dict[str, str] = {
    "no_contracts": "📭 Need at least 2 contracts to compare. Upload more contracts!",
    "same_contract": "⚠️ Please select two different contracts to compare",
    "comparing": "🔍 Analyzing contract differences...",
    "complete": "✅ Comparison complete!",
    "no_changes": "✅ No changes detected - contracts are identical",
    "export_success": "✅ Report exported successfully!",
    "copy_success": "✅ Report copied to clipboard!"
}

# ============================================================================
# COMPARE CHANGE CATEGORIES
# ============================================================================

CHANGE_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "formatting": {
        "label": "📝 Formatting",
        "color": "#94A3B8",
        "description": "Whitespace and formatting changes"
    },
    "minor": {
        "label": "🟢 Minor",
        "color": "#0D9488",
        "description": "Minor wording or punctuation changes"
    },
    "significant": {
        "label": "🟡 Significant",
        "color": "#D97706",
        "description": "Substantive changes to content"
    },
    "major": {
        "label": "🔴 Major",
        "color": "#DC2626",
        "description": "Major structural or content changes"
    }
}

# ============================================================================
# COMPARE VERSION DIFFERENCES
# ============================================================================

VERSION_DIFFERENCES: Dict[str, Dict[str, Any]] = {
    "minor": {
        "label": "🟢 Minor Revision",
        "threshold": 10,
        "description": "Minor changes - likely formatting or wording updates"
    },
    "moderate": {
        "label": "🟡 Moderate Revision",
        "threshold": 50,
        "description": "Substantive changes - review recommended"
    },
    "major": {
        "label": "🔴 Major Revision",
        "threshold": 100,
        "description": "Major restructuring - comprehensive review required"
    }
}

# ============================================================================
# CROSSCHECK CONFIGURATION
# ============================================================================

CROSSCHECK_CONFIG: Dict[str, Any] = {
    "min_contracts": 2,
    "max_findings_display": 20,
    "severity_thresholds": {
        "critical": 50,  # percentage deviation
        "high": 25,
        "medium": 10,
        "low": 5
    },
    "detection_types": [
        "Payment Terms",
        "Liability Cap",
        "Termination Notice",
        "Governing Law",
        "Confidentiality Period",
        "Renewal Terms"
    ],
    "max_values_display": 10,
    "show_recommendations": True,
    "enable_export": True,
    "enable_visualization": True
}

# ============================================================================
# CROSSCHECK MESSAGES
# ============================================================================

CROSSCHECK_MESSAGES: Dict[str, str] = {
    "no_contracts": "📭 Need at least 2 contracts for cross-check analysis",
    "analyzing": "🔍 Analyzing contracts for inconsistencies...",
    "complete": "✅ Analysis complete! Found {count} inconsistency type(s)",
    "no_findings": "🎉 No inconsistencies found! All contracts are consistent.",
    "error": "⚠️ Error during analysis: {error}",
    "export_success": "✅ Report exported successfully!",
    "export_failed": "❌ Failed to export report",
    "clear_success": "✅ Results cleared successfully!"
}

# ============================================================================
# CROSSCHECK SEVERITY LABELS
# ============================================================================

CROSSCHECK_SEVERITY: Dict[str, Dict[str, str]] = {
    "critical": {
        "label": "🔴 Critical",
        "description": "Significant inconsistencies requiring immediate attention",
        "action": "Immediate review required"
    },
    "high": {
        "label": "🟠 High",
        "description": "Important inconsistencies that should be addressed soon",
        "action": "Priority review recommended"
    },
    "medium": {
        "label": "🟡 Medium",
        "description": "Moderate inconsistencies worth reviewing",
        "action": "Consider standardizing"
    },
    "low": {
        "label": "🟢 Low",
        "description": "Minor inconsistencies, low priority",
        "action": "Monitor for trends"
    },
    "none": {
        "label": "✅ Consistent",
        "description": "No inconsistencies detected",
        "action": "No action required"
    }
}

# ============================================================================
# CHAT CONFIGURATION
# ============================================================================

CHAT_CONFIG: Dict[str, Any] = {
    "max_context_contracts": 10,
    "max_context_chars": 3000,
    "max_history": 50,
    "temperature": 0.7,
    "max_tokens": 800,
    "model": "mixtral-8x7b-32768",
    "available_models": [
        "mixtral-8x7b-32768",
        "llama3-70b-8192",
        "gemma2-9b-it",
        "llama3-8b-8192"
    ],
    "quick_suggestions": [
        "What are the payment terms across all contracts?",
        "Show me contracts with unlimited liability",
        "Which contracts have auto-renewal clauses?",
        "Compare termination notice periods",
        "What are the governing laws in my contracts?",
        "Show me liability caps summary",
        "Which contracts have confidentiality issues?",
        "Summarize all indemnification clauses"
    ]
}

# ============================================================================
# CHAT MESSAGES
# ============================================================================

CHAT_MESSAGES: Dict[str, str] = {
    "no_contracts": "📭 No contracts uploaded yet. Upload contracts first to ask questions!",
    "no_api_key": "ℹ️ Using fallback mode (keyword matching)",
    "api_key_set": "✅ API key set successfully!",
    "api_key_removed": "🗑️ API key removed successfully",
    "api_key_invalid": "⚠️ Invalid or expired API key. Please check your Groq API key.",
    "rate_limit": "⏳ Rate limit exceeded. Please wait a moment and try again.",
    "groq_not_installed": "⚠️ Groq library not installed. Install it with: `pip install groq`",
    "no_results": "No results found. Try different keywords or enable AI with a Groq API key.",
    "clear_success": "✅ Chat history cleared!",
    "export_success": "✅ Chat history exported successfully!",
    "suggestions_title": "💡 Suggested Questions",
    "close_suggestions": "✕ Close Suggestions",
    "empty_chat": "💬 No messages yet. Ask a question about your contracts to get started."
}

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

PROMPT_TEMPLATES: Dict[str, str] = {
    "system_prompt": """You are a premium contract intelligence assistant for KontractIQ. 
Your expertise is in analyzing contracts, identifying key clauses, and providing actionable insights.

**Your Capabilities:**
- Analyze payment terms, liability caps, and termination clauses
- Identify risks and compliance issues
- Compare clauses across contracts
- Summarize complex legal language
- Provide practical recommendations

**Response Guidelines:**
1. Be specific and cite contract names
2. Use bullet points for clarity
3. Highlight risks and opportunities
4. Provide actionable recommendations
5. Use professional but accessible language
6. Include relevant clause references""",

    "context_template": """
📄 **Contract: {name}**
📋 Clauses: {clause_count} | ⚠️ Risks: {risk_count}
🏷️ Type: {file_type} | 📄 Pages: {pages}
{health_info}{vendor_info}

📝 **Content:**
{text}
""",

    "response_template": """
📋 **Analysis:**

{analysis}

📊 **Key Findings:**
{findings}

💡 **Recommendations:**
{recommendations}

---
⏱️ Response generated in {time}s
"""
}

# ============================================================================
# CHAT UI CONSTANTS
# ============================================================================

CHAT_UI: Dict[str, Dict[str, str]] = {
    "hero": {
        "title": "💬 AI Contract Assistant",
        "subtitle": "Ask questions about your contracts and get intelligent answers powered by AI"
    },
    "settings": {
        "title": "⚙️ Settings",
        "api_key": "🔑 API Key",
        "model": "🧠 Model",
        "advanced": "🔧 Advanced",
        "quick_actions": "🚀 Quick Actions"
    },
    "input": {
        "placeholder": "e.g., What are the payment terms across all contracts?",
        "ask_button": "💬 Ask",
        "clear_button": "🗑️"
    },
    "metrics": {
        "contracts": "📄 Contracts Available",
        "questions": "💬 Questions Asked",
        "status": "🤖 AI Status",
        "clauses": "📋 Total Clauses"
    }
}

# ============================================================================
# ANOMALY DETECTION CONFIGURATION
# ============================================================================

ANOMALY_CONFIG: Dict[str, Any] = {
    "min_contracts": 2,
    "payment_term_std_threshold": 1.5,
    "liability_cap_std_threshold": 1.5,
    "risk_density_std_threshold": 1.5,
    "length_std_threshold": 2.0,
    "max_payment_terms": 180,
    "min_contract_value": 10000,
    "common_laws": ['california', 'new york', 'delaware', 'texas', 'florida', 'illinois'],
    "anomaly_types": [
        "Unusual Payment Term",
        "Unusual Liability Cap",
        "Uncommon Governing Law",
        "Missing Clauses",
        "Excessive Clauses",
        "High Risk Density",
        "Contract Length Anomaly"
    ],
    "severity_weights": {
        "critical": 10,
        "high": 7,
        "medium": 4,
        "low": 1,
        "info": 0
    },
    "color_map": {
        "critical": "#DC2626",
        "high": "#D97706",
        "medium": "#D97706",
        "low": "#3B82F6",
        "info": "#94A3B8"
    },
    "bg_map": {
        "critical": "#FEE2E2",
        "high": "#FEF3C7",
        "medium": "#FEF3C7",
        "low": "#EFF6FF",
        "info": "#F8FAFE"
    },
    "icon_map": {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🔵",
        "info": "ℹ️"
    },
    "detection_types": [
        {
            "name": "Payment Terms",
            "icon": "💰",
            "description": "Unusual payment periods that deviate significantly from the norm",
            "severity_impact": "Can indicate cash flow issues or non-standard vendor relationships"
        },
        {
            "name": "Liability Caps",
            "icon": "🛡️",
            "description": "Liability limits that are significantly higher or lower than average",
            "severity_impact": "Indicates risk exposure differences across contracts"
        },
        {
            "name": "Governing Law",
            "icon": "⚖️",
            "description": "Uncommon jurisdictions that may pose compliance risks",
            "severity_impact": "Legal and compliance risk assessment"
        },
        {
            "name": "Clause Coverage",
            "icon": "📋",
            "description": "Contracts with missing or excessive clauses",
            "severity_impact": "Contract completeness and quality assessment"
        },
        {
            "name": "Risk Density",
            "icon": "⚠️",
            "description": "Unusually high concentration of risks in a contract",
            "severity_impact": "Risk management prioritization"
        },
        {
            "name": "Contract Length",
            "icon": "📄",
            "description": "Contracts that are unusually short or long",
            "severity_impact": "Contract complexity and review effort"
        }
    ]
}