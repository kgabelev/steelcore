# Open Corrections — Steel Render Register (v1)

Generated alongside `RENDER_REGISTER.csv`, `DUPLICATE_GROUPS.csv`, `SIBLING_PAIRS.csv`,
and `LINEAGE_CANDIDATES.csv` from the Google Drive source folder:
`https://drive.google.com/drive/folders/1whcWEFpgkipHvWMRQe9QYtya3lJt2fCg`.

This document lists every place where this register's measured findings
diverge from the assumptions it was asked to verify, every ambiguous or
unresolved item, and every historical record it could not reconcile against.
Nothing below overwrites prior evidence; it is additive.

## 1. File count does not match the assumed 35

The source folder contains **37 `.mp3` files**, not 35, plus one non-audio
Google Doc (see §4). This was verified twice independently: once via an
unfiltered folder listing and once via a `mimeType = 'audio/mpeg'`-filtered
query, both returning the same 37 file IDs. See
`catalog/render-register/evidence/drive_mp3_listing.json` for the full listing.

**Open question for the owner:** was the folder modified after the "35
files" figure was recorded, or was that figure wrong from the start? Two of
the 37 files could not be downloaded and hashed (§2), so it is not yet known
whether they add 2 genuinely new renders or 1-2 more duplicates.

## 2. Two source files could not be downloaded

`Golden string cypher.mp3` (`drive_file_id=14Fnd_TB-7Cv42s3wA-WFwakqzfF2tl8G`)
and `Gypsy Strings (Trap Femme Edit).mp3`
(`drive_file_id=1R39wxWwiWopsy61faCnITE77MWC1VfDR`) both failed to download
through the available Google Drive MCP tool, consistently, across roughly
8 attempts each (alone and in batches), while `get_file_metadata` succeeded
for both and every other file in the folder — including files of similar or
larger size — downloaded without issue. This looks like a real limitation
or bug in that specific tool call for these two files, not a transient
network blip.

Consequences:
- Both appear in `RENDER_REGISTER.csv` as `REND-UNK-01` and `REND-UNK-02`
  with `evidence_status=download_failed_metadata_only`. Only their Drive
  title, file size, and URL are known — no hash, duration, sample rate,
  Suno song id, or creation timestamp.
- Neither could be evaluated for duplicate, sibling-pair, or lineage
  membership, because that evaluation depends on the hash and ID3 fields
  this register never guesses.
- **Action needed:** re-attempt the download through a different path (a
  fresh Drive session, browser export, or direct authenticated fetch) and
  re-run `scripts/render-register/build_render_register.py` once both files
  have real metadata.

## 3. Verified vs. assumed: unique render count

The "approximately 32 unique renders" figure holds **exactly** for the 35
files that did download: 32 unique Suno song ids, 32 unique SHA-256 hashes,
and the two counts agree file-for-file (every duplicate pair shares both the
same `suno_song_id` and the same `sha256` — true byte-identical
re-downloads, not re-encodes). See `DUPLICATE_GROUPS.csv` for the 3 pairs
(`DUP-001`..`DUP-003`).

This figure is **not yet confirmed for the full 37-file folder** — it
depends on resolving §2.

## 4. Non-audio file found in the source folder

`Untitled document` (`id=1b7rKMUMOfDhlXSFKdxXx0uKid7BjS7WSOz0dnIfrbWg`,
Google Doc, created 2026-08-06T21:33) sits alongside the 37 mp3s. It is a
Suno share-page text export/caption for "Golden String Cypher" and, notably,
contains an explicit line:

