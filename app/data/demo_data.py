"""
KontractIQ - Demo Data Loader
Optimized for performance and consistency
"""

import streamlit as st
from datetime import datetime
import random
import hashlib
from typing import List, Dict, Any, Optional
from ..models.contract import Contract
from ..models.clause import Clause
from ..models.risk import Risk
from ..utils.helpers import generate_id
from ..utils.constants import DEMO_CONTRACT_NAMES


# Pre-compiled demo contracts for performance
DEMO_CONTRACTS_DATA: List[Dict[str, Any]] = [
    {
        "name": "Acme_Software_License_Agreement.txt",
        "vendor": "Acme Corporation",
        "contract_value": 100000.0,
        "text": """
SOFTWARE LICENSE AGREEMENT

This Software License Agreement (the "Agreement") is entered into between Acme Corporation 
("Licensor") and Beta Technologies Inc. ("Licensee") on January 15, 2024.

1. GRANT OF LICENSE. Licensor hereby grants Licensee a non-exclusive, non-transferable 
license to use the Software for internal business purposes only.

2. PAYMENT TERMS. Licensee shall pay Licensor the sum of $100,000 annually. Payment shall 
be made within 30 days of receipt of invoice.

3. LIABILITY CAP. In no event shall Licensor's aggregate liability exceed $1,000,000.

4. GOVERNING LAW. This Agreement shall be governed by the laws of the State of California.

5. TERMINATION. This Agreement may be terminated by either party upon 60 days written notice.

6. CONFIDENTIALITY. Licensee agrees to maintain the confidentiality of the Software for 
a period of 5 years from the Effective Date.

7. INDEMNIFICATION. Licensee agrees to indemnify and hold harmless Licensor against any 
claims arising from Licensee's use of the Software.

8. FORCE MAJEURE. Neither party shall be liable for delays due to circumstances beyond 
their reasonable control.
""",
        "file_type": "txt",
        "pages": 1
    },
    {
        "name": "Beta_MSA_Agreement.txt",
        "vendor": "Gamma Consulting LLC",
        "contract_value": 150000.0,
        "text": """
MASTER SERVICES AGREEMENT

This Master Services Agreement (the "MSA") is made between Gamma Consulting LLC 
("Service Provider") and Delta Enterprises Inc. ("Client") on February 1, 2024.

1. SERVICES. Service Provider shall provide consulting services as described in 
Statements of Work executed by both parties.

2. FEES AND PAYMENT. Client shall pay Service Provider $150,000 monthly. Invoices 
are payable within 45 days of receipt.

3. LIABILITY. Service Provider's total liability under this Agreement shall not 
exceed $5,000,000, and in no event shall liability exceed the total fees paid.

4. GOVERNING LAW. This Agreement shall be governed by the laws of Delaware.

5. TERMINATION. Either party may terminate this Agreement for any reason with 
90 days advance written notice. The Agreement will automatically renew for 
successive one-year terms unless terminated.

6. CONFIDENTIALITY. The parties agree to keep all confidential information in 
strict confidence for 7 years from disclosure.

7. FORCE MAJEURE. Neither party shall be liable for delays due to circumstances 
beyond their reasonable control.
""",
        "file_type": "txt",
        "pages": 1
    },
    {
        "name": "Gamma_NDA_Agreement.txt",
        "vendor": "Epsilon Corporation",
        "contract_value": None,
        "text": """
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (the "NDA") is entered into by and between Epsilon Corporation 
("Disclosing Party") and Zeta Solutions Inc. ("Receiving Party") on March 1, 2024.

PURPOSE. The parties wish to explore a potential business relationship and may disclose 
confidential information for this purpose.

CONFIDENTIALITY OBLIGATIONS. The Receiving Party agrees to hold all Confidential Information 
in strict confidence and to use it solely for the Purpose. The confidentiality obligations 
shall survive for a period of 5 years.

GOVERNING LAW. This NDA shall be governed by the laws of New York.

TERM. This NDA shall remain in effect for 3 years from the Effective Date.
""",
        "file_type": "txt",
        "pages": 1
    },
    {
        "name": "Delta_Service_Agreement.txt",
        "vendor": "Theta Solutions",
        "contract_value": 75000.0,
        "text": """
SERVICE AGREEMENT

This Service Agreement is entered into between Theta Solutions ("Service Provider") 
and Iota Industries ("Client") on April 1, 2024.

1. SERVICES. Service Provider shall provide IT consulting services.

2. PAYMENT. Client shall pay $75,000 quarterly, payable within 30 days of invoice.

3. LIABILITY. Service Provider's liability shall be limited to $2,000,000.

4. GOVERNING LAW. This agreement shall be governed by Texas law.

5. TERMINATION. This agreement may be terminated with 60 days notice.

6. CONFIDENTIALITY. Confidentiality obligations survive for 3 years.

7. INDEMNIFICATION. Service Provider shall indemnify Client for any damages.

8. FORCE MAJEURE. Force majeure events shall excuse performance.
""",
        "file_type": "txt",
        "pages": 1
    },
    {
        "name": "Epsilon_Supply_Contract.txt",
        "vendor": "Kappa Manufacturing",
        "contract_value": 50000.0,
        "text": """
SUPPLY CONTRACT

This Supply Contract is entered into between Kappa Manufacturing ("Supplier") 
and Lambda Corporation ("Buyer") on May 1, 2024.

1. SUPPLY. Supplier shall deliver goods as specified in purchase orders.

2. PAYMENT. Buyer shall pay within 15 days of delivery.

3. LIABILITY. Supplier's liability shall not exceed $500,000.

4. GOVERNING LAW. This contract shall be governed by Florida law.

5. TERMINATION. This contract may be terminated with 30 days notice.

6. CONFIDENTIALITY. Confidentiality obligations survive for 5 years.

7. INDEMNIFICATION. Supplier shall indemnify Buyer for any claims.

8. FORCE MAJEURE. Force majeure shall excuse performance.
""",
        "file_type": "txt",
        "pages": 1
    }
]


