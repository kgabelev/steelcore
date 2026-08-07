# EXP-001 — Flow State Fundamentals: Embedded Lyrical Guidance Remix Experiment

**Status:** preliminary observational, not controlled, not reproduced.
**Dataset:** `catalog/render-register/FLOW_STATE_FUNDAMENTALS_REGISTER.csv`, built by
`scripts/render-register/build_flow_state_register.py` from the Drive folder
`https://drive.google.com/drive/folders/1r1m6CS7wiZ78mEtvGrQ4R-x5wbw8pZlF`
("My Workspace Unzipped Files", inside `2026-08-06_FLOW_STATE_FUNDAMENTALS_RAW_BATCH`),
cross-referenced against the existing secondary-folder register
(`catalog/render-register/RENDER_REGISTER.csv`, from PR #11) for lineage only — the
secondary folder was **not** re-ingested.
**Sample size:** 21 of 21 in-scope files fully extracted (hash, ID3, DSP signal
features). The Drive MCP connector's `download_file_content` tool proved persistently
unreliable (session-expired errors even after the owner reauthorized the connector,
confirmed not concurrency-related); the remaining 17 files (beyond the first 4) were
instead fetched via `gdown` against the shared folder link, a non-MCP path, with every
file's local size verified byte-for-byte against the Drive listing before extraction.
See `OPEN_CORRECTIONS_FLOW_STATE_ADDENDUM.md` §3 for the full account.

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

From `FLOW_STATE_FUNDAMENTALS_REGISTER.csv` (all 21 of 21 in-scope files), factual and
metadata/DSP-derived only:

- **21 distinct renders, 21 distinct SHA-256 hashes, 21 distinct `suno_song_id` values.**
  Zero exact (byte-identical) duplicates in this batch.
- **20 of the 21 files resolve into 10 sibling pairs**; `Concrete Flow Fundamentals
  Chill Studio Session.mp3` is the only unpaired render (no second Drive file with a
  matching title in this batch). Every other family/variant in the batch — both
  branches, all 9 named variants — appears exactly twice with matching normalized
  titles and Suno creation timestamps 0.0–2.0s apart:

  | Pair | Variant | Duration Δ | Tempo est. (BPM) |
  |---|---|---|---|
  | FSF-SIB-001 | Clean Studio Mix | 2.5% | 93.8 / 93.8 |
  | FSF-SIB-002 | Isolated Studio Version | 0.7% | 92.2 / 92.2 |
  | FSF-SIB-003 | Organic Roots Fusion (a) | 1.5% | 187.5* / 93.8 |
  | FSF-SIB-004 | Organic Roots Fusion (b) | 0.9% | 187.5* / 187.5* |
  | FSF-SIB-005 | Studio Pocket Remix | 2.5% | 93.8 / 92.2 |
  | FSF-SIB-006 | Playful Reggae Mix | 3.4% | 97.0 / 97.0 |
  | FSF-SIB-007 | Reggaetón Fusion Experiment (a) | 1.6% | 95.3 / 95.3 |
  | FSF-SIB-008 | Reggaetón Fusion Experiment (b) | 0.6% | 95.3 / 95.3 |
  | FSF-SIB-009 | Slow Burn Version | 3.8% | 97.0 / 98.7 |
  | FSF-SIB-010 | Flow State Fundamentals (base) | 8.3% | 100.4 / 100.4 |

  *187.5 BPM is very likely a beat-tracking octave error (exactly 2× its sibling's
  93.8) rather than a genuine tempo difference — a known limitation of automated
  tempo estimators on syncopated/trap-adjacent percussion, not a claim that this
  render is actually twice as fast.
- **All 10 duration deltas fall in the 0.6%–8.3% range**, closely matching the
  0–8.2% natural sibling-pair variance baseline established in
  [[research/render-register/EXP-000-suno-seed-variance.md|EXP-000]] (measured from
  8 plain-regeneration pairs in the secondary-folder catalog, max 8.2%, mean 4.6%).
  **This is a genuine cross-check, not just a coincidence of scale**: this batch's
  variance, generated under a Remix-with-guidance condition, is statistically
  indistinguishable in magnitude from EXP-000's plain-regeneration baseline. That is
  evidence about *generation-seed variance*, not about the core research question —
  it does not confirm or rule out guidance uptake, only that whatever Suno is doing
  here does not obviously destabilize duration/structure beyond its normal variance.
- No embedded artwork in any of the 21 files (`apic_count == 0` throughout). No
  embedded lyrics, title, artist, or album ID3 frames in any file — only a
  `TXXX:comment` id/timestamp field (and, for 2 of the 21, a `TXXX:sga` frame).
- No cross-folder match: none of the 21 files' `suno_song_id` values appear in PR #11's
  secondary-folder register — these are new renders, not re-uploads of prior catalog
  tracks (checked programmatically, not assumed).
- Automated DSP signal features (tempo estimate, percussive-energy ratio, spectral
  centroid) are the only quantitative production-style evidence available; they are
  objective waveform measurements, not genre or instrument classifications. No
  perceptual judgment (genre, guitar type, vocal delivery) was made for any of the 21
  in-scope files — see Known gaps.
- The register's `genre_family_by_title` field is drawn from filename text alone —
  this plausibly reflects the Suno style prompt the owner used per variant, but is not
  independently confirmed by listening.

**This dataset describes what Suno produced across two remix branches of one
lyric-guidance experiment; it does not test the core causal hypothesis.** Nothing here
establishes *why* these renders came out the way they did — only what they measurably
are (durations, tempo estimates, hashes, sibling structure). See Alternative
explanations below for why a stronger claim is not warranted.

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
- Repeated generations could produce some strong-sounding outputs stochastically,
  independent of any guidance-following mechanism — a selection effect if the owner is
  judging strength post hoc from many attempts. This batch confirms the mechanism for
  such an effect exists here: **every one of the 9 named variants was generated twice**
  (10 sibling pairs total, matching Suno's standard two-renders-per-call pattern
  already documented in EXP-000), so any single "unusually strong" render the owner
  points to had, at minimum, one sibling generated from the identical prompt to compare
  against — and this register does not yet know whether the owner's strong impression
  was formed from one render, both, or a comparison between them.
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

Preliminary observational evidence. Ingestion is complete (21 of 21 in-scope files
hashed, tagged, and DSP-analyzed), but this remains a single, uncontrolled batch — not
yet controlled or independently reproduced.

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

- The 14 out-of-scope files in the same primary folder (pre-existing catalog titles:
  Circle Stays Tight remix, Golden String Cypher, Real Madrid, Paco de Lucia Legend
  Cypher) were inventoried but not analyzed — see addendum §1.
- Perceptual audio judgments (genre, guitar type, vocal delivery, "reggae feel") were
  not made by listening — this workstream has no audio-listening/classification tool.
  Genre labels here are drawn from filename/title text and automated DSP signal
  features only, explicitly labeled as such per-record. Perceptual confirmation is
  deferred to the owner or a future session with listening capability.
- The original ~4-minute guidance parent track was not located in either Drive folder.
- The Google Drive MCP connector's `download_file_content` tool proved unreliable
  throughout this workstream (session-expired errors, not resolved by the owner's
  reauthorization) — 17 of 21 files were ultimately fetched via `gdown` instead. This
  doesn't affect the data quality (every file's size was verified against the Drive
  listing before extraction) but is a tooling limitation worth flagging for future
  ingestion work. See `OPEN_CORRECTIONS_FLOW_STATE_ADDENDUM.md` §3.