> Cover of [Golden string cypher](https://suno.com/song/aaf957b9-a5d3-4ff6-b2a9-3682ac2b12ba)

`aaf957b9-a5d3-4ff6-b2a9-3682ac2b12ba` is the confirmed `suno_song_id` of
`REND-022` (`Golden string cypher (3).mp3`) in this register. This is
genuine Suno-sourced lineage evidence (not a title-text inference), but the
**cover render itself is not identifiable among the 37 audio files** in this
folder — there is no mp3 whose Suno song id matches whatever "cover"
generated this doc. This is logged as a missing/unresolved track, not
folded into `LINEAGE_CANDIDATES.csv`, because that file only holds
title-text inferences and this is a stronger, differently-sourced claim that
deserves separate handling once the actual audio is located.

This document was excluded from `RENDER_REGISTER.csv` (it is not an audio
render) and left untouched in Drive.

## 5. No existing catalog workbook was found in-repo to check against

The task's "known findings to verify" mention that an existing catalog
workbook contains at least two potentially incorrect Suno song IDs.
`catalog/source-inventory.yaml` — the only in-repo catalog inventory — does
not track Suno song IDs at all (see its `next_batch_requirements`, which
still lists "inventory all Suno song and variation links" as outstanding).
No other workbook or track sheet was found under `catalog/`, `research/`,
`legal/`, or `artist-bible/`.

**Action needed:** the owner should point to where that workbook actually
lives (an external Google Sheet, a Suno account view, etc.) so its Suno IDs
can be diffed against the verified `suno_song_id` values in
`RENDER_REGISTER.csv`. Until then, "at least two incorrect song IDs" remains
unverified against this register — this register can only assert that its
own 32 confirmed IDs were read directly from ID3 tags, not guessed.

## 6. Bookkeeping choice, not a canon decision

For each of the 3 duplicate-file groups, `RENDER_REGISTER.csv` lists one
Drive file as the representative row (`is_primary_in_register=yes` in
`DUPLICATE_GROUPS.csv`), chosen as the earlier-uploaded copy by Drive
`createdTime`. This is only a bookkeeping necessity for a one-row-per-render
table — both copies are fully preserved as separate rows in
`DUPLICATE_GROUPS.csv`. No render, remix, or version is being marked as
canon, approved, or "the winner" by this choice.

## 7. Isolated paths used for this workstream — reconciliation deferred

Per owner instruction, all output of this workstream was written under
new, isolated subdirectories rather than the paths named in the original
task spec, to avoid colliding with two other active, unmerged workstreams
already tracked in `EXECUTION_LEDGER.yaml` (`creative-catalog-import` owns
`catalog/`, `research-import` owns `research/`):

| Written here (this workstream) | Originally requested path | Reconciliation owner/trigger |
|---|---|---|
| `catalog/render-register/RENDER_REGISTER.csv` | `catalog/RENDER_REGISTER.csv` | after `creative-catalog-import` (PR #5 lineage) settles |
| `catalog/render-register/DUPLICATE_GROUPS.csv` | `catalog/DUPLICATE_GROUPS.csv` | same |
| `catalog/render-register/SIBLING_PAIRS.csv` | `catalog/SIBLING_PAIRS.csv` | same |
| `catalog/render-register/LINEAGE_CANDIDATES.csv` | `catalog/LINEAGE_CANDIDATES.csv` | same |
| `catalog/render-register/OPEN_CORRECTIONS.md` (this file) | `catalog/OPEN_CORRECTIONS.md` | same |
| `research/render-register/EXP-000-suno-seed-variance.md` | `research/music-science/EXP-000-suno-seed-variance.md` | after `research-import` settles |
| `scripts/render-register/build_render_register.py` | `scripts/build_render_register.py` | no blocking owner; can move any time |
| `tests/render-register/` | `tests/` | once M4 `creative-session-runtime` gets an assigned owner, or sooner by explicit approval |
| `catalog/source-inventory.yaml` | (update in place) | not touched by this workstream; still needs a follow-up entry once the above CSVs are reconciled into `catalog/` proper |

None of the above paths were modified by this workstream. This table is the
complete list of what still needs to move and where.

## 8. Unresolved / assumption reminders carried into the register itself

- Every `SIBLING_PAIRS.csv` row is labeled `evidence_status=inferred` —
  matching title + sub-second creation-timestamp deltas are strong
  circumstantial evidence of Suno's same-prompt A/B generation, but Suno
  does not expose an explicit sibling/variation ID in the ID3 tags this
  register read, so it is not a confirmed fact.
- Every `LINEAGE_CANDIDATES.csv` row is labeled
  `evidence_status=inferred_from_title_text_only` and capped at
  `confidence=medium`, except where a Suno-native lineage link exists (see
  §4, which is deliberately kept out of that file for now).
- Multiple identically-titled "plain" renders (e.g. three separate "Real
  Madrid" renders on different days, five separate "Golden string cypher"
  renders) are **not** treated as lineage or sibling relationships by this
  register — they are just repeated generations of the same prompt title,
  logged as independent renders.