def load_demo_contracts() -> bool:
    """
    Load sample contracts for demo mode - OPTIMIZED
    
    Returns:
        bool: True if demo loaded successfully, False otherwise
    """
    try:
        # Check if demo already loaded
        existing_demo = [
            c for c in st.session_state.get('contracts', [])
            if c.name in DEMO_CONTRACT_NAMES
        ]
        
        if existing_demo:
            st.warning("⚠️ Demo data already loaded. Clear existing data first.")
            return False
        
        # Clear any existing demo data first
        _clear_demo_data()
        
        # Import core modules (lazy import for performance)
        from ..core.extractor import ClauseExtractor
        from ..core.risk_scanner import RiskScanner
        
        extractor = ClauseExtractor()
        scanner = RiskScanner(st.session_state.get('risk_rules', {}))
        
        # Process each demo contract
        loaded_count = 0
        for demo_data in DEMO_CONTRACTS_DATA:
            contract = _create_contract_from_demo(demo_data)
            
            if contract:
                # Extract clauses
                clauses = extractor.extract_all_clauses(
                    contract.text,
                    contract.id,
                    contract.name
                )
                for clause in clauses:
                    contract.add_clause(clause)
                    st.session_state.clauses.append(clause)
                
                # Scan for risks
                risks = scanner.scan_contract(contract)
                for risk in risks:
                    contract.add_risk(risk)
                    st.session_state.risks.append(risk)
                
                # Add to session state
                st.session_state.contracts.append(contract)
                st.session_state.upload_count = st.session_state.get('upload_count', 0) + 1
                loaded_count += 1
        
        if loaded_count > 0:
            st.session_state.demo_mode = True
            st.success(f"✅ Successfully loaded {loaded_count} demo contracts!")
            return True
        else:
            st.error("❌ Failed to load demo contracts.")
            return False
            
    except Exception as e:
        st.error(f"❌ Error loading demo data: {str(e)}")
        return False


def _clear_demo_data() -> None:
    """Clear existing demo data from session - OPTIMIZED"""
    try:
        demo_contracts = [
            c for c in st.session_state.get('contracts', [])
            if c.name in DEMO_CONTRACT_NAMES
        ]
        
        for contract in demo_contracts:
            # Remove contract
            st.session_state.contracts = [
                c for c in st.session_state.contracts
                if c.id != contract.id
            ]
            
            # Remove associated clauses
            st.session_state.clauses = [
                c for c in st.session_state.get('clauses', [])
                if c.contract_id != contract.id
            ]
            
            # Remove associated risks
            st.session_state.risks = [
                r for r in st.session_state.get('risks', [])
                if r.contract_id != contract.id
            ]
        
        # Reset demo mode flag
        st.session_state.demo_mode = False
        
    except Exception as e:
        st.warning(f"Warning while clearing demo data: {str(e)}")


def _create_contract_from_demo(demo_data: Dict[str, Any]) -> Optional[Contract]:
    """
    Create a contract from demo data - OPTIMIZED
    
    Args:
        demo_data: Dictionary containing contract data
        
    Returns:
        Contract object or None if error
    """
    try:
        timestamp = int(datetime.now().timestamp())
        random_suffix = random.randint(1000, 9999)
        contract_id = generate_id(f"{demo_data['name']}_{timestamp}_{random_suffix}")
        
        # Generate file hash from text content
        file_hash = hashlib.md5(demo_data['text'].encode('utf-8')).hexdigest()
        
        return Contract(
            id=contract_id,
            name=demo_data['name'],
            file_type=demo_data['file_type'],
            file_size=len(demo_data['text'].encode('utf-8')),
            upload_date=datetime.now(),
            text=demo_data['text'],
            pages=demo_data.get('pages', 1),
            is_scanned=False,
            file_hash=file_hash,
            vendor=demo_data.get('vendor', None),
            contract_value=demo_data.get('contract_value', None)
        )
    except Exception as e:
        st.error(f"Error creating demo contract: {str(e)}")
        return None


def get_demo_status() -> bool:
    """
    Check if demo mode is active - OPTIMIZED
    
    Returns:
        bool: True if demo mode is active
    """
    return st.session_state.get('demo_mode', False)


def get_demo_contract_names() -> List[str]:
    """
    Get list of demo contract names - OPTIMIZED
    
    Returns:
        List of demo contract names
    """
    return DEMO_CONTRACT_NAMES.copy()


def clear_demo_data() -> bool:
    """
    Clear all demo data from session - OPTIMIZED
    
    Returns:
        bool: True if cleared successfully
    """
    try:
        _clear_demo_data()
        st.success("✅ Demo data cleared successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Error clearing demo data: {str(e)}")
        return False


def is_demo_contract(contract_name: str) -> bool:
    """
    Check if a contract is a demo contract - OPTIMIZED
    
    Args:
        contract_name: Name of the contract
        
    Returns:
        bool: True if it's a demo contract
    """
    return contract_name in DEMO_CONTRACT_NAMES


def get_demo_contract_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Get demo contract data by name - OPTIMIZED
    
    Args:
        name: Contract name
        
    Returns:
        Optional[Dict]: Demo contract data or None
    """
    for demo in DEMO_CONTRACTS_DATA:
        if demo['name'] == name:
            return demo
    return None