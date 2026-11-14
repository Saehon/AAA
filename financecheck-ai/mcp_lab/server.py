"""FinanceCheck v3 reference MCP stdio JSON-RPC server.

Local demonstration only; NOT a hosted or connected ChatGPT/Claude service.
No external network, database, filesystem writes, or confidential input support.
Requires no dependencies other than Python 3.11+.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation, localcontext
import json
import sys
import re
from typing import Any

NAME = "financecheck-reference"
VERSION = "3.0.0"
PROTOCOL_VERSION = "2025-06-18"
MAX_MESSAGE_BYTES = 32768
# Strictly bound fields; a local educational tool must not silently accept
# unrelated sensitive payloads just because users classified the request public.
INPUT_SAFETY_FLAGS = ('contains_personal_data','contains_confidential_data','licensed_restricted','private_repo','private_drive')
CALC_FIELDS = frozenset(('classification','previous','current','period_previous','period_current','currency',*INPUT_SAFETY_FLAGS))
EXPLAIN_FIELDS = frozenset(('classification','term',*INPUT_SAFETY_FLAGS))
SUPPORTED_PERIOD_RE = re.compile(r'^(?:(?:FY)?(19\d\d|20\d\d))(?:-Q([1-4]))?$')

TERMS = {
  "revenue": ("Money a business earned by selling goods or services during a period, before expenses.", "Revenue is not the same thing as net profit."),
  "profit": ("The amount remaining after relevant expenses are deducted from revenue under an accounting definition.", "Always distinguish net profit from adjusted EBITDA and cash flow."),
  "cash flow": ("Cash received and paid during a period, which may differ from accounting profit.", "A profitable company can still experience cash shortages."),
  "accrual": ("Accounting for revenue or expenses in the period they are earned or incurred, not necessarily when cash moves.", "A credit sale can increase revenue before cash arrives."),
  "debt": ("An obligation to repay borrowed funds or certain other financing liabilities.", "Assess interest, maturities and liquidity, not just total debt."),
}

def decimal_value(value:Any)->Decimal:
    if isinstance(value,bool) or isinstance(value,(list,dict)) or value is None:
        raise ValueError("Financial inputs must be finite decimal numbers")
    try:
        d=Decimal(str(value))
    except (InvalidOperation,ValueError):
        raise ValueError("Financial inputs must be finite decimal numbers") from None
    if not d.is_finite() or abs(d) > Decimal('1e15'):
        raise ValueError("Numbers must be finite and within bounded demonstration range")
    return d

def check_public_data(a:dict, expected_fields:frozenset[str]):
    if not isinstance(a,dict):
        raise ValueError("Tool arguments must be an object")
    if len(json.dumps(a, ensure_ascii=False, default=str)) > MAX_MESSAGE_BYTES:
        raise ValueError("BLOCKED: input exceeds local tool size limit")
    unknown=set(a)-expected_fields
    if unknown:
        # Never echo the unknown key/value: it may contain personal information.
        raise ValueError("BLOCKED: input contains unsupported fields; provide only documented public/synthetic fields")
    if a.get('classification') not in ('public','synthetic'):
        raise ValueError("BLOCKED: choose public or synthetic classification")
    for field in INPUT_SAFETY_FLAGS:
        if field in a and not isinstance(a[field],bool):
            raise ValueError("BLOCKED: safety classification flags must be booleans")
    if any(a.get(x) for x in INPUT_SAFETY_FLAGS):
        raise ValueError("BLOCKED: personal, confidential, private and restricted-licensed information not accepted")
    # This is an input contract, not a personal-data detector or a filing authenticator.


def annual_or_same_quarter_yoy(previous_period:str,current_period:str):
    if previous_period == current_period:
        raise ValueError('Two distinct reporting periods are required')
    a=SUPPORTED_PERIOD_RE.fullmatch(previous_period)
    b=SUPPORTED_PERIOD_RE.fullmatch(current_period)
    if not a or not b:
        raise ValueError('Two valid reporting periods are required (FY2024/FY2025 or 2024-Q1/2025-Q1)')
    y0,q0=int(a.group(1)),a.group(2)
    y1,q1=int(b.group(1)),b.group(2)
    if y1 != y0+1 or q0 != q1:
        raise ValueError('Year-over-year periods must be consecutive years and the same quarter/annual basis')


def calculate(a:dict)->dict:
    check_public_data(a, CALC_FIELDS)
    for field in ('previous','current','period_previous','period_current','currency'):
        if not a.get(field) and a.get(field)!=0: raise ValueError(f"Missing required field: {field}")
    previous=decimal_value(a['previous']);current=decimal_value(a['current'])
    if previous<=0:raise ValueError("Previous revenue must be positive for comparable growth percentage")
    if previous<Decimal('0.000000001'):raise ValueError("Previous revenue below supported precision")
    if current<0:raise ValueError("Revenue must be nonnegative")
    p0=str(a['period_previous']);p1=str(a['period_current'])
    annual_or_same_quarter_yoy(p0,p1)
    ccy=str(a['currency']).strip().upper()
    if not re.fullmatch(r'[A-Z]{3}',ccy):
        raise ValueError("Currency must be a three-letter code (format checked, ISO validity not authenticated)")
    with localcontext() as ctx:
        ctx.prec=60
        pct=(current-previous)/previous*100
        def s(d):return format(d.quantize(Decimal('0.01')),'f')
        s_prev_diff=s(current-previous)
        s_pct=s(pct)
    return {'status':'CALCULATED_FROM_SUBMITTED_INPUTS','source_status':'NOT_INDEPENDENTLY_INSPECTED',
      'previous':str(previous),'current':str(current),'difference':s_prev_diff,'percentage_change':s_pct,
      'period_previous':p0,'period_current':p1,'currency':ccy,'currency_code_status':'FORMAT_ONLY_NOT_AUTHENTICATED','classification':a['classification'],
      'caveat':'Accurate arithmetic on supplied numbers does not authenticate a filing, validate comparable accounting definitions, or imply investment advice.'}

def story(a:dict)->dict:
    r=calculate(a)
    is_synthetic=a['classification']=='synthetic'
    label='FICTIONAL EDUCATIONAL EXAMPLE' if is_synthetic else 'PUBLIC INPUTS — NOT SOURCE VERIFIED'
    name='a fictional company' if is_synthetic else 'the company (source not verified)'
    pct=r['percentage_change']
    verb='increased' if Decimal(pct)>0 else ('decreased' if Decimal(pct)<0 else 'was unchanged')
    # No verified badge, and no claim beyond numerical inputs.
    cards=[
       {'title':'What changed?', 'body':f"Submitted revenue for {name} {verb} by {pct}% from {r['period_previous']} to {r['period_current']}.", 'label':label},
       {'title':'The calculation', 'body':f"{r['previous']} → {r['current']} {r['currency']}; difference {r['difference']} {r['currency']}. Same currency and revenue definition are assumed, not independently checked.", 'label':label},
       {'title':'Check the evidence', 'body':'This tool did not retrieve or authenticate the original annual report. Inspect the original public filing before treating this as a company fact.', 'label':label},
    ]
    return {'share_status':'ILLUSTRATIVE_ONLY' if is_synthetic else 'REQUIRES_ORIGINAL_SOURCE_REVIEW','cards':cards,
            'full_source':'No original filing inspected','synthetic':is_synthetic,'data_status':r['status'],
            'safe_caption':'Educational arithmetic. Figures are not independently verified. No investment recommendation.'}

def explain(a:dict)->dict:
    check_public_data(a, EXPLAIN_FIELDS)
    term=str(a.get('term','')).strip().lower()
    if term not in TERMS:
        raise ValueError('Unsupported term. Choose: '+', '.join(sorted(TERMS)))
    definition,caution=TERMS[term]
    return {'term':term,'definition':definition,'caution':caution,'example_status':'GENERAL_EDUCATION','source_status':'NOT_A_COMPANY_FACT'}

COMMON_SAFETY_PROPERTIES={x:{'type':'boolean','description':'If true, request is blocked; personal and restricted content is not supported.'} for x in INPUT_SAFETY_FLAGS}
FINANCE_PROPERTIES={
  'classification':{'type':'string','enum':['public','synthetic']},
  'previous':{'type':['number','string'],'description':'Prior-year revenue from user-supplied figures, not authenticated'},
  'current':{'type':['number','string'],'description':'Current-year revenue from user-supplied figures, not authenticated'},
  'period_previous':{'type':'string','maxLength':12,'description':'Prior year: 2024, FY2024 or 2024-Q1'},
  'period_current':{'type':'string','maxLength':12,'description':'Following comparable year, same annual/quarter format'},
  'currency':{'type':'string','minLength':3,'maxLength':3,'description':'Three-letter currency code, format check only'},
  **COMMON_SAFETY_PROPERTIES
}
READ_ONLY_ANNOTATIONS={'readOnlyHint':True,'destructiveHint':False,'openWorldHint':False}
TOOLS=[
 {'name':'check_revenue_change','description':'Calculate year-over-year revenue arithmetic from non-sensitive caller-supplied public/synthetic figures. NO filing lookup or verified company facts.','annotations':READ_ONLY_ANNOTATIONS,'inputSchema':{'type':'object','properties':FINANCE_PROPERTIES,'required':['classification','previous','current','period_previous','period_current','currency'],'additionalProperties':False}},
 {'name':'make_finance_story_card','description':'Create 3 short factual/fictional cards based solely on non-sensitive submitted numbers; do not claim independent verification.','annotations':READ_ONLY_ANNOTATIONS,'inputSchema':{'type':'object','properties':FINANCE_PROPERTIES,'required':['classification','previous','current','period_previous','period_current','currency'],'additionalProperties':False}},
 {'name':'explain_finance_term','description':'Offer brief definitions of supported general finance terms; no company, investment, or data retrieval claims.','annotations':READ_ONLY_ANNOTATIONS,'inputSchema':{'type':'object','properties':{'classification':{'type':'string','enum':['public','synthetic']},'term':{'type':'string','maxLength':30,'enum':list(TERMS)},**COMMON_SAFETY_PROPERTIES},'required':['classification','term'],'additionalProperties':False}}
]

REGISTRY={'check_revenue_change':calculate,'make_finance_story_card':story,'explain_finance_term':explain}

def respond(message:dict)->dict|None:
    if not isinstance(message,dict) or message.get('jsonrpc')!='2.0':
        return {'jsonrpc':'2.0','id':message.get('id') if isinstance(message,dict) else None,'error':{'code':-32600,'message':'Invalid JSON-RPC request'}}
    # Notifications have no id and must not receive a response.
    if 'id' not in message:return None
    ident=message.get('id');method=message.get('method');params=message.get('params') or {}
    if not isinstance(params,dict):
        return {'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'Invalid params object'}}
    try:
        if method=='initialize':
            result={'protocolVersion':PROTOCOL_VERSION,'capabilities':{'tools':{'listChanged':False}},'serverInfo':{'name':NAME,'version':VERSION},'instructions':'Reference-only local financial arithmetic. Do not claim that this server verifies original public filings or connects to third-party finance data.'}
        elif method=='ping':result={}
        elif method=='tools/list':result={'tools':TOOLS}
        elif method=='tools/call':
            name=params.get('name');arguments=params.get('arguments') or {}
            if name not in REGISTRY:raise KeyError('Unknown tool')
            try:
                data=REGISTRY[name](arguments)
                result={'content':[{'type':'text','text':json.dumps(data,ensure_ascii=False)}], 'structuredContent':data,'isError':False}
            except (ValueError,TypeError) as e:
                result={'content':[{'type':'text','text':str(e)}],'isError':True}
        else: return {'jsonrpc':'2.0','id':ident,'error':{'code':-32601,'message':'Method not found'}}
        return {'jsonrpc':'2.0','id':ident,'result':result}
    except KeyError:
        return {'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'Unknown tool name'}}

def main():
    for line in sys.stdin.buffer:
        if len(line)>MAX_MESSAGE_BYTES:
            sys.stdout.write(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Message too large'}})+'\n');sys.stdout.flush();continue
        try: msg=json.loads(line)
        except (json.JSONDecodeError,UnicodeDecodeError):
            sys.stdout.write(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Invalid JSON'}})+'\n');sys.stdout.flush();continue
        out=respond(msg)
        if out is not None:
            sys.stdout.write(json.dumps(out,ensure_ascii=False)+'\n');sys.stdout.flush()
if __name__=='__main__':main()
