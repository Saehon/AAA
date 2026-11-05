"""Release hygiene tests limited to this isolated public project folder."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ASSETS = [p for p in ROOT.rglob("*") if p.is_file() and ".venv" not in p.parts and "__pycache__" not in p.parts]
PROHIBITED = [
    "Saehon/pomelo-core",
    "drive.google.com/drive/folders/",
    "docs.google.com/document/d/",
    "BEGIN PRIVATE KEY",
    "sk-proj-",
]

def test_selected_public_files_do_not_reference_private_archives_or_keys():
    for file in PUBLIC_ASSETS:
        if file.suffix in {".pyc", ".pyo"}:
            continue
        data = file.read_text(encoding="utf-8")
        for pattern in PROHIBITED:
            # This test file contains the prohibited marker strings by definition.
            if file.name == "test_public_release_safety.py":
                continue
            assert pattern not in data, f"Private or secret marker found in {file}"
