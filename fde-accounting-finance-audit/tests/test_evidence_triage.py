"""Scientific source type, ranking and year regression checks."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))
from evidence_triage import _load, validate

def test_all_registries_validate():
    counts = validate()
    assert counts["journals"] >= 15
    assert counts["theses"] >= 12
    assert counts["tldr"] >= 5

def test_theses_never_mislabeled_as_q1_or_ft50():
    for thesis in _load("theses"):
        assert all(v is None for v in thesis["journal_rankings"].values())
        assert thesis["not_peer_reviewed_journal_article"] is True

def test_venue_rank_separate_from_article_evidence():
    studies = _load("journals")
    assert any(x["rankings"]["ajg_2024"] == "4*" for x in studies)
    assert any(x["rankings"]["ajg_2024"] == "4" for x in studies)
    assert any(x["rankings"]["ajg_2024"] == "3" for x in studies)
    assert any(x["rankings"]["ajg_2024"] == "2" for x in studies)
    assert all(x["source_type"] == "peer_reviewed_journal_article" for x in studies)

def test_news_never_claimed_peer_reviewed_or_deployed():
    for signal in _load("tldr"):
        assert signal["not_peer_reviewed"] is True
        assert signal["implementation_status"] == "proposed_not_yet_built"
