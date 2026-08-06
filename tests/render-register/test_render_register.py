#!/usr/bin/env python3
"""Repository-local render-register checks without network or pytest dependencies.

Run directly: python3 tests/render-register/test_render_register.py

These tests rebuild the register from the committed evidence JSON (never
from live Drive access) into a temp directory, then check the four CSVs.
They never touch the checked-in catalog/render-register/*.csv or any
audio source file.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/render-register/build_render_register.py"
EVIDENCE_DIR = ROOT / "catalog/render-register/evidence"
MANIFEST = EVIDENCE_DIR / "drive_mp3_listing.json"
METADATA = EVIDENCE_DIR / "extracted_metadata.json"

REQUIRED_REGISTER_FIELDS = [
    "render_id", "suno_song_id", "title", "original_filename", "drive_file_id",
    "drive_url", "created_at_utc", "duration_seconds", "file_size_bytes",
    "sha256", "md5", "sample_rate", "channels", "bitrate",
    "duplicate_group_id", "sibling_pair_id", "lineage_id",
    "inferred_parent_render_id", "lineage_confidence", "evidence_status", "notes",
]

MUTATION_PATTERNS = [
    r"\bos\.remove\(", r"\bos\.unlink\(", r"\bos\.rename\(",
    r"\bshutil\.move\(", r"\bshutil\.rmtree\(", r"\bPath\([^)]*\)\.unlink\(",
    r"\.rename\(", r"open\([^)]*['\"]w['\"][^)]*\)\s*$",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_build(out_dir: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--manifest", str(MANIFEST), "--metadata", str(METADATA), "--out-dir", str(out_dir)],
        capture_output=True, text=True,
    )
    require(result.returncode == 0, f"build script failed: {result.stderr}")


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def test_required_fields(out_dir: Path) -> None:
    rows = read_csv(out_dir / "RENDER_REGISTER.csv")
    require(len(rows) > 0, "RENDER_REGISTER.csv has no rows")
    header = list(rows[0].keys())
    require(header == REQUIRED_REGISTER_FIELDS,
            f"RENDER_REGISTER.csv header mismatch.\nexpected: {REQUIRED_REGISTER_FIELDS}\nactual:   {header}")


def test_unique_render_counts(out_dir: Path) -> None:
    manifest = json.loads(MANIFEST.read_text())
    manifest_files = manifest["files"] if isinstance(manifest, dict) else manifest
    metadata = json.loads(METADATA.read_text())

    register_rows = read_csv(out_dir / "RENDER_REGISTER.csv")
    render_ids = [r["render_id"] for r in register_rows]
    require(len(render_ids) == len(set(render_ids)), "duplicate render_id values found in RENDER_REGISTER.csv")

    dup_rows = read_csv(out_dir / "DUPLICATE_GROUPS.csv")
    files_absorbed_into_duplicates = len(dup_rows) - len({r["duplicate_group_id"] for r in dup_rows})
    expected_render_count = len(manifest_files) - files_absorbed_into_duplicates
    require(len(register_rows) == expected_render_count,
            f"expected {expected_render_count} unique renders "
            f"({len(manifest_files)} source files - {files_absorbed_into_duplicates} absorbed by duplicate grouping), "
            f"got {len(register_rows)}")

    known_song_ids = {m["suno_song_id"] for m in metadata if m.get("suno_song_id")}
    require(len(known_song_ids) == 32,
            f"expected exactly 32 unique known Suno song ids in the extracted metadata evidence, got {len(known_song_ids)}")


def test_duplicate_grouping(out_dir: Path) -> None:
    dup_rows = read_csv(out_dir / "DUPLICATE_GROUPS.csv")
    require(len(dup_rows) > 0, "expected at least one duplicate group")
    by_group: dict[str, list[dict]] = {}
    for r in dup_rows:
        by_group.setdefault(r["duplicate_group_id"], []).append(r)
    for group_id, rows in by_group.items():
        require(len(rows) >= 2, f"{group_id} has fewer than 2 members")
        hashes = {r["sha256"] for r in rows}
        require(len(hashes) == 1, f"{group_id} members do not all share one sha256: {hashes}")
        primaries = [r for r in rows if r["is_primary_in_register"] == "yes"]
        require(len(primaries) == 1, f"{group_id} does not have exactly one primary row: {len(primaries)}")

    register_rows = read_csv(out_dir / "RENDER_REGISTER.csv")
    register_by_id = {r["render_id"]: r for r in register_rows}
    for group_id, rows in by_group.items():
        render_id = rows[0]["render_id"]
        require(render_id in register_by_id, f"{group_id} points at render_id {render_id} not present in RENDER_REGISTER.csv")
        require(register_by_id[render_id]["duplicate_group_id"] == group_id,
                f"RENDER_REGISTER.csv row {render_id} does not reference back to {group_id}")


def test_ids_and_timestamps_not_guessed(out_dir: Path) -> None:
    """Every non-empty suno_song_id / created_at_utc in the register must be
    traceable byte-for-byte to the extracted-metadata evidence file; nothing
    invented, defaulted, or copied from a sibling/duplicate."""
    metadata = json.loads(METADATA.read_text())
    metadata_by_id = {m["drive_file_id"]: m for m in metadata}

    register_rows = read_csv(out_dir / "RENDER_REGISTER.csv")
    unresolved_count = 0
    for row in register_rows:
        meta = metadata_by_id.get(row["drive_file_id"])
        if meta is None:
            unresolved_count += 1
            require(row["suno_song_id"] == "", f"{row['render_id']}: has no metadata evidence but suno_song_id is non-empty")
            require(row["created_at_utc"] == "", f"{row['render_id']}: has no metadata evidence but created_at_utc is non-empty")
            require(row["evidence_status"] == "download_failed_metadata_only",
                    f"{row['render_id']}: missing evidence but evidence_status is {row['evidence_status']!r}")
            continue
        if row["suno_song_id"]:
            require(row["suno_song_id"] == meta.get("suno_song_id"),
                    f"{row['render_id']}: suno_song_id does not match its own source file's extracted metadata")
        if row["created_at_utc"]:
            require(row["created_at_utc"] == meta.get("created_at_utc"),
                    f"{row['render_id']}: created_at_utc does not match its own source file's extracted metadata")

    require(unresolved_count == 2,
            f"expected exactly 2 renders with no download evidence (the two known Drive download failures), got {unresolved_count}")


def test_inferred_relationships_are_labeled(out_dir: Path) -> None:
    sibling_rows = read_csv(out_dir / "SIBLING_PAIRS.csv")
    require(len(sibling_rows) > 0, "expected at least one sibling pair")
    for row in sibling_rows:
        require(row["evidence_status"] == "inferred",
                f"{row['sibling_pair_id']}: evidence_status must be 'inferred', got {row['evidence_status']!r}")
        require(row["confidence"] in {"high", "medium", "low"},
                f"{row['sibling_pair_id']}: confidence {row['confidence']!r} is not one of high/medium/low")

    lineage_rows = read_csv(out_dir / "LINEAGE_CANDIDATES.csv")
    require(len(lineage_rows) > 0, "expected at least one lineage candidate")
    for row in lineage_rows:
        require("infer" in row["evidence_status"].lower(),
                f"{row['lineage_id']}: evidence_status must say it is inferred, got {row['evidence_status']!r}")
        require(row["confidence"] in {"high", "medium", "low"},
                f"{row['lineage_id']}: confidence {row['confidence']!r} is not one of high/medium/low")

    register_rows = read_csv(out_dir / "RENDER_REGISTER.csv")
    for row in register_rows:
        if row["sibling_pair_id"]:
            require(row["sibling_pair_id"].startswith("SIB-"),
                    f"{row['render_id']}: sibling_pair_id {row['sibling_pair_id']!r} does not look like a SIB- id")
        if row["lineage_id"]:
            require(row["lineage_id"].startswith("LIN-"),
                    f"{row['render_id']}: lineage_id {row['lineage_id']!r} does not look like a LIN- id")
            require(row["lineage_confidence"] in {"high", "medium", "low"},
                    f"{row['render_id']}: has a lineage_id but lineage_confidence is {row['lineage_confidence']!r}")


def test_no_source_mutation_logic() -> None:
    source = SCRIPT.read_text()
    for pattern in MUTATION_PATTERNS:
        matches = re.findall(pattern, source, flags=re.MULTILINE)
        require(len(matches) == 0,
                f"build_render_register.py contains a potential source-mutation call matching {pattern!r}: {matches}")
    require("os.remove" not in source and "shutil.rmtree" not in source and "os.rename" not in source,
            "build_render_register.py contains forbidden deletion/rename identifiers")


def test_evidence_files_are_read_only_inputs() -> None:
    require(MANIFEST.exists(), f"missing committed evidence file: {MANIFEST}")
    require(METADATA.exists(), f"missing committed evidence file: {METADATA}")
    manifest = json.loads(MANIFEST.read_text())
    manifest_files = manifest["files"] if isinstance(manifest, dict) else manifest
    require(len(manifest_files) == 37, f"expected 37 source mp3 files in the committed manifest, got {len(manifest_files)}")
    metadata = json.loads(METADATA.read_text())
    require(len(metadata) == 35, f"expected 35 successfully-hashed files in the committed metadata evidence, got {len(metadata)}")


def main() -> None:
    test_no_source_mutation_logic()
    test_evidence_files_are_read_only_inputs()
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        run_build(out_dir)
        test_required_fields(out_dir)
        test_unique_render_counts(out_dir)
        test_duplicate_grouping(out_dir)
        test_ids_and_timestamps_not_guessed(out_dir)
        test_inferred_relationships_are_labeled(out_dir)
    print("render register validation passed")


if __name__ == "__main__":
    main()
