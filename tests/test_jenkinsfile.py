import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

STAGES_IN_ORDER = [
    "Checkout",
    "Build",
    "Test",
    "Package",
    "Deploy to AWS",
    "Deploy to Azure",
    "Deploy to GCP",
]

# Built by joining pieces, so this test file does not contain the
# very patterns it is scanning for.
SECRET_PATTERNS = [
    "AK" + "IA",
    "BEGIN PRIVATE " + "KEY",
    "pass" + "word =",
    "pass" + "word:",
    "api" + "_key =",
    "secret" + "_key =",
]

TEXT_SUFFIXES = {".py", ".sh", ".md", ".txt", ".yml", ".yaml", ".tf", ".csv", ""}
SKIP_DIRS = {".git", "__pycache__", "logs", "artifacts", ".venv", ".pytest_cache"}


def test_jenkinsfile_has_all_stages_in_order():
    text = (ROOT / "Jenkinsfile").read_text(encoding="utf-8")
    positions = []
    for stage in STAGES_IN_ORDER:
        needle = f"stage('{stage}')"
        assert needle in text, f"missing stage: {stage}"
        positions.append(text.index(needle))
    assert positions == sorted(positions), "stages are out of order"


def test_jenkinsfile_uses_dry_run_and_credential_ids_only():
    text = (ROOT / "Jenkinsfile").read_text(encoding="utf-8")
    assert "DRY_RUN = 'true'" in text
    for cred_id in ("aws-creds", "azure-creds", "gcp-creds"):
        assert cred_id in text


def test_no_secret_values_anywhere_in_repo():
    checked = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in ("Jenkinsfile", ".gitignore"):
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        checked += 1
        for pattern in SECRET_PATTERNS:
            assert pattern not in content, f"possible secret pattern in {path}"
    assert checked > 15


def test_terraform_files_exist_for_all_three_clouds():
    for cloud in ("aws", "azure", "gcp"):
        for name in ("main.tf", "variables.tf", "outputs.tf"):
            assert (ROOT / "terraform" / cloud / name).is_file()
