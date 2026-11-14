"""FinanceCheck SEC XBRL evidence module: direct SEC API, no embedded proprietary data."""
from .verify import verify_revenue_yoy, verify_live_sec_claim, sec_companyfacts_url, EvidenceError
__all__ = ['verify_revenue_yoy','verify_live_sec_claim','sec_companyfacts_url','EvidenceError']
