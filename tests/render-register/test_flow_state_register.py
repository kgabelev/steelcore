#!/usr/bin/env python3
"""Repository-local checks for the Flow State Fundamentals comparison register.

Run directly: python3 tests/render-register/test_flow_state_register.py

Rebuilds the register from the committed evidence JSON (never from live Drive
access) into a temp directory, then checks the outputs. Never touches the
checked-in catalog/render-register/*.csv or any audio source file.
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
SCRIPT = ROOT / "scripts/render-register/build_flow_state_register.py"
EVIDENCE_DIR = ROOT / "catalog/render-register/evidence"
MANIFEST = EVIDENCE_DIR / "flow_state_primary_manifest.json"
METADATA = EVIDENCE_DIR / "flow_state_extracted_metadata.json"
SECONDARY_REGISTER = ROOT / "catalog/render-register/RENDER_REGISTER.csv"

REQUIRED_REGISTER_FIELDS = [
    "record_id", "original_filename", "drive_file_id", "drive_url", "source_folder",
    "suno_song_id", "suno_song_url", "created_at_utc", "duration_seconds",
    "file_size_bytes", "sha256", "md5", "sample_rate", "channels", "bitrate",
    "genre_family_by_title", "paired_take_family", "has_artwork", "artwork_sha256",
    "lyrics_availability", "prompt_availability",
    "tempo_bpm_estimate", "spectral_centroid_hz_mean", "percussive_energy_ratio",
    "signal_features_note", "cross_folder_match_render_id", "cross_folder_evidence",
    "confirmed_or_candidate_parent", "lineage_confidence", "generation_depth",
    "owner_rating", "owner_notes", "analyst_observations",
    "canon_status", "release_status", "unresolved_questions",
    "download_status", "evidence_status", "id3_error", "ffprobe_error",
    "size_matches_drive_listing", "notes",
]

MUTATION_PATTERNS = [
    r"\bos\.remove\(", r"\bos\.unlink\(", r"\bos\.rename\(",
    r"\bshutil\.move\(", r"\bshutil\.rmtree\(", r"\bPath\([^)]*\)\.unlink\(",
    r"\.rename\(", r"open\([^)]*['\"]w['\"][^)]*\)\s*$",
]

EXPECTED_IN_SCOPE_FILES = 21
EXPECTED_TOTAL_PRIMARY_FILES = 35


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_build(out_dir: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--manifest", str(MANIFEST), "--metadata", str(METADATA),
         "--secondary-register", str(SECONDARY_REGISTER), "--out-dir", str(out_dir)],
        capture_output=True, text=True,
    )
    require(result.returncode == 0, f"build script failed: {result.stderr}")


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def test_evidence_files_are_read_only_inputs() -> None:
    require(MANIFEST.exists(), f"missing committed evidence file: {MANIFEST}")
    require(METADATA.exists(), f"missing committed evidence file: {METADATA}")
    manifest = json.loads(MANIFEST.read_text())
    manifest_files = manifest["files"] if isinstance(manifest, dict) else manifest
    require(len(manifest_files) == EXPECTED_TOTAL_PRIMARY_FILES,
            f"expected {EXPECTED_TOTAL_PRIMARY_FILES} files in the primary-folder manifest, got {len(manifest_files)}")
    in_scope = [f for f in manifest_files if f.get("in_scope")]
    require(len(in_scope) == EXPECTED_IN_SCOPE_FILES,
            f"expected {EXPECTED_IN_SCOPE_FILES} in-scope files, got {len(in_scope)}")


def test_required_fields(out_dir: Path) -> None:
    rows = read_csv(out_dir / "FLOW_STATE_FUNDAMENTALS_REGISTER.csv")
    require(len(rows) == EXPECTED_IN_SCOPE_FILES,
            f"expected {EXPECTED_IN_SCOPE_FILES} register rows (one per in-scope file), got {len(rows)}")
    header = list(rows[0].keys())
    require(header == REQUIRED_REGISTER_FIELDS,
            f"register header mismatch.\nexpected: {REQUIRED_REGISTER_FIELDS}\nactual:   {header}")


def test_no_fabricated_evidence_for_failed_downloads() -> None:
    metadata = json.loads(METADATA.read_text())
    metadata_by_id = {m["drive_file_id"]: m for m in metadata}
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        run_build(out_dir)
        rows = read_csv(out_dir / "FLOW_STATE_FUNDAMENTALS_REGISTER.csv")
    for row in rows:
        meta = metadata_by_id.get(row["drive_file_id"])
        if meta is None or meta.get("download_status") == "failed":
            require(row["download_status"] == "failed", f"{row['record_id']}: expected failed status")
            require(row["sha256"] == "", f"{row['record_id']}: has no download evidence but sha256 is non-empty")
            require(row["suno_song_id"] == "", f"{row['record_id']}: has no download evidence but suno_song_id is non-empty")
        else:
            if row["sha256"]:
                require(row["sha256"] == meta.get("sha256"),
                        f"{row['record_id']}: sha256 does not match its own source file's extracted metadata")
            if row["suno_song_id"]:
                require(row["suno_song_id"] == meta.get("suno_song_id"),
                        f"{row['record_id']}: suno_song_id does not match its own source file's extracted metadata")


def test_sibling_pairs_are_labeled_inferred(out_dir: Path) -> None:
    path = out_dir / "FLOW_STATE_SIBLING_PAIRS.csv"
    rows = read_csv(path)
    for row in rows:
        require(row["evidence_status"] == "inferred",
                f"{row['sibling_pair_id']}: evidence_status must be 'inferred', got {row['evidence_status']!r}")
        require(row["confidence"] in {"high", "medium", "low"},
                f"{row['sibling_pair_id']}: confidence {row['confidence']!r} is not one of high/medium/low")
        require(float(row["delta_seconds"]) <= 2.0,
                f"{row['sibling_pair_id']}: delta_seconds {row['delta_seconds']} exceeds the 2.0s sibling threshold")


def test_no_source_mutation_logic() -> None:
    source = SCRIPT.read_text()
    for pattern in MUTATION_PATTERNS:
        matches = re.findall(pattern, source, flags=re.MULTILINE)
        require(len(matches) == 0,
                f"build_flow_state_register.py contains a potential source-mutation call matching {pattern!r}: {matches}")
    require("os.remove" not in source and "shutil.rmtree" not in source and "os.rename" not in source,
            "build_flow_state_register.py contains forbidden deletion/rename identifiers")


def test_deterministic_rebuild() -> None:
    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        run_build(Path(tmp1))
        run_build(Path(tmp2))
        for name in ("FLOW_STATE_FUNDAMENTALS_REGISTER.csv", "FLOW_STATE_SIBLING_PAIRS.csv"):
            a = (Path(tmp1) / name).read_text()
            b = (Path(tmp2) / name).read_text()
            require(a == b, f"{name} is not byte-identical across two builds from the same evidence")


def main() -> None:
    test_no_source_mutation_logic()
    test_evidence_files_are_read_only_inputs()
    test_no_fabricated_evidence_for_failed_downloads()
    test_deterministic_rebuild()
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        run_build(out_dir)
        test_required_fields(out_dir)
        test_sibling_pairs_are_labeled_inferred(out_dir)
    print("flow state fundamentals register validation passed")


if __name__ == "__main__":
    main()
