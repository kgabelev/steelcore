#!/usr/bin/env python3
"""
Build the Flow State Fundamentals comparison register (this workstream's isolated
extension of the render-register architecture from catalog/render-register-v1).

Read-only, deterministic, reproducible. Never deletes, renames, moves, or writes to
any source audio file or Drive object. Reads:

  --manifest    Full primary-folder Drive listing (all files found in the primary
                batch folder), with an `in_scope` flag per file marking which ones
                belong to the Flow State Fundamentals / Concrete Flow Fundamentals
                lyric-guidance remix family (see OPEN_CORRECTIONS.md sec 9.1 for why
                the rest are excluded).
  --metadata    Extracted metadata JSON (sha256, ffprobe fields, ID3 fields, librosa
                signal features) for every in-scope file that was successfully
                downloaded and hashed, or a `download_status: failed` stub for files
                that could not be fetched. Never guesses missing fields.
  --secondary-register  The existing catalog/render-register/RENDER_REGISTER.csv from
                PR #11, used ONLY to detect cross-folder duplicates by suno_song_id
                (a file appearing in both Drive folders becomes one logical audio
                record, not two creative outputs). This script never re-derives or
                overwrites that file.

Outputs (written fresh each run to --out-dir):
  FLOW_STATE_FUNDAMENTALS_REGISTER.csv, FLOW_STATE_SIBLING_PAIRS.csv

Identity model: a render is identified by its Suno song id (WOAS URL / COMM "id="
field). Two in-scope files sharing a suno_song_id AND sha256 are the same render
(exact duplicate). A file whose suno_song_id or hash could not be extracted gets its
own unresolved row -- never merged into another render by guessing.
"""
import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SIBLING_TIME_THRESHOLD_SECONDS = 2.0

GENRE_FAMILY_KEYWORDS = [
    ("reggaetón fusion experiment", "Reggaetón Fusion Experiment"),
    ("reggaeton fusion experiment", "Reggaetón Fusion Experiment"),
    ("playful reggae mix", "Playful Reggae Mix"),
    ("slow burn version", "Slow Burn Version"),
    ("chill studio session", "Chill Studio Session"),
    ("clean studio mix", "Clean Studio Mix"),
    ("isolated studio version", "Isolated Studio Version"),
    ("studio pocket remix", "Studio Pocket Remix"),
    ("organic roots fusion", "Organic Roots Fusion"),
    ("concrete flow fundamentals", "Concrete Flow Fundamentals (base)"),
    ("flow state fundamentals", "Flow State Fundamentals (base)"),
]


class BuildError(Exception):
    pass


