from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioComponent:
    component: str
    repository: str
    role: str
    integration_status: str


PORTFOLIO_COMPONENTS: tuple[PortfolioComponent, ...] = (
    PortfolioComponent(
        "Finance & Operations Audit Engine",
        "Saehon/AAA",
        "Deterministic transaction testing, evidence IDs, controls, forensic and operations-risk foundation.",
        "executable_dependency",
    ),
    PortfolioComponent(
        "IFRS-AI Inspector",
        "Saehon/IFRS-AI-Inspector",
        "Standards-aware reporting, evidence provenance, deterministic verification and human-gated assurance concepts.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "AuditData API",
        "Saehon/AuditData-API",
        "Potential audit-data ingestion and normalized evidence-access layer.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "Multi-Agent BERT",
        "Saehon/Google-Antigravity-using-a-multi-agent-BERT-architecture",
        "Potential financial-text classification, embeddings and NLP risk-signal layer.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "Financial Sentiment Models",
        "Saehon/Financial-Sentiment-Analysis-and-Classification-Deep-Learning-Models",
        "Potential narrative, sentiment and disclosure-risk signal layer.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "TimesFM",
        "Saehon/timesfm",
        "Potential time-series forecasting and anomaly-baseline layer for controls and financial processes.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "GAN Lab",
        "Saehon/ganlab",
        "Potential adversarial/synthetic scenario generation for control and fraud-risk evaluation.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "Synthetic Data",
        "Saehon/fg-data-synthetic",
        "Potential privacy-preserving synthetic test populations and simulation data.",
        "adapter_boundary",
    ),
    PortfolioComponent(
        "Banking Agent",
        "Saehon/agent-openai-python-banking-assistant",
        "Reference implementation for finance-agent interaction and transaction-oriented workflows.",
        "reference_only",
    ),
    PortfolioComponent(
        "Research Architecture",
        "Saehon/Saeid-Homayoun",
        "Portfolio-level evidence governance, reproducibility, scientific challenge and human decision rights.",
        "governance_reference",
    ),
)
