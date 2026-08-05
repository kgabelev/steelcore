#!/usr/bin/env python3
"""Validate the canonical research evidence topology without external packages."""

from __future__ import annotations

import csv
import re
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1]
REPO = RESEARCH.parent
REGISTER = RESEARCH / "source-register.csv"
QUESTIONS = RESEARCH / "open-questions.md"
LINKED_DOCUMENTS = [
    RESEARCH / "README.md",
    QUESTIONS,
    RESEARCH / "legal" / "synthesis" / "ai-music-legal-ip-business-structure-2026.md",
    RESEARCH / "industry" / "synthesis" / "ai-music-distribution-landscape-risk-2026.md",
]
EXPECTED_CLAIM_STATUS = "secondary_evidence_pending_primary_verification"


def validate_register() -> None:
    with REGISTER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 5, f"expected 5 source records, found {len(rows)}"
    assert len({row["source_id"] for row in rows}) == len(rows), "source_id values must be unique"
    for row in rows:
        assert row["classification"] == "evidence", row
        assert row["claim_status"] == EXPECTED_CLAIM_STATUS, row
        assert "verified_primary_source" not in row["verification_status"], row
        assert "approved_policy" not in row["verification_status"], row


def validate_links() -> None:
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for document in LINKED_DOCUMENTS:
        for target in pattern.findall(document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            assert (document.parent / target).resolve().is_file(), (
                f"broken relative link {target!r} in {document.relative_to(REPO)}"
            )


def validate_single_topology() -> None:
    assert REGISTER.is_file()
    assert QUESTIONS.is_file()
    assert not (RESEARCH / "legal" / "source-register.csv").exists()
    assert not (RESEARCH / "legal" / "open-questions.md").exists()


if __name__ == "__main__":
    validate_register()
    validate_links()
    validate_single_topology()
    print("Research topology validation passed.")
