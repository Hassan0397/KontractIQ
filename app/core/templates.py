"""
KontractIQ - Contract Template Logic
6 complete templates for all use cases
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re

# ============================================================================
# BASE TEMPLATE CLASS
# ============================================================================

class ContractTemplate:
    """Base class for contract templates"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.fields = {}
        self.warnings = []
    
    def validate(self, field_values: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate field values and return warnings
        
        Returns:
            List of warning dictionaries with field, value, and message
        """
        warnings = []
        
        # Check for required fields
        for field_name, field_config in self.fields.items():
            if field_config.get('required', False):
                value = field_values.get(field_name)
                if not value or (isinstance(value, str) and not value.strip()):
                    warnings.append({
                        'field': field_name,
                        'message': f'{field_config["label"]} is required',
                        'severity': 'error'
                    })
        
        # Check numeric ranges
        for field_name, field_config in self.fields.items():
            if field_config.get('type') == 'number':
                value = field_values.get(field_name)
                if value is not None:
                    min_val = field_config.get('min')
                    max_val = field_config.get('max')
                    if min_val is not None and value < min_val:
                        warnings.append({
                            'field': field_name,
                            'message': f'{field_config["label"]} must be at least {min_val}',
                            'severity': 'error'
                        })
                    if max_val is not None and value > max_val:
                        warnings.append({
                            'field': field_name,
                            'message': f'{field_config["label"]} must be at most {max_val}',
                            'severity': 'error'
                        })
        
        return warnings
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate contract text from field values"""
        raise NotImplementedError("Subclasses must implement generate()")


# ============================================================================
# NDA (UNILATERAL) TEMPLATE
# ============================================================================

class NDAUnilateralTemplate(ContractTemplate):
    """Unilateral NDA template"""
    
    def __init__(self):
        super().__init__(
            name="NDA (Unilateral)",
            description="One-way non-disclosure agreement"
        )
        self.fields = {
            'disclosing_party': {
                'type': 'text',
                'label': 'Disclosing Party',
                'required': True,
                'placeholder': 'Company A',
                'help': 'The party disclosing confidential information'
            },
            'receiving_party': {
                'type': 'text',
                'label': 'Receiving Party',
                'required': True,
                'placeholder': 'Company B',
                'help': 'The party receiving confidential information'
            },
            'purpose': {
                'type': 'textarea',
                'label': 'Purpose',
                'required': False,
                'placeholder': 'Describe the purpose of the NDA',
                'help': 'The business purpose for sharing confidential information'
            },
            'confidentiality_period': {
                'type': 'number',
                'label': 'Confidentiality Period (years)',
                'required': True,
                'default': 3,
                'min': 1,
                'max': 10,
                'help': 'How long confidentiality obligations survive'
            },
            'term_years': {
                'type': 'number',
                'label': 'Term (years)',
                'required': True,
                'default': 2,
                'min': 1,
                'max': 10,
                'help': 'Duration of the agreement'
            },
            'governing_law': {
                'type': 'select',
                'label': 'Governing Law',
                'required': True,
                'options': ['California', 'New York', 'Delaware', 'Texas', 'Florida'],
                'default': 'California',
                'help': 'Jurisdiction that will govern the agreement'
            },
            'include_exclusions': {
                'type': 'checkbox',
                'label': 'Include Exclusions',
                'default': True,
                'help': 'Standard exclusions for publicly available information'
            },
            'include_return': {
                'type': 'checkbox',
                'label': 'Include Return of Information',
                'default': True,
                'help': 'Require return or destruction of confidential information'
            }
        }
    
    def validate(self, field_values: Dict[str, Any]) -> List[Dict[str, Any]]:
        warnings = super().validate(field_values)
        
        # Check confidentiality period
        conf_period = field_values.get('confidentiality_period', 0)
        if conf_period < 1:
            warnings.append({
                'field': 'confidentiality_period',
                'message': 'Confidentiality period should be at least 1 year',
                'severity': 'warning'
            })
        
        # Check term
        term = field_values.get('term_years', 0)
        if term < 1:
            warnings.append({
                'field': 'term_years',
                'message': 'Term should be at least 1 year',
                'severity': 'warning'
            })
        
        # Check if term > confidentiality period
        if conf_period > term:
            warnings.append({
                'field': 'confidentiality_period',
                'message': f'Confidentiality period ({conf_period} years) is longer than the agreement term ({term} years)',
                'severity': 'warning'
            })
        
        return warnings
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate unilateral NDA text"""
        disclosing = field_values.get('disclosing_party', '[DISCLOSING PARTY]')
        receiving = field_values.get('receiving_party', '[RECEIVING PARTY]')
        purpose = field_values.get('purpose', 'exploring a potential business relationship')
        conf_period = field_values.get('confidentiality_period', 3)
        term = field_values.get('term_years', 2)
        law = field_values.get('governing_law', 'California')
        include_exclusions = field_values.get('include_exclusions', True)
        include_return = field_values.get('include_return', True)
        
        today = datetime.now().strftime('%B %d, %Y')
        
        return f"""
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (the "Agreement") is entered into as of {today} 
between {disclosing} ("Disclosing Party") and {receiving} ("Receiving Party").

1. PURPOSE
The Disclosing Party desires to disclose certain confidential information to the Receiving Party 
for the purpose of: {purpose}

2. CONFIDENTIAL INFORMATION
"Confidential Information" means any information disclosed by the Disclosing Party, in any form, 
that is designated as confidential or would reasonably be understood to be confidential.

3. CONFIDENTIALITY OBLIGATIONS
The Receiving Party agrees to:
(a) Hold all Confidential Information in strict confidence
(b) Use Confidential Information solely for the Purpose
(c) Not disclose Confidential Information to any third party
(d) Use at least the same degree of care to protect Confidential Information as it uses for its own confidential information

4. EXCLUSIONS
{'Confidential Information does not include information that: (a) is or becomes publicly available through no fault of the Receiving Party, (b) was known to the Receiving Party prior to disclosure, (c) is independently developed by the Receiving Party without use of Confidential Information, or (d) is required to be disclosed by law.' if include_exclusions else ''}

5. CONFIDENTIALITY PERIOD
The confidentiality obligations shall survive for a period of {conf_period} years from the Effective Date.

6. RETURN OF INFORMATION
{'Upon termination of this Agreement or upon written request, the Receiving Party shall promptly return or destroy all Confidential Information and certify such return or destruction.' if include_return else ''}

7. TERM
This Agreement shall remain in effect for {term} years from the Effective Date.

8. GOVERNING LAW
This Agreement shall be governed by the laws of {law}.

9. SEVERABILITY
If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions shall remain in full force and effect.

10. ENTIRE AGREEMENT
This Agreement constitutes the entire agreement between the parties regarding the subject matter hereof.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

________________________________
{disclosing}

By: __________________________
Title: _______________________
Date: ________________________

________________________________
{receiving}

By: __________________________
Title: _______________________
Date: ________________________
"""


# ============================================================================
# NDA (MUTUAL) TEMPLATE
# ============================================================================

class NDAMutualTemplate(ContractTemplate):
    """Mutual NDA template"""
    
    def __init__(self):
        super().__init__(
            name="NDA (Mutual)",
            description="Two-way non-disclosure agreement"
        )
        self.fields = {
            'party_a': {
                'type': 'text',
                'label': 'Party A',
                'required': True,
                'placeholder': 'Company A',
                'help': 'First party to the agreement'
            },
            'party_b': {
                'type': 'text',
                'label': 'Party B',
                'required': True,
                'placeholder': 'Company B',
                'help': 'Second party to the agreement'
            },
            'purpose': {
                'type': 'textarea',
                'label': 'Purpose',
                'required': False,
                'placeholder': 'Describe the purpose of the NDA',
                'help': 'The business purpose for sharing confidential information'
            },
            'confidentiality_period': {
                'type': 'number',
                'label': 'Confidentiality Period (years)',
                'required': True,
                'default': 3,
                'min': 1,
                'max': 10,
                'help': 'How long confidentiality obligations survive'
            },
            'term_years': {
                'type': 'number',
                'label': 'Term (years)',
                'required': True,
                'default': 2,
                'min': 1,
                'max': 10,
                'help': 'Duration of the agreement'
            },
            'governing_law': {
                'type': 'select',
                'label': 'Governing Law',
                'required': True,
                'options': ['California', 'New York', 'Delaware', 'Texas', 'Florida'],
                'default': 'California',
                'help': 'Jurisdiction that will govern the agreement'
            }
        }
    
    def validate(self, field_values: Dict[str, Any]) -> List[Dict[str, Any]]:
        warnings = super().validate(field_values)
        
        # Check if parties are different
        party_a = field_values.get('party_a', '').strip().lower()
        party_b = field_values.get('party_b', '').strip().lower()
        if party_a and party_b and party_a == party_b:
            warnings.append({
                'field': 'party_b',
                'message': 'Party A and Party B must be different entities',
                'severity': 'error'
            })
        
        return warnings
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate mutual NDA text"""
        party_a = field_values.get('party_a', '[PARTY A]')
        party_b = field_values.get('party_b', '[PARTY B]')
        purpose = field_values.get('purpose', 'exploring a potential business relationship')
        conf_period = field_values.get('confidentiality_period', 3)
        term = field_values.get('term_years', 2)
        law = field_values.get('governing_law', 'California')
        
        today = datetime.now().strftime('%B %d, %Y')
        
        return f"""
MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into as of {today} 
between {party_a} and {party_b} (collectively, the "Parties").

1. PURPOSE
The Parties wish to disclose certain confidential information to each other for the purpose of: {purpose}

2. CONFIDENTIAL INFORMATION
"Confidential Information" means any information disclosed by either Party, in any form, 
that is designated as confidential or would reasonably be understood to be confidential.

3. MUTUAL CONFIDENTIALITY OBLIGATIONS
Each Party agrees to:
(a) Hold all Confidential Information of the other Party in strict confidence
(b) Use Confidential Information solely for the Purpose
(c) Not disclose Confidential Information to any third party
(d) Use at least the same degree of care to protect Confidential Information as it uses for its own confidential information

4. EXCLUSIONS
Confidential Information does not include information that: (a) is or becomes publicly available through no fault of the Receiving Party, (b) was known to the Receiving Party prior to disclosure, (c) is independently developed by the Receiving Party without use of Confidential Information, or (d) is required to be disclosed by law.

5. CONFIDENTIALITY PERIOD
The confidentiality obligations shall survive for a period of {conf_period} years from the Effective Date.

6. RETURN OF INFORMATION
Upon termination of this Agreement or upon written request, each Party shall promptly return or destroy all Confidential Information of the other Party and certify such return or destruction.

7. TERM
This Agreement shall remain in effect for {term} years from the Effective Date.

8. GOVERNING LAW
This Agreement shall be governed by the laws of {law}.

9. NO LICENSE
Nothing in this Agreement grants either Party any license or rights to the other Party's intellectual property.

10. ENTIRE AGREEMENT
This Agreement constitutes the entire agreement between the Parties regarding the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first above written.

________________________________
{party_a}

By: __________________________
Title: _______________________
Date: ________________________

________________________________
{party_b}

By: __________________________
Title: _______________________
Date: ________________________
"""


# ============================================================================
# MASTER SERVICES AGREEMENT TEMPLATE
# ============================================================================

class MSATemplate(ContractTemplate):
    """Master Services Agreement template"""
    
    def __init__(self):
        super().__init__(
            name="Master Services Agreement",
            description="Master Services Agreement for ongoing vendor relationships"
        )
        self.fields = {
            'service_provider': {
                'type': 'text',
                'label': 'Service Provider',
                'required': True,
                'placeholder': 'Service Provider Name',
                'help': 'The company providing services'
            },
            'client': {
                'type': 'text',
                'label': 'Client',
                'required': True,
                'placeholder': 'Client Name',
                'help': 'The company receiving services'
            },
            'services_description': {
                'type': 'textarea',
                'label': 'Services Description',
                'required': True,
                'placeholder': 'Describe the services to be provided in detail',
                'help': 'Detailed description of services to be performed'
            },
            'payment_terms': {
                'type': 'number',
                'label': 'Payment Terms (days)',
                'required': True,
                'default': 30,
                'min': 7,
                'max': 90,
                'help': 'Number of days to pay invoices'
            },
            'liability_cap': {
                'type': 'text',
                'label': 'Liability Cap',
                'required': True,
                'placeholder': 'e.g., $1,000,000 or amount of fees paid',
                'help': 'Maximum liability exposure'
            },
            'governing_law': {
                'type': 'select',
                'label': 'Governing Law',
                'required': True,
                'options': ['California', 'New York', 'Delaware', 'Texas', 'Florida'],
                'default': 'California',
                'help': 'Jurisdiction that will govern the agreement'
            },
            'auto_renewal': {
                'type': 'checkbox',
                'label': 'Auto-Renewal',
                'default': False,
                'help': '⚠️ Auto-renewal may lock you into the agreement'
            }
        }
    
    def validate(self, field_values: Dict[str, Any]) -> List[Dict[str, Any]]:
        warnings = super().validate(field_values)
        
        # Check for auto-renewal warning
        if field_values.get('auto_renewal', False):
            warnings.append({
                'field': 'auto_renewal',
                'message': 'Auto-renewal clause may lock you into the agreement - consider adding termination for convenience',
                'severity': 'warning'
            })
        
        # Check payment terms
        payment_terms = field_values.get('payment_terms', 30)
        if payment_terms < 15:
            warnings.append({
                'field': 'payment_terms',
                'message': f'Short payment terms ({payment_terms} days) may impact cash flow - consider 30+ days',
                'severity': 'warning'
            })
        elif payment_terms > 60:
            warnings.append({
                'field': 'payment_terms',
                'message': f'Long payment terms ({payment_terms} days) may impact cash flow for service provider',
                'severity': 'info'
            })
        
        # Check liability cap
        liability_cap = field_values.get('liability_cap', '').lower()
        if 'unlimited' in liability_cap:
            warnings.append({
                'field': 'liability_cap',
                'message': '⚠️ UNLIMITED liability detected - this is a significant risk! Consider capping liability.',
                'severity': 'critical'
            })
        elif not re.search(r'\$[\d,]+', liability_cap) and not re.search(r'[\d,]+', liability_cap):
            warnings.append({
                'field': 'liability_cap',
                'message': 'Consider specifying a clear liability cap amount',
                'severity': 'info'
            })
        
        return warnings
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate MSA text"""
        provider = field_values.get('service_provider', '[SERVICE PROVIDER]')
        client = field_values.get('client', '[CLIENT]')
        services = field_values.get('services_description', '[DESCRIPTION OF SERVICES]')
        payment = field_values.get('payment_terms', 30)
        liability = field_values.get('liability_cap', '$1,000,000')
        law = field_values.get('governing_law', 'California')
        auto_renewal = field_values.get('auto_renewal', False)
        
        today = datetime.now().strftime('%B %d, %Y')
        
        return f"""
MASTER SERVICES AGREEMENT

This Master Services Agreement (the "MSA") is made as of {today} between {provider} 
("Service Provider") and {client} ("Client").

1. SERVICES
Service Provider shall provide the following services: {services}

2. PAYMENT TERMS
Client shall pay Service Provider within {payment} days of receipt of invoice. 
Invoices shall be submitted monthly or as agreed in writing.

3. LIABILITY CAP
Service Provider's liability under this Agreement shall not exceed {liability}.
This limitation shall not apply to: (a) breach of confidentiality, (b) breach of intellectual property rights, 
or (c) gross negligence or willful misconduct.

4. TERM AND TERMINATION
This Agreement shall remain in effect until terminated by either party with 30 days written notice.
{'This Agreement will automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least 60 days prior to the end of the then-current term.' if auto_renewal else ''}

5. GOVERNING LAW
This Agreement shall be governed by the laws of {law}.

6. INDEPENDENT CONTRACTOR
Service Provider is an independent contractor and not an employee of Client.

7. CONFIDENTIALITY
Each party shall maintain the confidentiality of the other party's confidential information.

8. INSURANCE
Service Provider shall maintain appropriate insurance coverage as required by law.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

________________________________
{provider}

By: __________________________
Title: _______________________
Date: ________________________

________________________________
{client}

By: __________________________
Title: _______________________
Date: ________________________
"""


# ============================================================================
# INDEPENDENT CONTRACTOR AGREEMENT TEMPLATE
# ============================================================================

class IndependentContractorTemplate(ContractTemplate):
    """Independent Contractor Agreement template"""
    
    def __init__(self):
        super().__init__(
            name="Independent Contractor Agreement",
            description="Freelancers and consultants"
        )
        self.fields = {
            'company': {
                'type': 'text',
                'label': 'Company',
                'required': True,
                'placeholder': 'Company Name',
                'help': 'The hiring company'
            },
            'contractor': {
                'type': 'text',
                'label': 'Contractor',
                'required': True,
                'placeholder': 'Contractor Name',
                'help': 'The independent contractor'
            },
            'services': {
                'type': 'textarea',
                'label': 'Services',
                'required': True,
                'placeholder': 'Describe the services to be provided',
                'help': 'Detailed description of work to be performed'
            },
            'payment_rate': {
                'type': 'text',
                'label': 'Payment Rate',
                'required': True,
                'placeholder': 'e.g., $100/hour or $5,000/month',
                'help': 'Compensation rate for services'
            },
            'payment_terms': {
                'type': 'number',
                'label': 'Payment Terms (days)',
                'required': True,
                'default': 30,
                'min': 7,
                'max': 90,
                'help': 'Number of days to pay invoices'
            },
            'project_duration_months': {
                'type': 'number',
                'label': 'Project Duration (months)',
                'required': True,
                'default': 6,
                'min': 1,
                'max': 36,
                'help': 'Expected duration of the engagement'
            },
            'governing_law': {
                'type': 'select',
                'label': 'Governing Law',
                'required': True,
                'options': ['California', 'New York', 'Delaware', 'Texas', 'Florida'],
                'default': 'California',
                'help': 'Jurisdiction that will govern the agreement'
            }
        }
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate Independent Contractor Agreement text"""
        company = field_values.get('company', '[COMPANY]')
        contractor = field_values.get('contractor', '[CONTRACTOR]')
        services = field_values.get('services', '[SERVICES]')
        rate = field_values.get('payment_rate', '[RATE]')
        payment = field_values.get('payment_terms', 30)
        duration = field_values.get('project_duration_months', 6)
        law = field_values.get('governing_law', 'California')
        
        today = datetime.now().strftime('%B %d, %Y')
        
        return f"""
INDEPENDENT CONTRACTOR AGREEMENT

This Independent Contractor Agreement (the "Agreement") is made as of {today} between {company} 
("Company") and {contractor} ("Contractor").

1. SERVICES
Contractor shall provide the following services: {services}

2. COMPENSATION
Company shall pay Contractor at the rate of {rate}. Invoices shall be submitted monthly and 
paid within {payment} days of receipt.

3. TERM
This Agreement shall remain in effect for {duration} months from the Effective Date, 
unless earlier terminated by either party with 30 days written notice.

4. INDEPENDENT CONTRACTOR STATUS
Contractor is an independent contractor and not an employee of Company. 
Contractor shall be responsible for all taxes, insurance, and benefits.

5. CONFIDENTIALITY
Contractor shall maintain the confidentiality of Company's confidential information.

6. INTELLECTUAL PROPERTY
All work product created by Contractor shall be the exclusive property of Company.

7. GOVERNING LAW
This Agreement shall be governed by the laws of {law}.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

________________________________
{company}

By: __________________________
Title: _______________________
Date: ________________________

________________________________
{contractor}

Date: ________________________
"""


# ============================================================================
# EMPLOYMENT OFFER LETTER TEMPLATE
# ============================================================================

class EmploymentOfferTemplate(ContractTemplate):
    """Employment Offer Letter template"""
    
    def __init__(self):
        super().__init__(
            name="Employment Offer Letter",
            description="Hiring employees"
        )
        self.fields = {
            'company_name': {
                'type': 'text',
                'label': 'Company Name',
                'required': True,
                'placeholder': 'Company Name',
                'help': 'The hiring company'
            },
            'candidate_name': {
                'type': 'text',
                'label': 'Candidate Name',
                'required': True,
                'placeholder': 'Candidate Full Name',
                'help': 'The candidate being hired'
            },
            'position': {
                'type': 'text',
                'label': 'Position',
                'required': True,
                'placeholder': 'Job Title',
                'help': 'The position being offered'
            },
            'start_date': {
                'type': 'text',
                'label': 'Start Date',
                'required': True,
                'placeholder': 'e.g., January 15, 2024',
                'help': 'Expected start date'
            },
            'salary': {
                'type': 'text',
                'label': 'Salary',
                'required': True,
                'placeholder': 'e.g., $100,000 per year',
                'help': 'Annual salary or hourly rate'
            },
            'employment_type': {
                'type': 'select',
                'label': 'Employment Type',
                'required': True,
                'options': ['Full-Time', 'Part-Time', 'Contract', 'Internship'],
                'default': 'Full-Time',
                'help': 'Type of employment'
            },
            'governing_law': {
                'type': 'select',
                'label': 'Governing Law',
                'required': True,
                'options': ['California', 'New York', 'Delaware', 'Texas', 'Florida'],
                'default': 'California',
                'help': 'Jurisdiction that will govern the agreement'
            }
        }
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate Employment Offer Letter text"""
        company = field_values.get('company_name', '[COMPANY]')
        candidate = field_values.get('candidate_name', '[CANDIDATE]')
        position = field_values.get('position', '[POSITION]')
        start_date = field_values.get('start_date', '[START DATE]')
        salary = field_values.get('salary', '[SALARY]')
        emp_type = field_values.get('employment_type', 'Full-Time')
        law = field_values.get('governing_law', 'California')
        
        today = datetime.now().strftime('%B %d, %Y')
        
        return f"""
EMPLOYMENT OFFER LETTER

Date: {today}

Dear {candidate},

We are pleased to offer you the position of {position} at {company}. 
We are excited about the potential value you can bring to our team.

POSITION DETAILS
- Position: {position}
- Employment Type: {emp_type}
- Start Date: {start_date}
- Salary: {salary}
- Reporting To: [Manager Name]
- Work Location: [Office Location]

BENEFITS
[Standard benefits package details to be added]

CONDITIONS OF EMPLOYMENT
This offer is subject to: (a) successful completion of background check, 
(b) verification of eligibility to work, and (c) execution of confidentiality agreement.

ACCEPTANCE
Please sign and return this offer letter by [Acceptance Date] to indicate your acceptance.

GOVERNING LAW
This Agreement shall be governed by the laws of {law}.

We look forward to welcoming you to our team!

Sincerely,

________________________________
[Hiring Manager Name]
{company}

ACCEPTANCE

I, {candidate}, accept the offer of employment as set forth above.

________________________________
{candidate}

Date: ________________________
"""


# ============================================================================
# SOFTWARE LICENSE AGREEMENT TEMPLATE
# ============================================================================

class SoftwareLicenseTemplate(ContractTemplate):
    """Software License Agreement template"""
    
    def __init__(self):
        super().__init__(
            name="Software License Agreement",
            description="Software sales and licensing"
        )
        self.fields = {
            'licensor': {
                'type': 'text',
                'label': 'Licensor',
                'required': True,
                'placeholder': 'Software Company Name',
                'help': 'The software provider'
            },
            'licensee': {
                'type': 'text',
                'label': 'Licensee',
                'required': True,
                'placeholder': 'Client Company Name',
                'help': 'The software user'
            },
            'software_name': {
                'type': 'text',
                'label': 'Software Name',
                'required': True,
                'placeholder': 'Product Name',
                'help': 'The software being licensed'
            },
            'license_type': {
                'type': 'select',
                'label': 'License Type',
                'required': True,
                'options': ['Perpetual', 'Annual Subscription', 'Monthly Subscription'],
                'default': 'Annual Subscription',
                'help': 'Type of license agreement'
            },
            'license_fee': {
                'type': 'text',
                'label': 'License Fee',
                'required': True,
                'placeholder': 'e.g., $10,000 per year',
                'help': 'License fee amount'
            },
            'payment_terms': {
                'type': 'number',
                'label': 'Payment Terms (days)',
                'required': True,
                'default': 30,
                'min': 7,
                'max': 90,
                'help': 'Number of days to pay invoices'
            },
            'governing_law': {
                'type': 'select',
                'label': 'Governing Law',
                'required': True,
                'options': ['California', 'New York', 'Delaware', 'Texas', 'Florida'],
                'default': 'California',
                'help': 'Jurisdiction that will govern the agreement'
            }
        }
    
    def validate(self, field_values: Dict[str, Any]) -> List[Dict[str, Any]]:
        warnings = super().validate(field_values)
        
        # Check license fee for proper format
        fee = field_values.get('license_fee', '')
        if fee and not re.search(r'\$[\d,]+', fee) and not re.search(r'[\d,]+', fee):
            warnings.append({
                'field': 'license_fee',
                'message': 'Consider specifying a clear license fee amount',
                'severity': 'info'
            })
        
        return warnings
    
    def generate(self, field_values: Dict[str, Any]) -> str:
        """Generate Software License Agreement text"""
        licensor = field_values.get('licensor', '[LICENSOR]')
        licensee = field_values.get('licensee', '[LICENSEE]')
        software = field_values.get('software_name', '[SOFTWARE]')
        license_type = field_values.get('license_type', 'Annual Subscription')
        fee = field_values.get('license_fee', '[FEE]')
        payment = field_values.get('payment_terms', 30)
        law = field_values.get('governing_law', 'California')
        
        today = datetime.now().strftime('%B %d, %Y')
        
        return f"""
SOFTWARE LICENSE AGREEMENT

This Software License Agreement (the "Agreement") is made as of {today} between {licensor} 
("Licensor") and {licensee} ("Licensee").

1. GRANT OF LICENSE
Licensor hereby grants Licensee a non-exclusive, non-transferable license to use the software 
known as {software} (the "Software") for internal business purposes only.

2. LICENSE TYPE
This license is a {license_type} license.

3. LICENSE FEE
Licensee shall pay Licensor the license fee of {fee}. Invoices shall be paid within {payment} days of receipt.

4. RESTRICTIONS
Licensee shall not: (a) copy, modify, or create derivative works of the Software, 
(b) reverse engineer, decompile, or disassemble the Software, or (c) sublicense, distribute, 
or rent the Software to third parties.

5. INTELLECTUAL PROPERTY
All intellectual property rights in the Software remain the exclusive property of Licensor.

6. WARRANTY AND LIABILITY
The Software is provided "as is" without warranty of any kind. Licensor's liability shall 
not exceed the license fees paid.

7. TERMINATION
This Agreement may be terminated by either party with 30 days written notice.

8. GOVERNING LAW
This Agreement shall be governed by the laws of {law}.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

________________________________
{licensor}

By: __________________________
Title: _______________________
Date: ________________________

________________________________
{licensee}

By: __________________________
Title: _______________________
Date: ________________________
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_templates() -> Dict[str, ContractTemplate]:
    """Get all available contract templates"""
    return {
        'NDA (Unilateral)': NDAUnilateralTemplate(),
        'NDA (Mutual)': NDAMutualTemplate(),
        'Master Services Agreement': MSATemplate(),
        'Independent Contractor Agreement': IndependentContractorTemplate(),
        'Employment Offer Letter': EmploymentOfferTemplate(),
        'Software License Agreement': SoftwareLicenseTemplate()
    }


def get_template_fields(template_name: str) -> Dict[str, Any]:
    """Get fields for a specific template"""
    templates = get_all_templates()
    template = templates.get(template_name)
    if template:
        return template.fields
    return {}


def validate_template_data(template_name: str, field_values: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate template data and return warnings"""
    templates = get_all_templates()
    template = templates.get(template_name)
    if template:
        return template.validate(field_values)
    return []


def generate_contract(template_name: str, field_values: Dict[str, Any]) -> str:
    """Generate a contract from a template"""
    templates = get_all_templates()
    template = templates.get(template_name)
    if template:
        return template.generate(field_values)
    return "Template not found."