def load_json(path: Path, what: str):
    if not path.exists():
        raise BuildError(f"{what} not found at {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise BuildError(f"{what} at {path} is not valid JSON: {e}")


def normalize_title(filename: str) -> str:
    t = filename
    if t.lower().endswith(".mp3"):
        t = t[:-4]
    t = re.sub(r"_\d+$", "", t)
    t = re.sub(r"\s\(\d+\)$", "", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def genre_family_from_title(filename: str) -> str:
    n = (filename or "").lower()
    for needle, label in GENRE_FAMILY_KEYWORDS:
        if needle in n:
            return label
    return "unclassified"


def extract_suno_created_at(record: dict):
    for frame_text in list(record.get("comm_frames", {}).values()) + list(record.get("txxx_frames", {}).values()):
        if frame_text and "created=" in frame_text:
            text = frame_text.split("created=")[-1].split(";")[0].strip()
            if text.endswith("Z"):
                text = text[:-1] + "+00:00"
            try:
                dt = datetime.fromisoformat(text)
            except ValueError:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
    return None


def load_secondary_register_by_suno_id(path: Path) -> dict:
    if not path.exists():
        return {}
    out = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("suno_song_id"):
                out[row["suno_song_id"]] = row
    return out


def build(manifest_files: list[dict], metadata_by_id: dict, secondary_by_suno_id: dict) -> list[dict]:
    in_scope = [f for f in manifest_files if f.get("in_scope")]
    rows = []
    for f in in_scope:
        fid = f["id"]
        meta = metadata_by_id.get(fid)
        base = {
            "original_filename": f.get("title"),
            "drive_file_id": fid,
            "drive_url": f.get("viewUrl"),
            "source_folder": "primary_flow_state_batch",
            "file_size_bytes": f.get("fileSize"),
        }
        if meta is None or meta.get("download_status") == "failed":
            rows.append({
                **base,
                "download_status": "failed",
                "evidence_status": "download_failed_metadata_only",
                "notes": (meta or {}).get("error", "not attempted"),
            })
            continue
        suno_id = meta.get("suno_song_id")
        created_at = extract_suno_created_at(meta)
        cross = secondary_by_suno_id.get(suno_id) if suno_id else None
        rows.append({
            **base,
            "suno_song_id": suno_id,
            "suno_song_url": meta.get("woas_url"),
            "created_at_utc": created_at.isoformat() if created_at else None,
            "duration_seconds": meta.get("duration_seconds"),
            "sha256": meta.get("sha256"),
            "md5": meta.get("md5"),
            "sample_rate": meta.get("sample_rate"),
            "channels": meta.get("channels"),
            "bitrate": meta.get("bitrate"),
            "genre_family_by_title": genre_family_from_title(f.get("title")),
            "has_artwork": meta.get("has_artwork"),
            "artwork_sha256": meta.get("artwork_sha256"),
            "lyrics_availability": "embedded_uslt_present" if meta.get("uslt_lyrics") else "not_embedded",
            "tempo_bpm_estimate": meta.get("tempo_bpm_estimate"),
            "spectral_centroid_hz_mean": meta.get("spectral_centroid_hz_mean"),
            "percussive_energy_ratio": meta.get("percussive_energy_ratio"),
            "signal_features_note": meta.get("signal_features_note"),
            "cross_folder_match_render_id": cross.get("render_id") if cross else "",
            "cross_folder_evidence": "same_suno_song_id_as_PR11_secondary_register" if cross else "",
            "download_status": "ok",
            "evidence_status": "verified_from_id3_and_hash" if suno_id else "hash_verified_no_suno_id3_tag",
            "id3_error": meta.get("id3_error"),
            "ffprobe_error": meta.get("ffprobe_error"),
            "size_matches_drive_listing": meta.get("size_matches_drive_listing"),
            "prompt_availability": "not_embedded_in_id3",
            "confirmed_or_candidate_parent": cross.get("render_id") if cross else "none_identified",
            "lineage_confidence": "confirmed_cross_folder_suno_id_match" if cross else "unknown",
            "generation_depth": "unknown",
            "owner_rating": "",
            "owner_notes": "",
            "analyst_observations": (
                f"Title implies '{genre_family_from_title(f.get('title'))}' style variant. "
                f"Duration {meta.get('duration_seconds'):.1f}s, tempo estimate "
                f"{meta.get('tempo_bpm_estimate')} BPM (automated DSP, not a listened judgment), "
                f"percussive-energy ratio {meta.get('percussive_energy_ratio')}. "
                "No perceptual genre/instrument/vocal-delivery observation was made -- no "
                "listening capability available to this workstream."
                if meta.get("duration_seconds") is not None else ""
            ),
            "canon_status": "not_canon",
            "release_status": "unresolved",
            "unresolved_questions": (
                "Original ~4-minute rap-writing-guidance parent track not identified in either "
                "Drive folder; no Suno-native parent/remix link recovered for this render; "
                "perceptual genre/instrumentation/vocal-delivery not evaluated."
            ),
        })
    return rows


def detect_sibling_pairs(rows: list[dict]) -> list[dict]:
    dated = [r for r in rows if r.get("created_at_utc") and r.get("download_status") == "ok"]
    pairs = []
    used = set()
    for i in range(len(dated)):
        for j in range(i + 1, len(dated)):
            a, b = dated[i], dated[j]
            if a["drive_file_id"] in used or b["drive_file_id"] in used:
                continue
            if normalize_title(a["original_filename"]) != normalize_title(b["original_filename"]):
                continue
            ta = datetime.fromisoformat(a["created_at_utc"])
            tb = datetime.fromisoformat(b["created_at_utc"])
            delta = abs((ta - tb).total_seconds())
            if delta <= SIBLING_TIME_THRESHOLD_SECONDS:
                pairs.append({
                    "sibling_pair_id": f"FSF-SIB-{len(pairs) + 1:03d}",
                    "drive_file_id_a": a["drive_file_id"],
                    "drive_file_id_b": b["drive_file_id"],
                    "title_a": a["original_filename"],
                    "title_b": b["original_filename"],
                    "created_at_utc_a": a["created_at_utc"],
                    "created_at_utc_b": b["created_at_utc"],
                    "delta_seconds": round(delta, 6),
                    "match_basis": "normalized_title_and_timestamp_within_threshold",
                    "confidence": "high" if delta < 1.0 else "medium",
                    "evidence_status": "inferred",
                })
                used.add(a["drive_file_id"])
                used.add(b["drive_file_id"])
                break
    return pairs


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in fieldnames})


REGISTER_FIELDS = [
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--metadata", required=True, type=Path)
    ap.add_argument("--secondary-register", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    args = ap.parse_args()

    try:
        manifest = load_json(args.manifest, "primary-folder manifest")
        metadata_list = load_json(args.metadata, "extracted metadata")
    except BuildError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    manifest_files = manifest.get("files") if isinstance(manifest, dict) else manifest
    metadata_by_id = {m["drive_file_id"]: m for m in metadata_list}
    secondary_by_suno_id = load_secondary_register_by_suno_id(args.secondary_register)

    rows = build(manifest_files, metadata_by_id, secondary_by_suno_id)
    rows.sort(key=lambda r: r["original_filename"] or "")
    for i, r in enumerate(rows, start=1):
        r["record_id"] = f"FSF-{i:03d}"

    sibling_pairs = detect_sibling_pairs(rows)
    row_to_sibling_id = {}
    for p in sibling_pairs:
        row_to_sibling_id[p["drive_file_id_a"]] = p["sibling_pair_id"]
        row_to_sibling_id[p["drive_file_id_b"]] = p["sibling_pair_id"]
    for r in rows:
        r["paired_take_family"] = row_to_sibling_id.get(r["drive_file_id"], "")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "FLOW_STATE_FUNDAMENTALS_REGISTER.csv", rows, REGISTER_FIELDS)

    write_csv(
        args.out_dir / "FLOW_STATE_SIBLING_PAIRS.csv", sibling_pairs,
        ["sibling_pair_id", "drive_file_id_a", "drive_file_id_b", "title_a", "title_b",
         "created_at_utc_a", "created_at_utc_b", "delta_seconds", "match_basis",
         "confidence", "evidence_status"],
    )

    total_in_scope = len(manifest_files and [f for f in manifest_files if f.get("in_scope")] or [])
    ok = len([r for r in rows if r.get("download_status") == "ok"])
    failed = len([r for r in rows if r.get("download_status") == "failed"])
    xfold = len([r for r in rows if r.get("cross_folder_match_render_id")])
    print(f"in-scope files in manifest: {total_in_scope}")
    print(f"register rows: {len(rows)} (ok={ok}, download_failed={failed})")
    print(f"sibling pairs: {len(sibling_pairs)}")
    print(f"cross-folder suno_song_id matches against PR #11 secondary register: {xfold}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
