#!/usr/bin/env python3
"""Repository-local provenance contract checks without network dependencies."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/provenance/artifact-provenance.schema.json"
EXAMPLES = ROOT / "examples/provenance"
DOCS = [ROOT / "legal/rights-and-provenance.md", ROOT / "legal/authorship-log-template.md", ROOT / "legal/disclosure-statement.md", ROOT / "legal/counsel-review-needed.md", ROOT / "legal/risk-checklist.md"]

CLASSIFICATIONS = {"unresolved", "evidence", "experiment", "candidate", "canon"}
CLEARANCE = {"cleared", "pending", "rejected", "unresolved", "unknown", "not_applicable"}
APPROVAL = {"approved", "pending", "rejected", "unknown", "not_applicable"}
RELEASE = {"unreleased", "scheduled", "released", "withdrawn", "blocked"}


def load(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_record(record: dict) -> None:
    required = {"schema_version", "artifact_id", "artifact_version", "artifact_type", "title", "created_at", "classification", "human_contributors", "ai_systems", "source_inputs", "transformations", "rights", "disclosure", "approvals", "release_clearance", "release"}
    require(set(record) == required, f"unexpected top-level fields: {sorted(set(record) ^ required)}")
    require(record["schema_version"] == "0.2", "schema_version must be 0.2")
    require(record["classification"] in CLASSIFICATIONS, "invalid classification")
    require(record["release_clearance"]["status"] in CLEARANCE, "invalid release_clearance.status")
    require(record["release"]["status"] in RELEASE, "invalid release.status")
    for approval in record["approvals"]:
        require(approval["status"] in APPROVAL, "invalid approval status")
        if approval["status"] == "approved":
            require(approval.get("reviewer") not in (None, "", "unknown"), "approved approvals require reviewer")
            require(approval.get("timestamp") not in (None, "", "unknown"), "approved approvals require timestamp")
            require(bool(approval.get("evidence_refs")), "approved approvals require evidence_refs")
    rights = record["rights"]
    if rights["ownership_status"] == "cleared":
        require(bool(rights["ownership_evidence_refs"]), "cleared ownership requires evidence")
    if rights["voice_likeness_status"] == "cleared":
        require(bool(rights["voice_likeness_evidence_refs"]), "cleared voice/likeness requires evidence")
    if rights["cultural_review_status"] == "cleared":
        require(bool(rights["cultural_review_evidence_refs"]), "cleared cultural review requires evidence")
    if record["classification"] == "canon":
        require(any(a["approval_type"] == "canon" and a["status"] == "approved" for a in record["approvals"]), "canon requires canon approval")
    if record["release_clearance"]["status"] == "cleared":
        require(record["rights"]["ownership_status"] == "cleared", "release clearance requires cleared ownership")
        require(record["rights"]["voice_likeness_status"] in {"cleared", "not_applicable"}, "release clearance requires voice/likeness resolved")
        require(record["rights"]["cultural_review_status"] in {"cleared", "not_applicable"}, "release clearance requires cultural review resolved")
        rc = record["release_clearance"]
        require(rc.get("reviewer") not in (None, "", "unknown"), "cleared release requires reviewer")
        require(rc.get("timestamp") not in (None, "", "unknown"), "cleared release requires timestamp")
        require(bool(rc.get("evidence_refs")), "cleared release requires evidence")
        require(any(a["approval_type"] == "release" and a["status"] == "approved" for a in record["approvals"]), "cleared release requires release approval")


def test_examples() -> None:
    for path in sorted(EXAMPLES.glob("*.json")):
        validate_record(load(path))
    legacy = load(EXAMPLES / "legacy-experiment-unknowns.json")
    require(legacy["classification"] == "experiment", "legacy example must be an experiment")
    require(legacy["release_clearance"]["status"] != "cleared", "legacy example must not be release-cleared")
    require(not any(a["approval_type"] == "canon" and a["status"] == "approved" for a in legacy["approvals"]), "legacy example must not be canon-approved")


def test_invalid_claims_fail() -> None:
    record = load(EXAMPLES / "legacy-experiment-unknowns.json")
    record["rights"]["ownership_status"] = "cleared"
    try:
        validate_record(record)
    except AssertionError:
        pass
    else:
        raise AssertionError("cleared ownership without evidence should fail")
    record = load(EXAMPLES / "legacy-experiment-unknowns.json")
    record["release_clearance"]["status"] = "cleared"
    try:
        validate_record(record)
    except AssertionError:
        pass
    else:
        raise AssertionError("cleared release without evidence/reviewer should fail")


def test_docs_terms() -> None:
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        require("release-ready" not in text.lower(), f"{path} uses release-ready instead of release_clearance")
        require("release_clearance" in text or path.name == "counsel-review-needed.md", f"{path} does not mention schema release_clearance")


def main() -> None:
    load(SCHEMA)
    test_examples()
    test_invalid_claims_fail()
    test_docs_terms()
    print("provenance validation passed")

if __name__ == "__main__":
    main()
