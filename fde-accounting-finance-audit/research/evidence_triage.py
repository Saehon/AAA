"""Offline research-source triage, not a scraping API or scholarly verification engine."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "journals": ("academic_sources_2022_2026.json", "articles"),
    "theses": ("university_theses_2022_2026.json", "theses"),
    "tldr": ("tldr_signals_2026.json", "signals"),
}
DOI = re.compile(r"^10\.\d{4,9}/[^\s]+$")


def _load(kind):
    filename, key = SOURCES[kind]
    data = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    return data[key]


def validate():
    seen = set()
    counts = {}
    for kind in SOURCES:
        entries = _load(kind)
        assert entries, f"empty registry: {kind}"
        for record in entries:
            rid = record["id"]
            assert rid not in seen, f"Duplicate ID: {rid}"
            seen.add(rid)
            if kind == "journals":
                assert record["source_type"] == "peer_reviewed_journal_article"
                assert DOI.match(record["doi"]), f"invalid DOI: {rid}"
                assert record["primary_url"].startswith("https://doi.org/")
                assert 2022 <= record["year"] <= 2026
                r = record["rankings"]
                assert type(r["ft50_2026"]) is bool
                assert r["ajg_2024"] in ("4*", "4", "3", "2", "1", None)
                assert r["scimago_q1_2025"] in (True, False, None)
            elif kind == "theses":
                assert record["source_type"] == "university_thesis"
                assert record["not_peer_reviewed_journal_article"] is True
                assert all(v is None for v in record["journal_rankings"].values())
                assert 2022 <= record["year"] <= 2026
                assert record["institution"] in {
                    "Harvard University", "Massachusetts Institute of Technology", "Stanford University"
                }
                assert record["source_url"].startswith("https://")
            else:
                assert record["source_type"] == "news_signal"
                assert record["not_peer_reviewed"] is True
                assert record["implementation_status"] == "proposed_not_yet_built"
                assert record["source_url"].startswith("https://")
                assert "2026-" in record["date"]
        counts[kind] = len(entries)
    return counts


def main():
    parser = argparse.ArgumentParser(description="Offline, structured evidence register viewer.")
    parser.add_argument("--feed", choices=[*SOURCES, "all"], default="all")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    counts = validate()
    if args.check:
        print("Offline format check passed (not remote DOI or rights verification):", counts)
    else:
        feeds = SOURCES if args.feed == "all" else [args.feed]
        for feed in feeds:
            for record in _load(feed):
                if feed == "journals":
                    print(f"{record['id']}: {record['year']} | {record['title']} | DOI {record['doi']}")
                elif feed == "theses":
                    print(f"{record['id']}: {record['year']} | {record['title']} | {record['source_url']}")
                else:
                    print(f"{record['id']}: {record['date']} | {record['title']} | {record['action']}")


if __name__ == "__main__":
    main()
