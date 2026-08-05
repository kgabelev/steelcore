#!/usr/bin/env python3
"""Validate Steelcore AI Resource Control Plane files.

This validator deliberately treats unknown quota values as valid when they are
explicitly represented as unknown. It validates structure, internal consistency,
and freshness signals without inventing provider data.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "system" / "control-plane"


class ValidationReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_yaml(path: Path, report: ValidationReport) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(f"Missing required file: {path.relative_to(ROOT)}")
        return {}
    except yaml.YAMLError as exc:
        report.error(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(data, dict):
        report.error(f"Expected mapping at root of {path.relative_to(ROOT)}")
        return {}
    return data


def load_json(path: Path, report: ValidationReport) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(f"Missing required file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        report.error(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(data, dict):
        report.error(f"Expected object at root of {path.relative_to(ROOT)}")
        return {}
    return data


def parse_date(value: Any, field: str, report: ValidationReport) -> date | None:
    if not isinstance(value, str):
        report.error(f"{field} must be an ISO date string")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        report.error(f"{field} is not a valid ISO date: {value!r}")
        return None


def parse_datetime(value: Any, field: str, report: ValidationReport) -> datetime | None:
    if not isinstance(value, str):
        report.error(f"{field} must be an ISO datetime string")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        report.error(f"{field} is not a valid ISO datetime: {value!r}")
        return None
    if parsed.tzinfo is None:
        report.error(f"{field} must include a timezone offset")
        return None
    return parsed


def validate_model_registry(report: ValidationReport, strict_freshness: bool) -> None:
    path = CONTROL / "model-registry.yaml"
    data = load_yaml(path, report)
    if not data:
        return

    required_root = {"schema_version", "last_updated", "policy", "models", "execution_resources"}
    missing_root = required_root - data.keys()
    if missing_root:
        report.error(f"model-registry.yaml missing root keys: {sorted(missing_root)}")

    parse_datetime(data.get("last_updated"), "model-registry.last_updated", report)

    models = data.get("models")
    resources = data.get("execution_resources")
    if not isinstance(models, list) or not models:
        report.error("model-registry.models must be a non-empty list")
        models = []
    if not isinstance(resources, list) or not resources:
        report.error("model-registry.execution_resources must be a non-empty list")
        resources = []

    required_model_fields = {
        "provider",
        "model",
        "strongest_use_cases",
        "weaknesses",
        "cloud_vs_local",
        "cost_class",
        "quota_class",
        "preferred_role",
        "fallback_model",
        "last_verified_date",
    }
    seen: set[tuple[str, str]] = set()
    all_targets: set[str] = set()

    for item in [*models, *resources]:
        if isinstance(item, dict) and isinstance(item.get("model"), str):
            all_targets.add(item["model"])

    reverify_days = data.get("policy", {}).get("reverify_after_days", 14)
    if not isinstance(reverify_days, int) or reverify_days <= 0:
        report.error("model-registry.policy.reverify_after_days must be a positive integer")
        reverify_days = 14

    for index, model in enumerate(models):
        prefix = f"model-registry.models[{index}]"
        if not isinstance(model, dict):
            report.error(f"{prefix} must be a mapping")
            continue
        missing = required_model_fields - model.keys()
        if missing:
            report.error(f"{prefix} missing fields: {sorted(missing)}")

        provider = model.get("provider")
        name = model.get("model")
        if not isinstance(provider, str) or not provider.strip():
            report.error(f"{prefix}.provider must be a non-empty string")
        if not isinstance(name, str) or not name.strip():
            report.error(f"{prefix}.model must be a non-empty string")
        if isinstance(provider, str) and isinstance(name, str):
            key = (provider, name)
            if key in seen:
                report.error(f"Duplicate model entry: {provider}/{name}")
            seen.add(key)

        for field in ("strongest_use_cases", "weaknesses"):
            value = model.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(v, str) and v.strip() for v in value):
                report.error(f"{prefix}.{field} must be a non-empty list of strings")

        if model.get("cloud_vs_local") not in {"cloud", "local", "hybrid"}:
            report.error(f"{prefix}.cloud_vs_local must be cloud, local, or hybrid")

        fallback = model.get("fallback_model")
        if not isinstance(fallback, str) or not fallback.strip():
            report.error(f"{prefix}.fallback_model must be a non-empty string")
        elif fallback not in all_targets:
            report.error(f"{prefix}.fallback_model references unknown target: {fallback}")

        verified = parse_date(model.get("last_verified_date"), f"{prefix}.last_verified_date", report)
        if verified:
            age = (date.today() - verified).days
            if age < 0:
                report.error(f"{prefix}.last_verified_date is in the future")
            elif age > reverify_days:
                message = f"{prefix} is stale by policy: verified {age} days ago (limit {reverify_days})"
                report.error(message) if strict_freshness else report.warn(message)


def validate_budget_policy(report: ValidationReport) -> None:
    data = load_yaml(CONTROL / "budget-policy.yaml", report)
    if not data:
        return

    parse_datetime(data.get("last_updated"), "budget-policy.last_updated", report)
    defaults = data.get("defaults")
    if not isinstance(defaults, dict):
        report.error("budget-policy.defaults must be a mapping")
        return

    required = {
        "currency",
        "per_project_budget",
        "maximum_model_calls",
        "maximum_premium_calls",
        "parallel_agent_ceiling",
        "local_memory_ceiling_gb",
        "cloud_first_rules",
        "stop_conditions",
        "approval_thresholds",
    }
    missing = required - defaults.keys()
    if missing:
        report.error(f"budget-policy.defaults missing fields: {sorted(missing)}")

    numeric_fields = (
        "per_project_budget",
        "maximum_model_calls",
        "maximum_premium_calls",
        "parallel_agent_ceiling",
        "local_memory_ceiling_gb",
    )
    for field in numeric_fields:
        value = defaults.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            report.error(f"budget-policy.defaults.{field} must be positive")

    maximum_calls = defaults.get("maximum_model_calls")
    premium_calls = defaults.get("maximum_premium_calls")
    if isinstance(maximum_calls, int) and isinstance(premium_calls, int) and premium_calls > maximum_calls:
        report.error("maximum_premium_calls cannot exceed maximum_model_calls")

    for field in ("cloud_first_rules", "stop_conditions"):
        value = defaults.get(field)
        if not isinstance(value, list) or not value or not all(isinstance(v, str) and v.strip() for v in value):
            report.error(f"budget-policy.defaults.{field} must be a non-empty list of strings")

    approvals = defaults.get("approval_thresholds")
    if not isinstance(approvals, dict) or not approvals:
        report.error("budget-policy.defaults.approval_thresholds must be a non-empty mapping")

    project_classes = data.get("project_classes")
    if not isinstance(project_classes, dict) or not project_classes:
        report.error("budget-policy.project_classes must be a non-empty mapping")
    else:
        for class_name, limits in project_classes.items():
            if not isinstance(limits, dict):
                report.error(f"project_classes.{class_name} must be a mapping")
                continue
            for field in ("per_project_budget", "maximum_model_calls", "maximum_premium_calls", "parallel_agent_ceiling"):
                value = limits.get(field)
                if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                    report.error(f"project_classes.{class_name}.{field} must be positive")


def validate_usage_snapshot(report: ValidationReport, strict_freshness: bool) -> None:
    data = load_json(CONTROL / "usage-snapshot.json", report)
    if not data:
        return

    checked = parse_datetime(data.get("last_checked_time"), "usage-snapshot.last_checked_time", report)
    providers = data.get("providers")
    if not isinstance(providers, list) or not providers:
        report.error("usage-snapshot.providers must be a non-empty list")
        return

    required = {
        "provider",
        "current_plan",
        "remaining_quota",
        "remaining_credits",
        "reset_time",
        "auto_reload_status",
        "confidence",
        "evidence",
    }
    seen: set[str] = set()
    for index, provider in enumerate(providers):
        prefix = f"usage-snapshot.providers[{index}]"
        if not isinstance(provider, dict):
            report.error(f"{prefix} must be an object")
            continue
        missing = required - provider.keys()
        if missing:
            report.error(f"{prefix} missing fields: {sorted(missing)}")
        name = provider.get("provider")
        if not isinstance(name, str) or not name.strip():
            report.error(f"{prefix}.provider must be a non-empty string")
        elif name in seen:
            report.error(f"Duplicate usage provider: {name}")
        else:
            seen.add(name)
        for field in ("current_plan", "reset_time", "auto_reload_status", "confidence", "evidence"):
            if not isinstance(provider.get(field), str) or not provider[field].strip():
                report.error(f"{prefix}.{field} must be a non-empty string")

    refresh_rules = data.get("refresh_rules")
    if not isinstance(refresh_rules, dict):
        report.error("usage-snapshot.refresh_rules must be an object")
        return
    max_age = refresh_rules.get("maximum_snapshot_age_hours")
    if not isinstance(max_age, int) or max_age <= 0:
        report.error("refresh_rules.maximum_snapshot_age_hours must be a positive integer")
    elif checked:
        age_hours = (datetime.now(timezone.utc) - checked.astimezone(timezone.utc)).total_seconds() / 3600
        if age_hours < -0.25:
            report.error("usage-snapshot.last_checked_time is in the future")
        elif age_hours > max_age:
            message = f"usage snapshot is stale: {age_hours:.1f} hours old (limit {max_age})"
            report.error(message) if strict_freshness else report.warn(message)


def validate_build_history(report: ValidationReport) -> None:
    path = CONTROL / "build-history.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        report.error(f"Missing required file: {path.relative_to(ROOT)}")
        return
    nonempty = [line for line in lines if line.strip()]
    if not nonempty:
        report.error("build-history.jsonl must contain at least one record")
        return

    required = {
        "timestamp",
        "project",
        "agent_model_used",
        "task",
        "duration_minutes",
        "estimated_cost_usd",
        "outcome",
        "failures",
        "lessons_learned",
    }
    for line_number, line in enumerate(nonempty, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            report.error(f"build-history.jsonl line {line_number} is invalid JSON: {exc}")
            continue
        if not isinstance(record, dict):
            report.error(f"build-history.jsonl line {line_number} must be an object")
            continue
        missing = required - record.keys()
        if missing:
            report.error(f"build-history.jsonl line {line_number} missing fields: {sorted(missing)}")
        parse_datetime(record.get("timestamp"), f"build-history line {line_number}.timestamp", report)
        if not isinstance(record.get("duration_minutes"), (int, float)) or record.get("duration_minutes", -1) < 0:
            report.error(f"build-history line {line_number}.duration_minutes must be non-negative")
        if not isinstance(record.get("estimated_cost_usd"), (int, float)) or record.get("estimated_cost_usd", -1) < 0:
            report.error(f"build-history line {line_number}.estimated_cost_usd must be non-negative")
        for field in ("failures", "lessons_learned"):
            if not isinstance(record.get(field), list):
                report.error(f"build-history line {line_number}.{field} must be a list")


def validate_routing_policy(report: ValidationReport) -> None:
    path = CONTROL / "routing-policy.md"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        report.error(f"Missing required file: {path.relative_to(ROOT)}")
        return
    normalized = text.lower()
    required_topics = {
        "parallel agents": "parallel agents",
        "graphs": "graph",
        "loops": "loop",
        "workflows": "workflow",
        "second laptop": "second laptop",
        "branch collisions": "branch collision",
        "duplicate work": "duplicate work",
    }
    for label, phrase in required_topics.items():
        if phrase not in normalized:
            report.error(f"routing-policy.md does not cover required topic: {label}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict-freshness",
        action="store_true",
        help="Fail instead of warning when model verification or usage snapshots are stale.",
    )
    args = parser.parse_args()

    report = ValidationReport()
    validate_model_registry(report, args.strict_freshness)
    validate_budget_policy(report)
    validate_usage_snapshot(report, args.strict_freshness)
    validate_build_history(report)
    validate_routing_policy(report)

    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")

    if report.errors:
        print(f"Control-plane validation failed with {len(report.errors)} error(s).")
        return 1
    print(f"Control-plane validation passed with {len(report.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
