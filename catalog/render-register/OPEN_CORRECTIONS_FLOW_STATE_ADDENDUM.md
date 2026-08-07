# Open Corrections Addendum — Flow State Fundamentals Batch

Written by the `research/flow-state-fundamentals` workstream, stacked on top of
`catalog/render-register-v1` (PR #11) per owner instruction. This is a separate file
rather than an edit to `OPEN_CORRECTIONS.md` so it does not touch content authored by
the still-unmerged PR #11 workstream. Nothing below overwrites prior evidence; it is
additive, covering the primary batch folder
(`https://drive.google.com/drive/folders/1r1m6CS7wiZ78mEtvGrQ4R-x5wbw8pZlF`, inside
`2026-08-06_FLOW_STATE_FUNDAMENTALS_RAW_BATCH`).

## 1. Primary folder contains two unrelated creative lineages

The primary batch folder contains **35 mp3 files**, verified via an unfiltered
`parentId` folder listing (`catalog/render-register/evidence/flow_state_primary_manifest.json`).
Of these:

- **21 files** carry titles containing "Flow State Fundamentals" or "Concrete Flow
  Fundamentals" — the lyric-guidance remix family this experiment record is about.
  These are the in-scope files for this workstream's deep extraction (hash, ID3,
  artwork, DSP signal features), captured in `FLOW_STATE_FUNDAMENTALS_REGISTER.csv`.
- **14 files** are out of scope: titles matching pre-existing renders already
  catalogued in PR #11's secondary-folder register (`Circle Stays Tight (All The Way
  Up Remix)` x2, `Golden String Cypher`/`Golden String Cypher 250` x4, `Real
  Madrid`/`Real Madrid Remastered` x4), or a new but unrelated title (`Paco de Lucia
  Legend Cypher`/`...Remastered` x4) with no connection to the rap-lyric-guidance
  experiment's subject matter. These 14 were inventoried (filename, Drive ID, URL,
  MIME, size, timestamps — see `evidence/flow_state_primary_manifest.json`, `in_scope:
  false`) but **not downloaded** by this workstream. Flagged here for a future,
  separate catalog-register follow-up, not analyzed further.

This means the task's "approximately 26 individual new outputs" estimate does not hold
folder-wide (35 total) but is close for the in-scope experiment family alone (21).

## 2. No file-size-identical pairs within the in-scope family

Unlike PR #11's secondary-folder `DUPLICATE_GROUPS.csv` (three byte-identical
re-download pairs), **no two same-titled files among the 21 in-scope files share an
identical file size**. The `_1`/`_2`/`_3`-suffixed files are therefore not simple
re-uploads of one render — they are independent Suno generations sharing a title, or
same-prompt sibling renders (distinguished by matching Suno creation-timestamp deltas,
per `FLOW_STATE_SIBLING_PAIRS.csv`).

### 2.1 Exact-duplicate check on all 21 in-scope files

All 21 files carry distinct SHA-256 hashes and distinct Suno song ids — zero exact
(byte-identical) duplicates in this batch. 20 of the 21 resolve into 10 sibling pairs
(matching normalized title + Suno creation timestamps 0.0–2.0s apart); the lone
unpaired file is `Concrete Flow Fundamentals Chill Studio Session.mp3`, which has no
second Drive file sharing its title in this folder.

## 3. Google Drive connector: `download_file_content` proved unreliable; resolved via `gdown`

An initial attempt to download all 21 in-scope files via 11 parallel background agents
resulted in 17 failures with `"MCP server \"claude.ai Google Drive\" session
expired"`; only the first 2 agents dispatched (4 files) succeeded. A concurrency cause
was suspected and tested: two further retry rounds (one fully sequential single-file
agent, one fresh 2-concurrent retry) against the same files both failed with the
identical, immediate `"session expired"` error, while a lightweight `get_file_metadata`
call from the primary session succeeded instantly each time — ruling out concurrency.

