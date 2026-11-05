"""Scientific-integrity tests: make synthetic-only semantics explicit."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))
from synthetic_control_benchmark import run, synthetic_casebook


def test_synthetic_rule_regression_with_fixed_seed():
    report = run(n=200, seed=20261105)
    assert report["cases"] == 200
    assert report["tp"] == 50
    assert report["tn"] == 150
    assert report["fn"] == report["fp"] == 0
    assert report["experiment_kind"] == "synthetic_deterministic_rule_sanity_test"
    assert "NOT empirical" in report["note"]


def test_synthetic_generation_reproducible():
    a, labels_a = synthetic_casebook(24, 123)
    b, labels_b = synthetic_casebook(24, 123)
    assert a.model_dump(mode="json") == b.model_dump(mode="json")
    assert labels_a == labels_b


def test_different_seed_changes_nominal_values_not_gold_schedule():
    a, labels_a = synthetic_casebook(20, 1)
    b, labels_b = synthetic_casebook(20, 2)
    assert a.model_dump(mode="json") != b.model_dump(mode="json")
    assert labels_a == labels_b
