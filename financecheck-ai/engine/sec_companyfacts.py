"""SEC Company Facts annual revenue prototype; no live verification asserted."""
import json,re
from datetime import date
from decimal import Decimal
from urllib.request import Request,urlopen
TAGS=("RevenueFromContractWithCustomerExcludingAssessedTax","Revenues","SalesRevenueNet")
def retrieve_companyfacts(cik,user_agent,timeout=15):
    if not re.fullmatch(r"\d{1,10}",str(cik)): raise ValueError("Invalid CIK")
    if not isinstance(user_agent,str) or len(user_agent.strip())<12 or "@" not in user_agent: raise ValueError("Identifying contact User-Agent required")
    url=f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(cik).zfill(10)}.json"
    with urlopen(Request(url,headers={"User-Agent":user_agent,"Accept":"application/json"}),timeout=timeout) as response: data=json.load(response)
    if str(data.get("cik"))!=str(int(cik)): raise ValueError("CIK mismatch")
    return data,url
def select_annual_revenues(data,as_of):
    cutoff=date.fromisoformat(as_of)
    facts=data.get("facts",{}).get("us-gaap",{})
    for tag in TAGS:
        entries=facts.get(tag,{}).get("units",{}).get("USD",[])
        grouped={}
        for r in entries:
            try:
                start,end,filed=[date.fromisoformat(r[k]) for k in ("start","end","filed")]
                year=int(r["fy"]);val=Decimal(str(r["val"]))
            except (KeyError,ValueError,TypeError,ArithmeticError):continue
            if (r.get("fp")!="FY" or r.get("form") not in ("10-K","10-K/A") or filed>cutoff
                or not val.is_finite() or val<0 or not 330<=(end-start).days<=380 or end.year!=year
                or r.get("frame") not in (None,f"CY{year}")):continue
            grouped.setdefault(year,[]).append((filed,val,r))
        selected={}
        for year,rows in grouped.items():
            latest=max(x[0] for x in rows);current=[x for x in rows if x[0]==latest]
            if len({x[1] for x in current})!=1:raise ValueError("Ambiguous revenue facts")
            selected[year]=current[0]
        out=[]
        for year in sorted(selected):
            if year-1 not in selected or selected[year-1][1]<=0:continue
            current,previous=selected[year],selected[year-1]
            out.append(dict(year=year,prior_year=year-1,growth_percent=str(((current[1]-previous[1])/previous[1]*100).quantize(Decimal("0.0001"))),current_revenue_usd=str(current[1]),prior_revenue_usd=str(previous[1]),current_accession=current[2].get("accn"),prior_accession=previous[2].get("accn"),concept=tag,unit="USD",as_of=as_of,evidence_status="SEC_COMPANYFACTS_METADATA_UNRECONCILED"))
        if out:return out
    raise ValueError("No comparable annual revenue observations")
