# EXP-001 — Flow State Fundamentals: Embedded Lyrical Guidance Remix Experiment

**Status:** preliminary observational, not controlled, not reproduced.
**Dataset:** `catalog/render-register/FLOW_STATE_FUNDAMENTALS_REGISTER.csv`, built by
`scripts/render-register/build_flow_state_register.py` from the Drive folder
`https://drive.google.com/drive/folders/1r1m6CS7wiZ78mEtvGrQ4R-x5wbw8pZlF`
("My Workspace Unzipped Files", inside `2026-08-06_FLOW_STATE_FUNDAMENTALS_RAW_BATCH`),
cross-referenced against the existing secondary-folder register
(`catalog/render-register/RENDER_REGISTER.csv`, from PR #11) for lineage only — the
secondary folder was **not** re-ingested.
**Sample size:** 21 in-scope files identified; **4 fully extracted, 17 blocked on a
Google Drive connector auth issue** (see `OPEN_CORRECTIONS_FLOW_STATE_ADDENDUM.md` §3).
All observations below are drawn only from the 4 successfully extracted files unless
stated otherwise.

## Question

Can semantic rap-writing guidance contained inside a parent recording influence a Suno
Remix when the user directly asks Suno to apply that guidance to create a new song?

This is a **working hypothesis only**. This document does not claim Suno is learning
permanently, training itself, reading a hidden system prompt, cumulatively improving
across remixes, or using any confirmed internal mechanism.

## Method

**Known parent (owner account):** the owner states they created a roughly four-minute
Suno track containing guidance, principles, tips, and examples about writing stronger
rap lyrics.

**Known instruction:** "Take all of these guidelines, tips, and tricks on how to write
good rap lyrics and use them to build a song. I think this song is going to be
incredible." Applied via Suno Remix to the parent track described above. **This is an
owner-recalled paraphrase, not a verified exact quotation** (see Prompt status).

**Initial output:** a song titled "Flow State Fundamentals."

**Branches present in the primary batch** (21 in-scope files; see register for
per-file evidence): Flow State Fundamentals (base, 2 renders), Playful Reggae Mix (2),
Reggaetón Fusion Experiment (4), Slow Burn Version (2); and a second family, Concrete
Flow Fundamentals, with Chill Studio Session (1), Clean Studio Mix (2), Isolated Studio
Version (2), Organic Roots Fusion (4), and Studio Pocket Remix (2).

**Evidence limitations:**
- No direct Suno parent/remix metadata link (an explicit "remixed from" field) was
  found in any extracted file's ID3 tags — only `TXXX:comment` carrying each render's
  *own* Suno song id and creation timestamp. Family relationships are inferred from
  filename/title text and batch co-upload, not a Suno-native lineage pointer.
- The original ~4-minute guidance parent track was not identified in either Drive
  folder; its Suno song id is unknown (open question, not assumed).
- The exact original remix instruction text could not be independently verified
  against a Suno-side source document.
- 17 of 21 in-scope files could not be downloaded due to a Google Drive connector
  issue (§ Known gaps). All observations below cover only the 4 that were.

## Observations

From `FLOW_STATE_FUNDAMENTALS_REGISTER.csv`, factual and metadata/DSP-derived only:

| Record | File | Duration | Suno created (UTC) | Tempo est. (BPM) | Percussive-energy ratio | Spectral centroid (Hz) |
|---|---|---|---|---|---|---|
| FSF-020 | Flow State Fundamentals.mp3 | 244.96s | 2026-08-06T23:46:24 | 100.4 | 0.208 | 4487.7 |
| FSF-021 | Flow State Fundamentals_1.mp3 | 267.20s | 2026-08-06T23:46:23 | 100.4 | 0.229 | 3701.9 |
| FSF-012 | Flow State Fundamentals Playful Reggae Mix.mp3 | 261.36s | 2026-08-07T00:00:31 | 97.0 | 0.260 | 4715.9 |
| FSF-013 | Flow State Fundamentals Playful Reggae Mix_1.mp3 | 270.68s | 2026-08-07T00:00:30 | 97.0 | 0.270 | 4413.4 |

- All 4 files carry distinct, verified `suno_song_id` values (no duplicates by hash or
  id) and no embedded artwork, lyrics, title, artist, or album ID3 frames — only a
  `TXXX:comment` timestamp/id field (see addendum §5).
- Both pairs above are classified `FLOW_STATE_SIBLING_PAIRS.csv` sibling pairs
  (matching normalized title, creation timestamps 1.0s apart — this ID3 field appears
  to carry only whole-second precision here, unlike PR #11's secondary-folder evidence,
  which had microsecond precision; confidence capped at `medium` accordingly, per the
  script's `<1.0s -> high` rule).
- Duration deltas within each sibling pair: Flow State Fundamentals base pair 8.3%
  (244.96s vs 267.20s), Playful Reggae Mix pair 3.5% (261.36s vs 270.68s). Both fall
  inside the 0–8.2% natural-variance range [[research/render-register/EXP-000-suno-seed-variance.md|EXP-000]]
  established for same-prompt Suno sibling generations — i.e., neither pair's duration
  spread is itself unusual for an unmodified-prompt regeneration, though EXP-000 did
  not cover Remix-with-guidance conditions specifically.
- No cross-folder match: none of the 4 files' `suno_song_id` values appear in PR #11's
  secondary-folder register — these are new renders, not re-uploads of prior catalog
  tracks (checked programmatically, not assumed).
- Automated DSP signal features (tempo estimate, percussive-energy ratio, spectral
  centroid) are the only quantitative production-style evidence available; they are
  objective waveform measurements, not genre or instrument classifications. No
  perceptual judgment (genre, guitar type, vocal delivery) was made for any of the 21
  in-scope files — see Known gaps.
- The register's `genre_family_by_title` field for all 4 files is drawn from filename
  text alone (2x "Flow State Fundamentals (base)", 2x "Playful Reggae Mix") — this
  plausibly reflects the Suno style prompt the owner used but is not independently
  confirmed by listening.

**n=4 is too small to draw any conclusion about the core research question.** These
observations describe what exists in this partial dataset; they do not test the
hypothesis.

## Working hypothesis

Semantic guidance in the parent recording may influence remix generation when combined
with a direct instruction to apply it.

## Alternative explanations

- The remix instruction alone (independent of any specific parent content) caused the
  thematic result — asking Suno to "write a song about writing better rap lyrics"
  would plausibly produce a similar self-referential/meta song regardless of what
  guidance, if any, was in the parent audio.
- Suno followed lyrical *patterns* present in the parent's audio/lyrics without
  "interpreting" them as instructions — surface-level continuation rather than
  semantic uptake.
- Suno continued the source track's subject matter (rap-writing-about-rap-writing) as
  a topic, which is a different claim than "applied the guidance as technique."
- Repeated generations (the full 21-file batch shows the same title generated multiple
  times — e.g. 4 differently-sized Reggaetón Fusion Experiment renders, 4 differently-
  sized Organic Roots Fusion renders) could produce some strong-sounding outputs
  stochastically, independent of any guidance-following mechanism — a selection effect
  if the owner is judging strength post hoc from many attempts.
- Later remixes (Concrete Flow Fundamentals, the reggae/reggaetón/studio variants) may
  have inherited traits from *prior renders in this same lineage* (e.g. Flow State
  Fundamentals itself, once it existed) rather than from the original lesson track —
  remix-of-a-remix drift, not guidance-from-the-original-lesson.
- Suno behavior may vary by model version, interface, voice vs. typed prompt, and
  Remix vs. Cover mode; none of that is controlled for or known here.
- No parent/child Suno-native link was recovered for any of these renders, so even the
  *existence* of a single traceable lineage chain from the guidance parent to these
  renders is itself unverified, not just the mechanism.

## Evidence status

Preliminary observational evidence, and materially incomplete (4 of 21 in-scope files).
Not yet controlled or independently reproduced.

## Prompt status

The remix instruction quoted in Method is an **owner-recalled paraphrase**, not a
verified exact quotation.

## Future controlled test plan (design only — not executed)

1. Same parent and same prompt, repeated N times — establish a variance baseline for
   this *specific* remix-with-guidance condition (parallel to
   [[research/render-register/EXP-000-suno-seed-variance.md|EXP-000]], which measured
   baseline variance for plain re-generation, not remix-with-guidance).
2. Same parent with a neutral prompt (no reference to "use these guidelines") —
   isolates whether the instruction alone drives the effect.
3. Same prompt applied to an unrelated parent (no rap-writing guidance content) —
   isolates whether the parent's specific content matters.
4. Guidance embedded in lyrics vs. guidance supplied directly in the prompt text.
5. Voice prompt vs. typed prompt for the same instruction.
6. Same lyrics carried forward vs. rewritten lyrics across remix generations.
7. Remix vs. Cover mode for the same parent+prompt.
8. Model-version comparison, if Suno exposes one at generation time.
9. Original (vocal) parent vs. an instrumental-only version of the same parent.
10. First-generation output vs. later-generation remixes, compared on the same
    lyrical/production dimensions this register can observe.

## Known gaps

- **17 of 21 in-scope files were not downloaded.** A Google Drive MCP connector fault
  specific to `download_file_content` (confirmed persistent across three separate
  retry attempts at different concurrency levels) blocked ingestion; a lightweight
  `get_file_metadata` call succeeded throughout, confirming the connector itself is
  reachable. Requires the owner to re-authorize the connector before retrying. See
  `OPEN_CORRECTIONS_FLOW_STATE_ADDENDUM.md` §3.
- The 14 out-of-scope files in the same primary folder (pre-existing catalog titles:
  Circle Stays Tight remix, Golden String Cypher, Real Madrid, Paco de Lucia Legend
  Cypher) were inventoried but not analyzed — see addendum §1.
- Perceptual audio judgments (genre, guitar type, vocal delivery, "reggae feel") were
  not made by listening — this workstream has no audio-listening/classification tool.
  Genre labels here are drawn from filename/title text and automated DSP signal
  features only, explicitly labeled as such per-record. Perceptual confirmation is
  deferred to the owner or a future session with listening capability.
- The original ~4-minute guidance parent track was not located in either Drive folder.
