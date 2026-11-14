"""Public-safe date-aware reporting research routing, not compliance/assurance validation."""
from __future__ import annotations
from datetime import date
from typing import Any

CUTOFF=date(2026,12,15)
ESRS_EFFECTIVE=date(2027,1,1)
ISSB_GHG_AMEND=date(2027,1,1)

def parse_date(value: str)->date:
    if not isinstance(value,str): raise ValueError('ISO date string required')
    try: return date.fromisoformat(value)
    except (TypeError,ValueError): raise ValueError('Invalid ISO date') from None

def assurance_transition(period_start:str, *, jurisdiction:str='IAASB_BASELINE', subject:str='sustainability', as_at:str|None=None)->dict[str,Any]:
    """Illustrative applicability gate. Never override jurisdiction-specific adoption."""
    start=parse_date(period_start)
    if subject not in ('sustainability','GHG','financial_audit'):
        raise ValueError('Unsupported engagement subject')
    if not isinstance(jurisdiction,str) or not jurisdiction.strip(): raise ValueError('Specify jurisdiction')
    if as_at is not None: parse_date(as_at)
    if subject=='financial_audit':
        return {'candidate':'FINANCIAL_AUDIT_STANDARDS_SEPARATE','jurisdiction':jurisdiction,'review_required':True,'basis':'PCAOB/ISA audit requirements differ from sustainability assurance'}
    reference_date=parse_date(as_at) if as_at else start
    future=reference_date>=CUTOFF
    return {'candidate':('ISSA_5000_IAASB_BASELINE' if future else 'ISAE_3410_GHG_HISTORICAL_CONTEXT' if subject=='GHG' else 'ISAE_3000_HISTORICAL_CONTEXT'),
            'jurisdiction':jurisdiction,'subject':subject,'reference_date':reference_date.isoformat(),
            'review_required':True,'legal_conclusion':False,'jurisdiction_adoption_verified':False,
            'warning':'Check local adoption, national transition, reporting period, early application and applicable ethical requirements; this is not an assurance opinion.'}

def reporting_version(reporting_start:str, *, jurisdiction:str, framework:str, early_adoption:bool=False)->dict[str,Any]:
    start=parse_date(reporting_start)
    if not jurisdiction:raise ValueError('Jurisdiction required')
    if framework=='ESRS':
        if start.year==2026:
            v='EU_2026_TRANSITION_OPTION_CHECK_REQUIRED'
        elif start>=ESRS_EFFECTIVE:v='REVISED_ESRS_2026_BASELINE'
        else:v='ESRS_PRIOR_REGIME_CHECK_REQUIRED'
    elif framework=='IFRS_S2_GHG_AMENDMENTS':v='AMENDED_IFRS_S2' if start>=ISSB_GHG_AMEND or early_adoption else 'PRE_2027_AMENDMENTS'
    elif framework=='ISSB_S1_S2':v='ISSB_STANDARDS_JURISDICTION_ADOPTION_REQUIRED'
    else:raise ValueError('Unsupported framework')
    return {'candidate_version':v,'jurisdiction':jurisdiction,'reporting_start':start.isoformat(),
            'mandatory_applicability_verified':False,'human_review_required':True}

def double_materiality_triage(record:dict[str,Any])->dict[str,Any]:
    """Never decide ESRS materiality; produce independent evidence flags."""
    if not isinstance(record,dict):raise ValueError('A topic record is required')
    allowed={'topic','financial_evidence','impact_evidence','stakeholder_evidence','threshold_method','reporting_period','source_url'}
    if set(record)-allowed:raise ValueError('Unsupported input fields')
    if not isinstance(record.get('topic'),str) or not record['topic'].strip(): raise ValueError('Topic required')
    for k in ('financial_evidence','impact_evidence','stakeholder_evidence'):
        if k in record and not isinstance(record[k],bool):raise ValueError('Evidence flags must be boolean')
    missing=[k for k in ('financial_evidence','impact_evidence','stakeholder_evidence','threshold_method','reporting_period','source_url') if not record.get(k)]
    return {'topic':record['topic'],'impact_materiality':'REQUIRES_HUMAN_ASSESSMENT','financial_materiality':'REQUIRES_HUMAN_ASSESSMENT',
            'potential_dimensions':[k.replace('_evidence','') for k in ('impact_evidence','financial_evidence') if record.get(k) is True],
            'missing_evidence':missing,'materiality_decision':None,'esrs_compliance_verified':False}

def evidence_passport(record:dict[str,Any])->dict[str,Any]:
    required={'claim','framework','report_period','source_url','source_inspected','evidence_type'}
    if not isinstance(record,dict) or set(record)-required or not required<=set(record):raise ValueError('Evidence passport requires exact documented fields')
    if not isinstance(record['source_inspected'],bool):raise ValueError('source_inspected must be boolean')
    if not isinstance(record['source_url'],str) or not record['source_url'].startswith('https://'):raise ValueError('HTTPS source URL required')
    if record['evidence_type'] not in ('public_source','synthetic','user_supplied'):raise ValueError('Unsupported evidence type')
    return {'claim':record['claim'],'framework':record['framework'],'report_period':record['report_period'],
            'source_url':record['source_url'],'evidence_level':'INSPECTED_BY_CALLER_ASSERTION_NOT_INDEPENDENTLY_AUTHENTICATED' if record['source_inspected'] else 'NOT_INSPECTED',
            'compliance_certified':False,'audit_opinion_issued':False,'human_review_required':True}
