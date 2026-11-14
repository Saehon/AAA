"""Pure, fail-closed research artifact checks and offline reviewer workflows."""
from __future__ import annotations
from urllib.parse import urlparse
import re
DOI_RE=re.compile(r'^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$', re.IGNORECASE)
LICENSE_APPROVED={'CC0-1.0','CC-BY-4.0','CC-BY-SA-4.0','MIT','Apache-2.0','BSD-3-Clause'}
RISK_FIELDS={'contains_personal_data','contains_confidential_data','contains_restricted_license','requires_paid_vendor','untrusted_executable'}

def audit_research_asset(record:dict)->dict:
    if not isinstance(record,dict):raise ValueError('Record object required')
    required={'title','record_url','asset_type','license','source_inspected','license_inspected'}
    allowed=required|RISK_FIELDS|{'doi','publisher','journal','publication_year','code_url','data_url'}
    if set(record)-allowed:raise ValueError('Unsupported fields are not accepted')
    if not required<=set(record):raise ValueError('Missing title/URL/type/license/inspection fields')
    if record['asset_type'] not in {'article','preprint','thesis','code','dataset'}:raise ValueError('Asset type unsupported')
    if any(type(record.get(s,False)) is not bool for s in RISK_FIELDS|{'source_inspected','license_inspected'}):raise ValueError('Safety and inspection flags must be booleans')
    if any(record.get(s) for s in RISK_FIELDS):return {'status':'BLOCKED','reason':'Sensitive, vendor restricted or untrusted executable','reuse_permitted':False}
    for key in ['record_url','code_url','data_url']:
        value=record.get(key)
        if value is not None and (not isinstance(value,str) or urlparse(value).scheme!='https' or not urlparse(value).hostname):raise ValueError('HTTPS evidence links required')
    if 'doi' in record and record['doi'] and (not isinstance(record['doi'],str) or not DOI_RE.fullmatch(record['doi'])):raise ValueError('DOI syntax invalid; DOI resolution not asserted')
    safe_license=record['license'] in LICENSE_APPROVED
    independently_reviewed=record['source_inspected'] and record['license_inspected']
    status='ELIGIBLE_FOR_HUMAN_REUSE_REVIEW' if independently_reviewed and safe_license else 'NEEDS_SOURCE_OR_LICENSE_REVIEW'
    return {'title':record['title'],'status':status,'reuse_permitted':False,
            'license_label':record['license'],'license_allowlist_candidate':safe_license,
            'evidence_inspected_by_declared_reviewer_not_independently_verified':record['source_inspected'],
            'license_inspected_by_declared_reviewer_not_independently_verified':record['license_inspected'],
            'doi_syntax_valid_not_resolved':bool(record.get('doi')),
            'requires_manual_rights_review':True,'code_executed':False,'dataset_downloaded':False,
            'publication_placement_verified':False}

def research_scout(*, topic:str, platforms:list[str]|None=None, years:int=4)->dict:
    if not isinstance(topic,str) or not 5<=len(topic.strip())<=500:raise ValueError('Research topic length out of range')
    if not isinstance(years,int) or isinstance(years,bool) or not 1<=years<=15:raise ValueError('Unsupported year window')
    allowed={'OpenAlex','Crossref','SSRN','GitHub','Kaggle','Hugging Face','Zenodo','Harvard Dataverse','University thesis repositories','SEC EDGAR'}
    p=platforms or ['OpenAlex','Crossref','SSRN','GitHub','Zenodo','University thesis repositories']
    if not isinstance(p,list) or not p or len(p)!=len(set(p)) or any(x not in allowed for x in p):raise ValueError('Unknown research catalog')
    return {'topic':topic.strip(),'requested_year_window':years,'discovery_platforms':p,
            'ft50_register_status':'journal names only, paper-by-paper verification required',
            'ajg4_register_status':'selected accounting/finance subset only; NOT complete list',
            'search_executed':False,'paper_matches':[], 'data_downloads':[],
            'required_metadata':['DOI or repository identifier','title, authors and published year','journal and AJG/FT50 edition','data and code provenance','reuse licence and permissions','research design','empirical population','result independent replication'],
            'status':'OFFLINE_SEARCH_PLAN_NOT_RESULTS'}

def co_scientist_review(proposal:dict)->dict:
    allowed={'title','question','hypotheses','data_source','identification_strategy','outcomes','code_repository'}
    if not isinstance(proposal,dict) or set(proposal)-allowed or not {'title','question','hypotheses','data_source','identification_strategy'}<=set(proposal):raise ValueError('Proposal required')
    if not isinstance(proposal['hypotheses'],list) or not proposal['hypotheses'] or any(not isinstance(x,str) or not x.strip() for x in proposal['hypotheses']):raise ValueError('Non-empty hypotheses required')
    for x in ['title','question','data_source','identification_strategy']:
        if not isinstance(proposal[x],str) or not 3<=len(proposal[x])<=500:raise ValueError('Proposal string missing or too long')
    tasks=[
      {'role':'Generation','next_action':'Search original FT50/AJG peer-reviewed and SSRN/thesis literature for the exact construct and relationship'},
      {'role':'Reflection/Falsification','next_action':'List rival explanations, endogeneity, measurement error, omitted confounders and leakage'},
      {'role':'Ranking','next_action':'Compare preregistered candidates on novelty, causal credibility, accessible data and implementability'},
      {'role':'Evolution','next_action':'Propose a minimal testable improvement, preserving the original benchmark baseline'},
      {'role':'Reproducibility','next_action':'Pin open data and code IDs, licences, dependencies, seed, environment and evaluation metrics'},
      {'role':'Meta-review','next_action':'Request independent qualified human review and define clear rejection conditions'}
    ]
    return {'proposal':proposal,'tasks':tasks,'agent_execution':'NOT_RUN_WORKFLOW_SPECIFICATION',
            'google_co_scientist_called':False,'google_alphaevolve_called':False,'science_discovery_verified':False,
            'novelty_verified':False,'hypothesis_supported':None,'data_access_verified':False,
            'replication_code_executed':False,'peer_review_complete':False,
            'next_gate':'Search and independently inspect original literature and data; do not treat generated ideas as discoveries'}
