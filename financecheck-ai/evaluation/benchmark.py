"""Evaluator for a future *human-labeled* public-filing benchmark.

Does not collect SEC filings, create human labels, run AI models, or verify URL
contents. A benchmark report is meaningful only after independent annotation.
"""
from __future__ import annotations
from collections import Counter
from decimal import Decimal
import csv
import json
import math
import pathlib
import sys
from typing import Any

VERDICTS={'SUPPORTED','CONTRADICTED','INSUFFICIENT_EVIDENCE'}
STRATA={
    'revenue_growth':40,
    'income_adjusted_metric':40,
    'operating_cashflow':40,
    'liquidity_and_debt':40,
    'restatement_period_and_unit':40,
}

def make_sampling_plan(path: str | pathlib.Path) -> None:
    """200 EMPTY sampling slots. They are NOT sourced/verified observations."""
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['case_id','stratum','company_cik','claim_text','fiscal_year','source_filing_url',
                    'gold_verdict','annotator_a','annotator_b','adjudicator','label_status'])
        for stratum,n in STRATA.items():
            for j in range(1,n+1):
                w.writerow([f'{stratum[:3].upper()}-{j:03d}',stratum,'','','','','','','','','TO_COLLECT'])

def load_jsonl(path: str | pathlib.Path) -> list[dict[str,Any]]:
    out=[]
    with open(path,encoding='utf-8') as f:
        for lineno,line in enumerate(f,1):
            if not line.strip():continue
            obj=json.loads(line)
            if not isinstance(obj,dict):raise ValueError(f'JSONL record {lineno} must be an object')
            out.append(obj)
    return out

def wilson_95(correct:int,total:int) -> dict[str,float] | None:
    if total==0:return None
    z=1.959963984540054
    p=correct/total
    den=1+z*z/total
    c=(p+z*z/(2*total))/den
    h=z*math.sqrt(p*(1-p)/total+z*z/(4*total*total))/den
    return {'low':round(max(0,c-h),4),'high':round(min(1,c+h),4)}

def evaluate(gold: list[dict[str,Any]], predictions: list[dict[str,Any]], *,
             require_200: bool=True) -> dict[str,Any]:
    """Quality metrics on adjudicated labels only, no model invocation or citation fetch."""
    ids=[str(x.get('case_id','')) for x in gold]
    if len(set(ids))!=len(ids) or not all(ids):raise ValueError('Gold case ids must be unique and nonempty')
    ps=[str(x.get('case_id','')) for x in predictions]
    if len(set(ps))!=len(ps) or not all(ps):raise ValueError('Prediction case ids must be unique and nonempty')
    if require_200 and len(gold)!=200:raise ValueError('A publishable benchmark requires 200 independently labeled public cases')
    for x in gold:
        if x.get('stratum') not in STRATA:raise ValueError('Unknown benchmark stratum')
        if x.get('gold_verdict') not in VERDICTS:raise ValueError('Missing or unsupported adjudicated label')
        annotators=x.get('annotators',[])
        if not isinstance(annotators,list) or len(set(annotators))<2:
            raise ValueError('Two independent, nonidentical human annotator ids are required')
        if x.get('label_status')!='ADJUDICATED':raise ValueError('Unadjudicated labels cannot be scored')
        if x.get('source_reviewed') is not True:
            raise ValueError('Gold label must attest source was manually reviewed; evaluator cannot prove that claim')
    if require_200 and Counter(x['stratum'] for x in gold)!=Counter(STRATA):
        raise ValueError('Expected 40 cases in each prespecified stratum')
    gp={x['case_id']:x for x in gold}
    if set(ps)-set(ids):raise ValueError('Predictions include ids not present in labeled gold')
    pp={x['case_id']:x for x in predictions}
    for x in predictions:
        if x.get('predicted_verdict') not in VERDICTS:
            raise ValueError('Prediction contains unsupported verdict')
    total=len(gold)
    answered=sum(x.get('predicted_verdict') != 'INSUFFICIENT_EVIDENCE' for x in predictions)
    correct=sum(pp[x['case_id']]['predicted_verdict']==x['gold_verdict'] for x in gold if x['case_id'] in pp)
    wrong_support=sum(1 for x in gold if x['case_id'] in pp and
                      pp[x['case_id']]['predicted_verdict']=='SUPPORTED' and x['gold_verdict']!='SUPPORTED')
    answered_support=sum(1 for x in predictions if x['predicted_verdict']=='SUPPORTED')
    return {
        'status':'LABELED_INPUTS_SCORED_NOT_INDEPENDENTLY_AUTHENTICATED',
        'benchmark_is_independently_verified':False,
        'case_count':total,'prediction_count':len(predictions),
        'scoring_population':'all adjudicated gold cases; unanswered counted incorrect',
        'overall_accuracy':round(correct/total,4),
        'overall_accuracy_ci95_wilson':wilson_95(correct,total),
        'coverage_fraction':round(len(predictions)/total,4),
        'nonabstention_fraction':round(answered/total,4),
        'false_support_rate_among_supported_predictions':(round(wrong_support/answered_support,4)
               if answered_support else None),
        'citation_accuracy':'NOT_MEASURED_REQUIRES_EXTERNAL_HUMAN_CITATION_AUDIT',
        'stratum_counts':dict(Counter(x['stratum'] for x in gold)),
        'disclaimer':'No real-company facts or filing pages are independently validated by this scoring script.'
    }

def main(argv: list[str]) -> int:
    if len(argv)==2 and argv[0]=='--make-plan':
        make_sampling_plan(argv[1]);print(f'Wrote 200 unsourced sampling slots: {argv[1]}');return 0
    if len(argv)!=2:
        print('Usage: python -m evaluation.benchmark GOLD.jsonl PREDICTIONS.jsonl',file=sys.stderr)
        return 2
    result=evaluate(load_jsonl(argv[0]),load_jsonl(argv[1]),require_200=True)
    print(json.dumps(result,indent=2));return 0
if __name__=='__main__':sys.exit(main(sys.argv[1:]))
