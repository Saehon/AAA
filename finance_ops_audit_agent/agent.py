from __future__ import annotations

import json
import os
from pathlib import Path

from agents import Agent, Runner, function_tool

from .analytics import analyze_transactions
from .schemas import AuditAgentReport


PACKAGE_ROOT = Path(__file__).resolve().parent
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")


def _resolve_repo_local_path(csv_path: str) -> Path:
    candidate = Path(csv_path)
    if not candidate.is_absolute():
        candidate = (PACKAGE_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()

    allowed_root = PACKAGE_ROOT.resolve()
    if allowed_root not in candidate.parents and candidate != allowed_root:
        raise ValueError(
            "For this public research prototype, data files must be inside "
            "finance_ops_audit_agent/ to reduce accidental access to unrelated local files."
        )
    return candidate


@function_tool
def run_transaction_tests(csv_path: str) -> str:
    """Run deterministic finance and operations audit tests on a repo-local CSV file.

    Args:
        csv_path: Path relative to finance_ops_audit_agent/, for example
            sample_data/transactions.csv.
    """
    path = _resolve_repo_local_path(csv_path)
    result = analyze_transactions(path)
    return json.dumps(result.model_dump(), indent=2)


finance_controls_agent = Agent(
    name="Finance Controls Auditor",
    model=MODEL,
    instructions=(
        "You are a finance and accounting internal-audit specialist. "
        "Assess authorization, segregation of duties, transaction integrity, financial-process risk, "
        "and evidence sufficiency. Use run_transaction_tests for transaction claims. "
        "Do not call a risk a confirmed control failure unless the supplied evidence supports that conclusion. "
        "Cite finding IDs and rule IDs in your response."
    ),
    tools=[run_transaction_tests],
)

forensic_agent = Agent(
    name="Forensic Transaction Analyst",
    model=MODEL,
    instructions=(
        "You are a forensic accounting specialist. Analyze unusual transactions, possible fraud indicators, "
        "duplicate processing, anomalous timing, and suspicious patterns. Distinguish indicators from proven misconduct. "
        "Use run_transaction_tests and cite the evidence/finding IDs behind every material statement."
    ),
    tools=[run_transaction_tests],
)

operations_risk_agent = Agent(
    name="Operations Risk Auditor",
    model=MODEL,
    instructions=(
        "You are an operational audit specialist. Interpret the transaction tests in the context of process resilience, "
        "scalability, accountability, authorization, and cross-functional risk. "
        "State what additional process evidence would be needed before a conclusion is finalized."
    ),
    tools=[run_transaction_tests],
)

audit_leader = Agent(
    name="Finance & Operations Audit Leader Agent",
    model=MODEL,
    instructions=(
        "Act as the lead internal-audit orchestrator for a research prototype. "
        "Use the specialist tools to perform a risk-based review. "
        "For transaction-population work, consult Finance Controls and Forensic specialists; consult Operations Risk "
        "when process or governance implications matter. Synthesize rather than merely concatenate their outputs. "
        "Every material risk must be tied to an evidence reference, finding ID, or explicit statement that evidence is missing. "
        "Do not issue an audit opinion, accuse a person or vendor of wrongdoing, or claim regulatory compliance. "
        "Recommendations must be practical, prioritized, and proportional. "
        "Set human_review_required to true because this system is decision support, not autonomous assurance."
    ),
    tools=[
        finance_controls_agent.as_tool(
            tool_name="finance_controls_review",
            tool_description="Review finance/accounting controls and transaction-level evidence.",
        ),
        forensic_agent.as_tool(
            tool_name="forensic_review",
            tool_description="Review fraud indicators and unusual transaction patterns without alleging misconduct.",
        ),
        operations_risk_agent.as_tool(
            tool_name="operations_risk_review",
            tool_description="Review operational, governance, and process implications.",
        ),
    ],
    output_type=AuditAgentReport,
)


async def run_audit(objective: str, csv_path: str) -> AuditAgentReport:
    prompt = (
        f"Audit objective: {objective}\n"
        f"Transaction file: {csv_path}\n"
        "Perform an evidence-grounded review. Keep conclusions within the evidence available."
    )
    result = await Runner.run(audit_leader, prompt)
    return result.final_output
