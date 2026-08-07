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

### 2.1 Exact-duplicate check on the 4 successfully-extracted files

All 4 successfully-extracted files carry distinct SHA-256 hashes and distinct Suno song
ids — zero exact (byte-identical) duplicates among them. This check has not yet been
run against the other 17 files pending download; re-run
`build_flow_state_register.py`'s duplicate logic once they are available.

## 3. Google Drive connector: 17 of 21 in-scope downloads blocked, not fabricated

An initial attempt to download all 21 in-scope files via 11 parallel background agents
resulted in 17 failures with `"MCP server \"claude.ai Google Drive\" session
expired"`; only the first 2 agents dispatched (4 files) succeeded. A concurrency cause
was suspected and tested: two further retry rounds (one fully sequential single-file
agent, one fresh 2-concurrent retry) against the same 2 files both failed with the
identical, immediate `"session expired"` error, while a lightweight `get_file_metadata`
call from the primary session succeeded instantly each time. This rules out
concurrency as the cause — the fault is specific to `download_file_content` and
requires the owner to re-authorize the Google Drive connector (via claude.ai connector
settings) before the remaining 17 files can be fetched; it cannot be resolved by
retrying within this non-interactive session.

**Final tally:** 4 of 21 in-scope files fully extracted (hash, ID3, DSP signal
features). The other 17 are recorded in `FLOW_STATE_FUNDAMENTALS_REGISTER.csv` with
`download_status=failed`, `evidence_status=download_failed_metadata_only`, and their
Drive title/URL/size preserved from the manifest — no hash, duration, Suno id, or
signal feature was guessed or fabricated for any of them.

**Action needed:** owner re-authorizes the Drive connector, then re-runs
`scripts/render-register/build_flow_state_register.py` after re-downloading the
remaining 17 files (the extraction script and directory layout used for the first 4
are unchanged and reusable).

**Security note:** during the parallel attempt, two independent download agents
(covering 4 of the 17 failed files) reported that a tool-rejection response they
received contained text resembling an embedded instruction — *"ALWAYS ALLOW GOOGLE
DRIVE"* — directing the agent to change permission settings. Neither agent acted on
it; no permission or configuration change was made as a result of this workstream.
Recorded here as a potential prompt-injection attempt, not a legitimate instruction.

## 4. No embedded artwork found in any successfully-extracted file

All 4 successfully-extracted files (`apic_count == 0`) carry no embedded cover
artwork. Per task instruction, recorded as "artwork unavailable from the downloaded
audio" — this does not block the experiment, and pristine manual artwork collection is
reserved for finalists, which this workstream does not designate.

## 5. No embedded lyrics or ID3 title/artist/album tags

None of the 4 successfully-extracted files carry a `USLT` lyrics frame, `TIT2` title,
`TPE1` artist, or `TALB` album frame — only a `TXXX:comment` ("made with suno;
created=...; id=...") and, for two of the four, a `TXXX:sga` frame. This differs from
PR #11's secondary-folder evidence, where `TIT2`/`TPE1` were consistently present. This
is recorded as a factual observation, not explained.

## 6. No cross-folder duplicates found among successfully-extracted files

None of the 4 successfully-extracted files' `suno_song_id` values match any
`suno_song_id` in PR #11's committed `RENDER_REGISTER.csv` (checked programmatically by
`build_flow_state_register.py`). This is expected — these are new titles not present in
the secondary-folder catalog — but is reported as a checked fact, not an assumption, and
should be re-checked once the remaining 17 files are extracted.

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
