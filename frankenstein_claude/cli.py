from __future__ import annotations

import argparse
from pathlib import Path

from .orchestrator import DEFAULT_SAMPLE, run_frankenstein_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Frankenstein Claude: evidence-governed multi-agent accounting and assurance prototype."
    )
    parser.add_argument(
        "--csv",
        default=str(DEFAULT_SAMPLE),
        help="Transaction CSV. Defaults to the Finance & Operations Audit Agent synthetic dataset.",
    )
    parser.add_argument(
        "--objective",
        default=(
            "Assess finance, accounting, internal-control, forensic, operations, sustainability, "
            "cost/FinOps, and AI/data-governance risks using evidence-grounded specialist review."
        ),
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run deterministic evidence and specialist scaffolding without calling Claude.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report = run_frankenstein_audit(
        objective=args.objective,
        csv_path=Path(args.csv),
        use_claude=not args.offline,
    )
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
