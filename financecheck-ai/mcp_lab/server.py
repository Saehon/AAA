"""FinanceCheck v3 reference MCP stdio JSON-RPC server.

Local demonstration only; NOT a hosted or connected ChatGPT/Claude service.
No external network, database, filesystem writes, or confidential input support.
Requires no dependencies other than Python 3.11+.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
import json
import sys
import re
from typing import Any

NAME = "financecheck-reference"
VERSION = "3.0.0"
PROTOCOL_VERSION = "2025-06-18"
MAX_MESSAGE_BYTES = 32768

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

def check_public_data(a:dict):
    if not isinstance(a,dict):
        raise ValueError("Tool arguments must be an object")
    if a.get('classification') not in ('public','synthetic'):
        raise ValueError("BLOCKED: choose public or synthetic classification")
    forbidden=('contains_personal_data','contains_confidential_data','licensed_restricted','private_repo','private_drive')
    if any(a.get(x) for x in forbidden):
        raise ValueError("BLOCKED: personal, confidential, private and restricted-licensed information not accepted")

def calculate(a:dict)->dict:
    check_public_data(a)
    for field in ('previous','current','period_previous','period_current','currency'):
        if not a.get(field) and a.get(field)!=0: raise ValueError(f"Missing required field: {field}")
    previous=decimal_value(a['previous']);current=decimal_value(a['current'])
    if previous<=0:raise ValueError("Previous revenue must be positive for comparable growth percentage")
    if current<0:raise ValueError("Revenue must be nonnegative")
    p0=str(a['period_previous']);p1=str(a['period_current'])
    if p0==p1 or not all(re.fullmatch(r'(?:FY)?\d{4}(?:-Q[1-4])?', v) for v in (p0,p1)):
        raise ValueError("Two distinct valid reporting periods are required, such as FY2025 or 2025-Q1")
    ccy=str(a['currency']).strip().upper()
    if not 3<=len(ccy)<=4 or not ccy.isalpha():raise ValueError("Currency must be a short alphabetic code")
    pct=(current-previous)/previous*100
    def s(d):return format(d.quantize(Decimal('0.01')),'f')
    return {'status':'CALCULATED_FROM_SUBMITTED_INPUTS','source_status':'NOT_INDEPENDENTLY_INSPECTED',
      'previous':str(previous),'current':str(current),'difference':s(current-previous),'percentage_change':s(pct),
      'period_previous':p0,'period_current':p1,'currency':ccy,'classification':a['classification'],
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
    check_public_data(a)
    term=str(a.get('term','')).strip().lower()
    if term not in TERMS:
        raise ValueError('Unsupported term. Choose: '+', '.join(sorted(TERMS)))
    definition,caution=TERMS[term]
    return {'term':term,'definition':definition,'caution':caution,'example_status':'GENERAL_EDUCATION','source_status':'NOT_A_COMPANY_FACT'}

TOOLS=[
{'name':'check_revenue_change','description':'Compute bounded year-over-year revenue arithmetic from public/synthetic caller-supplied figures; does NOT retrieve or authenticate corporate filings.','inputSchema':{'type':'object','properties':{'classification':{'type':'string','enum':['public','synthetic']},'previous':{'type':['number','string']},'current':{'type':['number','string']},'period_previous':{'type':'string'},'period_current':{'type':'string'},'currency':{'type':'string'}},'required':['classification','previous','current','period_previous','period_current','currency'],'additionalProperties':True}},
{'name':'make_finance_story_card','description':'Create three transparent, short-form educational financial story cards from unverified supplied public/synthetic figures; always labels missing original-source authentication.','inputSchema':{'type':'object','properties':{'classification':{'type':'string','enum':['public','synthetic']},'previous':{'type':['number','string']},'current':{'type':['number','string']},'period_previous':{'type':'string'},'period_current':{'type':'string'},'currency':{'type':'string'}},'required':['classification','previous','current','period_previous','period_current','currency'],'additionalProperties':True}},
{'name':'explain_finance_term','description':'Provide a short, original general explanation of selected finance terms, with a caution and no live company-data claim.','inputSchema':{'type':'object','properties':{'classification':{'type':'string','enum':['public','synthetic']},'term':{'type':'string'}},'required':['classification','term'],'additionalProperties':True}}
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
