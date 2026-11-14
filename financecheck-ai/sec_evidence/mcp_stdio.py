"""Opt-in local STDIO MCP demonstration of SEC XBRL evidence.

No live SEC retrieval occurs by default. Deployment to public ChatGPT/Claude
requires a separately hosted, authorized, security-reviewed remote MCP server.
"""
from __future__ import annotations
import json,sys
from typing import Any
from .verify import EvidenceError, verify_live_sec_claim, ALLOWED_CONCEPTS

PROTOCOL='2025-06-18'
VERSION='3.2.0'
CAP=16_384
PROPS={
  'cik': {'type':'string','pattern':'^[0-9]{1,10}$','description':'Public issuer SEC CIK; no private information'},
  'year':{'type':'integer','minimum':2009,'maximum':2026},
  'as_of':{'type':'string','pattern':'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
           'description':'Public information cut-off (YYYY-MM-DD)'},
  'concept':{'type':'string','enum':list(ALLOWED_CONCEPTS),
             'description':'Optional exact US-GAAP tag; if more than one tag qualifies, user selection is required'},
  'claimed_percentage':{'type':['string','number'],
          'description':'Optional company claim for evaluation against selected XBRL facts'},
}
TOOLS=[{
    'name':'inspect_sec_xbrl_revenue_yoy',
    'description':'OPTIONAL LIVE SEC API only when explicitly enabled: compute annual revenue YoY from SEC XBRL tagged facts. Returns accession, filing dates, source metadata and caveats. It does NOT inspect complete filing pages and is NOT connected to ChatGPT by this package.',
    'inputSchema':{'type':'object','properties':PROPS,'required':['cik','year','as_of'],'additionalProperties':False},
    'annotations':{'readOnlyHint':True,'destructiveHint':False,'openWorldHint':True}
}]

def handle(message:Any)->dict[str,Any]|None:
    if not isinstance(message,dict) or message.get('jsonrpc')!='2.0':
        return {'jsonrpc':'2.0','id':message.get('id') if isinstance(message,dict) else None,
                'error':{'code':-32600,'message':'Invalid JSON-RPC request'}}
    if 'id' not in message: return None
    identity=message.get('id'); method=message.get('method')
    if method=='initialize':
        result={'protocolVersion':PROTOCOL,'capabilities':{'tools':{'listChanged':False}},
                'serverInfo':{'name':'financecheck-sec-xbrl-reference','version':VERSION},
                'instructions':'Local opt-in SEC XBRL evidence. Disabled by default. Does not authenticate original full filing documents.'}
    elif method=='ping':result={}
    elif method=='tools/list':result={'tools':TOOLS}
    elif method=='tools/call':
        params=message.get('params')
        if not isinstance(params,dict) or params.get('name') != TOOLS[0]['name']:
            return {'jsonrpc':'2.0','id':identity,'error':{'code':-32602,'message':'Invalid tool call'}}
        args=params.get('arguments',{})
        if not isinstance(args,dict) or set(args)-set(PROPS) or not {'cik','year','as_of'}<=set(args):
            return {'jsonrpc':'2.0','id':identity,'error':{'code':-32602,'message':'Unknown or missing tool arguments'}}
        try:
            data=verify_live_sec_claim(**args)
            result={'content':[{'type':'text','text':json.dumps(data,ensure_ascii=False)}],
                    'structuredContent':data,'isError':False}
        except (EvidenceError, ValueError, TypeError):
            result={'content':[{'type':'text','text':'SEC verification unavailable or invalid request; no source evidence was authenticated.'}],
                    'isError':True}
    else:return {'jsonrpc':'2.0','id':identity,'error':{'code':-32601,'message':'Method not found'}}
    return {'jsonrpc':'2.0','id':identity,'result':result}

def main():
    for line in sys.stdin.buffer:
        if len(line)>CAP:
            sys.stdout.write(json.dumps({'jsonrpc':'2.0','id':None,
                                         'error':{'code':-32600,'message':'Message exceeds size limit'}})+'\n')
            sys.stdout.flush();continue
        try: request=json.loads(line)
        except (UnicodeDecodeError,json.JSONDecodeError):
            response={'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Invalid JSON'}}
        else:response=handle(request)
        if response is not None:
            sys.stdout.write(json.dumps(response,ensure_ascii=False)+'\n')
            sys.stdout.flush()
if __name__=='__main__':main()
