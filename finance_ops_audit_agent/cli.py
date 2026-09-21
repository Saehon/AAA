from __future__ import annotations

import argparse
import asyncio
import os

from .analytics import result_as_json
from .agent import run_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evidence-grounded Finance & Operations Audit Agent prototype."
    )
    parser.add_argument(
        "--csv",
        default="sample_data/transactions.csv",
        help="Repo-local CSV path relative to finance_ops_audit_agent/.",
    )
    parser.add_argument(
        "--objective",
        default=(
            "Assess financial-process and operational risks, test key transaction controls, "
            "identify forensic indicators, and recommend evidence-based follow-up."
        ),
    )
    parser.add_argument(
        "--deterministic-only",
        action="store_true",
        help="Run transparent transaction tests only; no model/API call.",
    )
    return parser


async def _main() -> None:
    args = build_parser().parse_args()

    if args.deterministic_only or not os.getenv("OPENAI_API_KEY"):
        csv_path = Path(args.csv)
        if not csv_path.is_absolute():
            csv_path = Path(__file__).resolve().parent / csv_path
        print(result_as_json(csv_path))
        if not args.deterministic_only and not os.getenv("OPENAI_API_KEY"):
            print(
                "\nOPENAI_API_KEY is not set, so only deterministic tests were run. "
                "Set the key to enable multi-agent synthesis."
            )
        return

    report = await run_audit(args.objective, args.csv)
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(_main())