The owner then reauthorized the Google Drive connector. **This did not resolve the
fault**: a further round of 4 parallel retry agents against the remaining 17 files (21
total download attempts, 3 tries each) again failed with the identical error, while
`get_file_metadata` continued to succeed throughout. The owner confirmed via Drive's
own web UI that the folder, files, and sharing were all intact and correctly
configured — this was never a problem with the underlying Drive folder or its access
grant, only with the Claude-side `download_file_content` MCP tool specifically.

**Resolution:** per owner instruction, the remaining 17 files were downloaded instead
via `gdown` (installed into the workstream's isolated venv) against the shared folder's
public/link-accessible file IDs — a non-MCP path that does not depend on the flaky
tool. Every file's local size was verified byte-for-byte against the Drive listing
(`flow_state_primary_manifest.json`) immediately after download and before any
extraction ran; all 17 matched exactly, with zero size mismatches. The 4 files
originally fetched via the MCP tool were **not** re-downloaded — `gdown` was used only
for the 17 that were still pending.

**Final tally:** 21 of 21 in-scope files fully extracted (hash, ID3, artwork check, DSP
signal features). No hash, duration, Suno id, or signal feature was ever guessed or
fabricated for any file at any point — files without evidence were carried as
`download_status=failed` until real data replaced them.

**Tooling note for future ingestion work in this repo:** `download_file_content` on
the Google Drive MCP connector is not reliable for batches of this size/frequency in
this environment, independent of authorization state. `gdown` against Drive-shared
links is a working fallback for files with link-sharing enabled; it does not work for
files requiring account-specific access.

**Security note:** during the parallel attempts (both pre- and post-reauthorization),
independent download agents repeatedly reported that a tool-rejection response they
received contained text resembling an embedded instruction — *"ALWAYS ALLOW GOOGLE
DRIVE"* — directing the agent to change permission settings. No agent acted on it; no
permission or configuration change was made as a result of this workstream at any
point. Recorded here as a potential prompt-injection attempt, not a legitimate
instruction.

## 4. No embedded artwork found in any file

All 21 files (`apic_count == 0` throughout) carry no embedded cover artwork. Per task
instruction, recorded as "artwork unavailable from the downloaded audio" — this does
not block the experiment, and pristine manual artwork collection is reserved for
finalists, which this workstream does not designate.

## 5. No embedded lyrics or ID3 title/artist/album tags

None of the 21 files carry a `USLT` lyrics frame, `TIT2` title, `TPE1` artist, or
`TALB` album frame — only a `TXXX:comment` ("made with suno; created=...; id=...") and,
for 2 of the 21, a `TXXX:sga` frame. This differs from PR #11's secondary-folder
evidence, where `TIT2`/`TPE1` were consistently present. Recorded as a factual
observation, not explained.

## 6. No cross-folder duplicates found among any in-scope files

None of the 21 files' `suno_song_id` values match any `suno_song_id` in PR #11's
committed `RENDER_REGISTER.csv` (checked programmatically by
`build_flow_state_register.py` across the full in-scope set). This is expected — these
are new titles not present in the secondary-folder catalog — but is reported as a
checked fact across all 21 records, not an assumption.

## 7. No perceptual (listening) audio analysis was performed

This workstream has no audio-listening or audio-classification tool. Genre, guitar
character, vocal delivery, and similar perceptual fields are populated only from (a)
filename/title text, which plausibly reflects the Suno style prompt the owner used, and
(b) automated `librosa` DSP signal features (tempo estimate, spectral centroid,
percussive-energy ratio) computed directly from the audio waveform. These DSP numbers
are objective measurements, not genre or instrument classifications, and every register
row carrying them says so explicitly (`signal_features_note`). Per the task's own
"IMPORTANT AUDIO CORRECTION" instruction, **no guitar in any of these files is labeled
nylon-string/flamenco/Spanish/rasgueado** — that would require actual listening, which
was not performed. Perceptual confirmation is deferred to the owner or a future session
with listening capability.

## 8. Original guidance-lesson parent track not located

Neither the primary nor the secondary Drive folder (as previously catalogued by PR #11)
was found to contain a distinct ~4-minute track matching the owner's description of the
original rap-writing-guidance source. Its Suno song id is unknown. This is the single
largest open gap in this experiment's lineage evidence — see `EXP-001` §"Evidence
limitations".
