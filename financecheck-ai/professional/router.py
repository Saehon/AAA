"""Conservative deterministic educational routing: not regulatory advice or assurance."""
from __future__ import annotations
from pathlib import Path
import json, re
_BASE=Path(__file__).resolve().parent
_BODIES={x['id']:x for x in json.loads((_BASE/'professional_bodies.json').read_text())['bodies']}
_BIG4={x['firm'].lower():x for x in json.loads((_BASE/'big4_public_guidance.json').read_text())['firms']}
US={'US','USA','UNITED STATES'}
EU={'EU','EEA','SWEDEN','GERMANY','FRANCE','NETHERLANDS','ITALY','SPAIN'}

def professional_route(*, jurisdiction:str, domain:str, credential:str|None=None, listed_issuer:bool=False, framework:str|None=None)->dict:
    if not isinstance(jurisdiction,str) or not jurisdiction.strip() or len(jurisdiction)>80:raise ValueError('Specific jurisdiction required')
    if domain not in ('financial_reporting','external_audit','internal_audit','sustainability','fraud','management_accounting','it_audit'):raise ValueError('Domain not supported')
    if not isinstance(listed_issuer,bool):raise ValueError('listed_issuer must be boolean')
    if credential is not None and credential not in _BODIES:raise ValueError('Unknown professional body identifier')
    j=jurisdiction.upper().strip()
    primary={
      'financial_reporting':('IFRS Accounting Standards and local legal adoption' if j in EU else 'US GAAP/FASB and SEC rules' if j in US else 'Applicable financial reporting requirements for the jurisdiction'),
      'external_audit':('PCAOB auditing standards for SEC issuer audits' if listed_issuer and j in US else 'Applicable ISA or national auditing/assurance standards and ethics'),
      'internal_audit':'IIA 2024 Global Internal Audit Standards effective 2025-01-09, subject to applicable context',
      'sustainability':('ESRS and EU law only where in-scope' if j in EU else 'ISSB IFRS S1/S2 subject to jurisdictional adoption')+'; assurance standards separate',
      'fraud':'Relevant law/evidence rules; ACFE professional ethics are guidance, not legal verdicts',
      'management_accounting':'IMA/CIMA management accounting ethics and business guidance; local rules as applicable',
      'it_audit':'ISACA/IIA practices plus applicable regulatory controls',
    }
    return {'jurisdiction':jurisdiction,'domain':domain,'primary_authority_candidate':primary[domain],
       'credential':credential,'body_reference':_BODIES[credential] if credential else None,
       'framework_requested':framework,'listed_issuer':listed_issuer,'local_adoption_verified':False,
       'operative_version_verified':False,'professional_certification':False,'assurance_opinion':False,
       'next_evidence':['effective reporting date and jurisdiction','actual official primary standard','engagement and issuer status','underlying supporting public sources'],
       'secondary_guidance_policy':'Compare Big Four and membership guidance only after establishing primary official authority; never claim endorsed by them',
       'status':'REVIEW_ROUTING_ONLY_NOT_STANDARDS_COMPLIANCE'}

def public_big4_comparison(firms:list[str])->dict:
    if not isinstance(firms,list) or not 1<=len(firms)<=4 or len(firms)!=len(set(firms)):raise ValueError('List 1 to 4 unique firms')
    found=[]
    for firm in firms:
        if not isinstance(firm,str) or firm.lower() not in _BIG4:raise ValueError('Unknown Big Four firm')
        found.append(_BIG4[firm.lower()])
    return {'resources':found,'standards_replaced':False,'guidance_inspected_for_current_case':False,
       'conclusion':'SOURCE POINTERS ONLY: read each specific relevant public publication before making a technical comparison'}
