#!/usr/bin/env python3
"""Validate provenance records with JSON Schema Draft 2020-12."""
from __future__ import annotations

import copy
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: install with `python -m pip install -r tests/provenance/requirements.txt`"
    ) from exc

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/provenance/artifact-provenance.schema.json"
EXAMPLES = ROOT / "examples/provenance"
DOCS = [
    ROOT / "legal/rights-and-provenance.md",
    ROOT / "legal/authorship-log-template.md",
    ROOT / "legal/disclosure-statement.md",
    ROOT / "legal/counsel-review-needed.md",
    ROOT / "legal/risk-checklist.md",
]

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


def validator() -> Draft202012Validator:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def assert_valid(record: dict) -> None:
    validator().validate(record)


def assert_invalid(record: dict, message: str) -> None:
    errors = sorted(validator().iter_errors(record), key=lambda error: list(error.path))
    if not errors:
        raise AssertionError(message)


def test_examples_validate_against_schema() -> None:
    for path in sorted(EXAMPLES.glob("*.json")):
        assert_valid(load(path))


def test_legacy_unknowns_and_invariants() -> None:
    legacy = load(EXAMPLES / "legacy-experiment-unknowns.json")
    assert_valid(legacy)
    require(legacy["created_at"] == "unknown", "legacy fixture must preserve unknown created_at")
    require(legacy["human_contributors"][0]["name"] == "unknown", "legacy fixture must allow unknown contributor")
    require(legacy["ai_systems"][0]["model_or_version"] == "unknown", "legacy fixture must allow unknown model")
    require(legacy["classification"] == "experiment", "legacy example must be an experiment")
    require(legacy["release_clearance"]["status"] != "cleared", "legacy example must not be release-cleared")
    require(
        not any(a["approval_type"] == "canon" and a["status"] == "approved" for a in legacy["approvals"]),
        "legacy example must not be canon-approved",
    )


def test_ambiguous_or_malformed_values_fail_schema() -> None:
    record = load(EXAMPLES / "legacy-experiment-unknowns.json")
    record["source_inputs"][0]["source_ref"] = "unknown"
    assert_invalid(record, "literal unknown must not be accepted as an evidence reference")

    record = load(EXAMPLES / "legacy-experiment-unknowns.json")
    record["human_contributors"][0]["name"] = ""
    assert_invalid(record, "empty known-or-unknown strings must fail")

    record = load(EXAMPLES / "legacy-experiment-unknowns.json")
    record["classification"] = "release_ready"
    assert_invalid(record, "classification values absent from the schema must fail")


def test_canon_without_evidenced_canon_approval_fails_schema() -> None:
    record = load(EXAMPLES / "canon-release-cleared.json")
    record["approvals"] = [a for a in record["approvals"] if a["approval_type"] != "canon"]
    assert_invalid(record, "canon classification requires evidenced canon approval")

    record = load(EXAMPLES / "canon-release-cleared.json")
    for approval in record["approvals"]:
        if approval["approval_type"] == "canon":
            approval["reviewer"] = "unknown"
    assert_invalid(record, "approved canon approval requires a known reviewer")


def test_release_clearance_requires_rights_approval_reviewer_timestamp_and_evidence() -> None:
    base = load(EXAMPLES / "canon-release-cleared.json")
    mutations = []

    record = copy.deepcopy(base)
    record["rights"]["ownership_status"] = "unresolved"
    mutations.append((record, "cleared release requires resolved ownership rights"))

    record = copy.deepcopy(base)
    record["rights"]["voice_likeness_status"] = "unknown"
    mutations.append((record, "cleared release requires resolved voice/likeness rights"))

    record = copy.deepcopy(base)
    record["approvals"] = [a for a in record["approvals"] if a["approval_type"] != "release"]
    mutations.append((record, "cleared release requires an approved release approval"))

    record = copy.deepcopy(base)
    record["release_clearance"]["reviewer"] = "unknown"
    mutations.append((record, "cleared release requires a known reviewer"))

    record = copy.deepcopy(base)
    record["release_clearance"]["timestamp"] = "unknown"
    mutations.append((record, "cleared release requires a timestamp"))

    record = copy.deepcopy(base)
    record["release_clearance"]["evidence_refs"] = []
    mutations.append((record, "cleared release requires evidence"))

    for record, message in mutations:
        assert_invalid(record, message)


def test_invalid_date_time_values_fail_schema() -> None:
    record = load(EXAMPLES / "canon-release-cleared.json")
    record["created_at"] = "2026-02-31T25:61:00Z"
    assert_invalid(record, "invalid date-time values must fail format checking")


def test_manual_status_invariants() -> None:
    for path in sorted(EXAMPLES.glob("*.json")):
        record = load(path)
        require(record["classification"] in CLASSIFICATIONS, "invalid classification")
        require(record["release_clearance"]["status"] in CLEARANCE, "invalid release_clearance.status")
        require(record["release"]["status"] in RELEASE, "invalid release.status")
        for approval in record["approvals"]:
            require(approval["status"] in APPROVAL, "invalid approval status")


def test_docs_terms() -> None:
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        require("release-ready" not in text.lower(), f"{path} uses release-ready instead of release_clearance")
        require(
            "release_clearance" in text or path.name == "counsel-review-needed.md",
            f"{path} does not mention schema release_clearance",
        )
    schema_text = SCHEMA.read_text(encoding="utf-8")
    for term in [*CLASSIFICATIONS, *CLEARANCE, *APPROVAL, *RELEASE]:
        require(term in schema_text, f"schema is missing documented status term {term}")


def main() -> None:
    test_examples_validate_against_schema()
    test_legacy_unknowns_and_invariants()
    test_ambiguous_or_malformed_values_fail_schema()
    test_canon_without_evidenced_canon_approval_fails_schema()
    test_release_clearance_requires_rights_approval_reviewer_timestamp_and_evidence()
    test_invalid_date_time_values_fail_schema()
    test_manual_status_invariants()
    test_docs_terms()
    print("provenance validation passed")


if __name__ == "__main__":
    main()
