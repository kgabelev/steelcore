#!/usr/bin/env python3
"""
Build the Steel render register from Drive source evidence.

Read-only, deterministic, reproducible. This script never deletes, renames,
moves, or writes to any source audio file or Drive object. It only reads two
JSON evidence files (a Drive file listing and per-file extracted metadata)
and writes CSV/Markdown outputs to a target directory.

Inputs (read-only):
  --manifest   Drive file listing JSON (id, title, fileSize, createdTime, viewUrl, ...)
                for every mp3 found in the source folder, including files whose
                content could not be downloaded.
  --metadata   Extracted metadata JSON (sha256, md5, ffprobe fields, ID3 fields)
                for every mp3 that was successfully downloaded and hashed.
                A file present in --manifest but absent from --metadata is
                reported as a download/extraction gap, never guessed at.

Outputs (written fresh each run, no partial mutation of existing repo files
other than these four generated artifacts):
  RENDER_REGISTER.csv, DUPLICATE_GROUPS.csv, SIBLING_PAIRS.csv,
  LINEAGE_CANDIDATES.csv

Identity model:
  - A "render" is identified primarily by its Suno song id (from ID3 WOAS /
    comment tags). Two Drive files sharing the same Suno song id AND the same
    sha256 are the same render re-downloaded (an exact duplicate group).
  - A file whose Suno song id or hash could not be extracted gets its own
    unresolved render row; it is never merged into another render by guessing.

Sibling-pair and lineage detection are both heuristic and are always labeled
as inferred. Nothing here is promoted to canon.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SIBLING_TIME_THRESHOLD_SECONDS = 2.0
LINEAGE_KEYWORDS = [
    "remix", "remaster", "remastered", "cover", "edit", "version",
    "original", "rework", "vip", "flip",
]


class BuildError(Exception):
    """Raised for any condition that would force this script to guess. Fail loudly instead."""


def normalize_title(title: str) -> tuple[str, str]:
    """Return (base_title, qualifier) where qualifier is any trailing
    parenthetical / lineage-keyword suffix, both lowercase/whitespace-collapsed.
    Purely mechanical string normalization -- carries no claim of musical identity.
    """
    t = title
    if t.lower().endswith(".mp3"):
        t = t[:-4]
    t = re.sub(r"\s+", " ", t).strip()

    # Strip a trailing "(N)" duplicate-index suffix, e.g. "Foo (1)" -> "Foo"
    m = re.match(r"^(.*)\s\(\d+\)$", t)
    dup_index_suffix = ""
    if m:
        t = m.group(1).strip()

    # Split off one trailing parenthetical qualifier, e.g. "Foo (Remastered)" -> ("Foo", "remastered")
    m = re.match(r"^(.*)\s\(([^)]+)\)$", t)
    qualifier = ""
    base = t
    if m:
        base = m.group(1).strip()
        qualifier = m.group(2).strip().lower()

    base_norm = re.sub(r"\s+", " ", base).strip().lower()
    return base_norm, qualifier


def load_json(path: Path, what: str) -> dict | list:
    if not path.exists():
        raise BuildError(f"{what} not found at {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise BuildError(f"{what} at {path} is not valid JSON: {e}")


def parse_created_at(value: str | None) -> datetime | None:
    if not value:
        return None
    v = value
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def build_render_rows(manifest_files: list[dict], metadata_by_id: dict[str, dict]) -> list[dict]:
    """One row per (drive_file_id) intermediate record, later collapsed into
    one row per unique render. Every manifest mp3 must produce exactly one
    intermediate record -- files missing from metadata are marked incomplete,
    never silently dropped and never given fabricated hash/tag values.
    """
    records = []
    for f in manifest_files:
        fid = f["id"]
        meta = metadata_by_id.get(fid)
        if meta is None:
            records.append({
                "drive_file_id": fid,
                "original_filename": f.get("title"),
                "drive_url": f.get("viewUrl"),
                "file_size_bytes": int(f["fileSize"]) if f.get("fileSize") else None,
                "drive_created_time": f.get("createdTime"),
                "suno_song_id": None,
                "created_at_utc": None,
                "title": f.get("title", "").rsplit(".mp3", 1)[0] if f.get("title") else None,
                "sha256": None,
                "md5": None,
                "duration_seconds": None,
                "sample_rate": None,
                "channels": None,
                "bitrate": None,
                "evidence_status": "download_failed_metadata_only",
                "notes": "Drive download_file_content failed repeatedly for this file (MCP session errors); hash, duration, and Suno tags are unavailable. Title/size/timestamps are from the Drive file listing only.",
            })
            continue
        records.append({
            "drive_file_id": fid,
            "original_filename": meta.get("original_filename"),
            "drive_url": meta.get("drive_view_url"),
            "file_size_bytes": meta.get("drive_file_size_bytes"),
            "drive_created_time": meta.get("drive_created_time"),
            "suno_song_id": meta.get("suno_song_id"),
            "created_at_utc": meta.get("created_at_utc"),
            "title": meta.get("tit2_title") or (meta.get("original_filename") or "").rsplit(".mp3", 1)[0],
            "sha256": meta.get("sha256"),
            "md5": meta.get("md5"),
            "duration_seconds": meta.get("duration_seconds"),
            "sample_rate": meta.get("sample_rate"),
            "channels": meta.get("channels"),
            "bitrate": meta.get("bitrate"),
            "evidence_status": "verified_from_id3_and_hash" if meta.get("suno_song_id") else "hash_verified_no_suno_id3_tag",
            "notes": "" if meta.get("suno_song_id") else "File downloaded and hashed successfully but no Suno song id was found in its ID3 tags.",
        })
    return records


def collapse_to_renders(records: list[dict]) -> tuple[list[dict], dict[str, list[dict]]]:
    """Collapse per-file records into per-render records.
    Grouping key: suno_song_id when known, else the record's own drive_file_id
    (i.e. it stands alone -- never guessed into a group).
    Returns (render_rows, duplicate_groups) where duplicate_groups maps
    group_key -> list of source file records for renders with >1 source file.
    """
    groups: dict[str, list[dict]] = {}
    for r in records:
        key = r["suno_song_id"] or f"__unresolved__{r['drive_file_id']}"
        groups.setdefault(key, []).append(r)

    render_rows = []
    duplicate_groups = {}
    for key, files in groups.items():
        if len(files) > 1:
            hashes = {f["sha256"] for f in files}
            if len(hashes) > 1:
                # Same Suno song id but different bytes -- flag, don't silently merge as "duplicate".
                for f in files:
                    f["notes"] = (f["notes"] + " " if f["notes"] else "") + \
                        "WARNING: shares suno_song_id with another file but sha256 differs -- re-encoded or corrupted copy, not a byte-identical duplicate."
            duplicate_groups[key] = files
            files_sorted = sorted(files, key=lambda f: (f["drive_created_time"] or "9999"))
            primary = files_sorted[0]
            primary = dict(primary)
            primary["notes"] = (primary["notes"] + " " if primary["notes"] else "") + \
                f"Primary of {len(files)} Drive copies sharing this render; see DUPLICATE_GROUPS.csv for the rest. Primary chosen as earliest Drive createdTime -- this is a bookkeeping choice for a single representative row, not a canon/quality judgment."
            render_rows.append(primary)
        else:
            render_rows.append(files[0])

    render_rows.sort(key=lambda r: (r["created_at_utc"] or "9999", r["drive_file_id"]))
    return render_rows, duplicate_groups


def assign_render_ids(render_rows: list[dict]) -> None:
    resolved = [r for r in render_rows if r["suno_song_id"]]
    unresolved = [r for r in render_rows if not r["suno_song_id"]]
    for i, r in enumerate(resolved, start=1):
        r["render_id"] = f"REND-{i:03d}"
    for i, r in enumerate(unresolved, start=1):
        r["render_id"] = f"REND-UNK-{i:02d}"


def detect_sibling_pairs(render_rows: list[dict]) -> list[dict]:
    dated = [r for r in render_rows if r["created_at_utc"]]
    pairs = []
    used = set()
    for i in range(len(dated)):
        for j in range(i + 1, len(dated)):
            a, b = dated[i], dated[j]
            if a["render_id"] in used or b["render_id"] in used:
                continue
            base_a, qual_a = normalize_title(a["title"] or "")
            base_b, qual_b = normalize_title(b["title"] or "")
            if base_a != base_b or qual_a != qual_b:
                continue
            ta, tb = parse_created_at(a["created_at_utc"]), parse_created_at(b["created_at_utc"])
            if ta is None or tb is None:
                continue
            delta = abs((ta - tb).total_seconds())
            if delta <= SIBLING_TIME_THRESHOLD_SECONDS:
                pairs.append({
                    "sibling_pair_id": f"SIB-{len(pairs) + 1:03d}",
                    "render_id_a": a["render_id"],
                    "render_id_b": b["render_id"],
                    "title_a": a["title"],
                    "title_b": b["title"],
                    "created_at_utc_a": a["created_at_utc"],
                    "created_at_utc_b": b["created_at_utc"],
                    "delta_seconds": round(delta, 6),
                    "match_basis": "normalized_title_and_timestamp_within_threshold",
                    "confidence": "high" if delta < 1.0 else "medium",
                    "evidence_status": "inferred",
                    "notes": "Titles match after normalization and creation timestamps are within "
                             f"{SIBLING_TIME_THRESHOLD_SECONDS}s of each other -- consistent with a Suno "
                             "same-prompt A/B generation, but this is inferred, not confirmed by any "
                             "explicit Suno sibling/variation identifier.",
                })
                used.add(a["render_id"])
                used.add(b["render_id"])
                break
    return pairs


def detect_lineage_candidates(render_rows: list[dict], sibling_render_ids: set[str]) -> list[dict]:
    by_base: dict[str, list[dict]] = {}
    for r in render_rows:
        base, qual = normalize_title(r["title"] or "")
        by_base.setdefault(base, []).append((r, qual))

    candidates = []
    for base, items in by_base.items():
        if len(items) < 2:
            continue
        plain = [r for r, q in items if q == ""]
        qualified = [(r, q) for r, q in items if q != ""]
        if not qualified:
            continue
        parent_pool = plain if plain else [min(items, key=lambda ri: ri[0]["created_at_utc"] or "9999")[0]]
        parent = min(parent_pool, key=lambda r: r["created_at_utc"] or "9999")
        for r, q in qualified:
            if r["render_id"] == parent["render_id"]:
                continue
            if r["render_id"] in sibling_render_ids and parent["render_id"] in sibling_render_ids:
                continue
            keyword_hit = next((k for k in LINEAGE_KEYWORDS if k in q), None)
            candidates.append({
                "lineage_id": f"LIN-{len(candidates) + 1:03d}",
                "render_id": r["render_id"],
                "title": r["title"],
                "inferred_parent_render_id": parent["render_id"],
                "parent_title": parent["title"],
                "relationship_type_guess": keyword_hit or "same_base_title_different_qualifier",
                "confidence": "medium" if keyword_hit else "low",
                "evidence_status": "inferred_from_title_text_only",
                "notes": "Base title matches after stripping one parenthetical qualifier "
                         f"('{q}'); no Suno-native parent/child link was found for this pair. "
                         "This is a title-text inference, not a verified fact.",
            })
    return candidates


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in fieldnames})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--metadata", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    args = ap.parse_args()

    try:
        manifest = load_json(args.manifest, "Drive manifest")
        metadata = load_json(args.metadata, "Extracted metadata")
    except BuildError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    manifest_files = manifest.get("files") if isinstance(manifest, dict) else manifest
    if not manifest_files:
        print("ERROR: manifest contains no files", file=sys.stderr)
        return 1

    metadata_by_id = {m["drive_file_id"]: m for m in metadata}

    seen_ids = set()
    for f in manifest_files:
        if f["id"] in seen_ids:
            print(f"ERROR: duplicate drive_file_id {f['id']} in manifest -- refusing to guess which entry is authoritative", file=sys.stderr)
            return 1
        seen_ids.add(f["id"])

    records = build_render_rows(manifest_files, metadata_by_id)
    render_rows, duplicate_groups = collapse_to_renders(records)
    assign_render_ids(render_rows)

    dup_group_ids_by_key = {key: f"DUP-{i+1:03d}" for i, key in enumerate(sorted(duplicate_groups.keys()))}
    render_by_key = {}
    for r in render_rows:
        key = r["suno_song_id"] or f"__unresolved__{r['drive_file_id']}"
        render_by_key[key] = r
    for key, dup_id in dup_group_ids_by_key.items():
        render_by_key[key]["duplicate_group_id"] = dup_id
    for r in render_rows:
        r.setdefault("duplicate_group_id", "")

    sibling_pairs = detect_sibling_pairs(render_rows)
    sibling_render_ids = set()
    render_to_sibling_id = {}
    for p in sibling_pairs:
        sibling_render_ids.add(p["render_id_a"])
        sibling_render_ids.add(p["render_id_b"])
        render_to_sibling_id[p["render_id_a"]] = p["sibling_pair_id"]
        render_to_sibling_id[p["render_id_b"]] = p["sibling_pair_id"]
    for r in render_rows:
        r["sibling_pair_id"] = render_to_sibling_id.get(r["render_id"], "")

    lineage_candidates = detect_lineage_candidates(render_rows, sibling_render_ids)
    render_to_lineage = {}
    render_to_parent = {}
    render_to_lineage_conf = {}
    for c in lineage_candidates:
        render_to_lineage[c["render_id"]] = c["lineage_id"]
        render_to_parent[c["render_id"]] = c["inferred_parent_render_id"]
        render_to_lineage_conf[c["render_id"]] = c["confidence"]
    for r in render_rows:
        r["lineage_id"] = render_to_lineage.get(r["render_id"], "")
        r["inferred_parent_render_id"] = render_to_parent.get(r["render_id"], "")
        r["lineage_confidence"] = render_to_lineage_conf.get(r["render_id"], "")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    register_fields = [
        "render_id", "suno_song_id", "title", "original_filename", "drive_file_id",
        "drive_url", "created_at_utc", "duration_seconds", "file_size_bytes",
        "sha256", "md5", "sample_rate", "channels", "bitrate",
        "duplicate_group_id", "sibling_pair_id", "lineage_id",
        "inferred_parent_render_id", "lineage_confidence", "evidence_status", "notes",
    ]
    write_csv(args.out_dir / "RENDER_REGISTER.csv", render_rows, register_fields)

    dup_rows = []
    for key, dup_id in dup_group_ids_by_key.items():
        for f in sorted(duplicate_groups[key], key=lambda x: (x["drive_created_time"] or "9999")):
            dup_rows.append({
                "duplicate_group_id": dup_id,
                "render_id": render_by_key[key]["render_id"],
                "suno_song_id": key if not key.startswith("__unresolved__") else "",
                "drive_file_id": f["drive_file_id"],
                "original_filename": f["original_filename"],
                "drive_url": f["drive_url"],
                "drive_created_time": f["drive_created_time"],
                "file_size_bytes": f["file_size_bytes"],
                "sha256": f["sha256"],
                "is_primary_in_register": "yes" if f["drive_file_id"] == render_by_key[key]["drive_file_id"] else "no",
            })
    write_csv(
        args.out_dir / "DUPLICATE_GROUPS.csv", dup_rows,
        ["duplicate_group_id", "render_id", "suno_song_id", "drive_file_id", "original_filename",
         "drive_url", "drive_created_time", "file_size_bytes", "sha256", "is_primary_in_register"],
    )

    write_csv(
        args.out_dir / "SIBLING_PAIRS.csv", sibling_pairs,
        ["sibling_pair_id", "render_id_a", "render_id_b", "title_a", "title_b",
         "created_at_utc_a", "created_at_utc_b", "delta_seconds", "match_basis",
         "confidence", "evidence_status", "notes"],
    )

    write_csv(
        args.out_dir / "LINEAGE_CANDIDATES.csv", lineage_candidates,
        ["lineage_id", "render_id", "title", "inferred_parent_render_id", "parent_title",
         "relationship_type_guess", "confidence", "evidence_status", "notes"],
    )

    total_files = len(manifest_files)
    unique_renders = len(render_rows)
    unresolved = len([r for r in render_rows if not r["suno_song_id"]])
    print(f"source mp3 files in manifest: {total_files}")
    print(f"unique renders written to RENDER_REGISTER.csv: {unique_renders} "
          f"({unresolved} unresolved -- download/hash unavailable)")
    print(f"duplicate groups: {len(duplicate_groups)}")
    print(f"sibling pairs: {len(sibling_pairs)}")
    print(f"lineage candidates: {len(lineage_candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
