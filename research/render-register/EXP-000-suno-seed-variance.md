# EXP-000 — Suno Seed-Variance Baseline (from sibling-pair renders)

**Status:** baseline measurement, not an experiment with a manipulated variable.
**Dataset:** `catalog/render-register/SIBLING_PAIRS.csv` and
`catalog/render-register/RENDER_REGISTER.csv`, built by
`scripts/render-register/build_render_register.py` from the Steel MP3 source
folder (`https://drive.google.com/drive/folders/1whcWEFpgkipHvWMRQe9QYtya3lJt2fCg`).
**Sample size:** 8 sibling pairs (16 renders) out of 34 renders registered.

## Purpose

Suno commonly returns two audio renders per generation call from what is,
as far as this repository can observe, the *same prompt and settings*. Before
any claim can be made that a prompt change, style-tag change, or model
version change caused a musical difference between two renders, there needs
to be a baseline for how much two renders already differ when *nothing about
the input changed* — i.e., variance from Suno's own generation seed. This
document is that baseline. It exists so that future experiments in this
research track have something to compare their effect sizes against, per
[[DECISIONS.md#D-007]]-style evidence discipline.

## How the sibling pairs were identified

A pair of renders was classified as a "sibling pair" only if, per
`scripts/render-register/build_render_register.py`:

1. their titles matched after normalization (case-insensitive, whitespace
   collapsed, one trailing parenthetical/index suffix stripped), **and**
2. their ID3-embedded Suno creation timestamps (`created=...` field, sourced
   from the `COMM` frame, which carries microsecond precision) were within
   2.0 seconds of each other.

This is an **inference**, not a fact. Suno does not expose an explicit
sibling/variation/generation-batch ID in the ID3 metadata this register
read. It is possible — though considered unlikely given how tightly
clustered the actual deltas turned out to be (see below) — that a pair
matched by coincidence rather than shared origin.

## Measured facts

For all 8 pairs, both renders carry **different Suno song IDs** and
**different SHA-256 hashes** — they are genuinely distinct audio renders,
not duplicate files.

**Creation-timestamp deltas** (both renders' `COMM` timestamp, in
microseconds):

| Pair | Title | Δt (µs) |
|---|---|---|
| SIB-001 | Gypsy Strings With The Trap | 83 |
| SIB-002 | Mi Barrio | 76 |
| SIB-003 | Barcelona Nights | 81 |
| SIB-004 | Fusion rap | 81 |
| SIB-005 | I Keep My Circle Tight | 86 |
| SIB-006 | Circle Stays Tight | 82 |
| SIB-007 | Circle Stays Tight (All The Way Up Remix) | 81 |
| SIB-008 | Golden string cypher | 82 |

Range: 76–86 µs. Mean: ~82 µs. This tight, consistent clustering (all 8
pairs within a 10 µs band) is itself a measured fact and is the strongest
evidence that these pairs come from a single generation call issuing two
renders in parallel, rather than from two independent, coincidentally
similarly-titled generations.

**Duration deltas** (`ffprobe`-measured `duration_seconds`, from
`RENDER_REGISTER.csv`):

| Pair | Title | Render A | Render B | Δ duration | Δ % of longer |
|---|---|---|---|---|---|
| SIB-001 | Gypsy Strings With The Trap | 245.40s | 226.44s | 18.96s | 7.7% |
| SIB-002 | Mi Barrio | 192.16s | 195.84s | 3.68s | 1.9% |
| SIB-003 | Barcelona Nights | 158.20s | 148.68s | 9.52s | 6.0% |
| SIB-004 | Fusion rap | 151.40s | 141.80s | 9.60s | 6.3% |
| SIB-005 | I Keep My Circle Tight | 189.40s | 185.92s | 3.48s | 1.8% |
| SIB-006 | Circle Stays Tight | 194.48s | 185.40s | 9.08s | 4.7% |
| SIB-007 | Circle Stays Tight (All The Way Up Remix) | 191.92s | 192.92s | 1.00s | 0.5% |
| SIB-008 | Golden string cypher | 229.40s | 249.80s | 20.40s | 8.2% |

Across the 8 pairs: **min duration delta 0.5%, max 8.2%, mean 4.6%, median
5.35%** (of the longer render's duration).

File size and bitrate also differ within every pair (see
`RENDER_REGISTER.csv`); this tracks duration and encoding variance rather
than being an independent signal, so it is not tabulated separately here.

## What this baseline does and does not license

**Licensed:** treating an observed duration/structural difference between
two renders of *the same unmodified prompt* as unremarkable if it falls
within roughly 0–8% duration variance. Nothing in this dataset measures
lyrical, melodic, or stylistic variance directly — only the two dimensions
this register's ID3/ffprobe extraction can observe (duration and encoding).

**Not licensed:** any claim that a specific prompt edit, style-tag change,
or model-version change "caused" a musical or structural difference,
*unless* that difference exceeds what this baseline shows can happen with
no input change at all. With n=8 pairs, this baseline is also too small to
support strong statistical claims about the *distribution* of natural
variance — it establishes an order-of-magnitude reference range, not a
validated confidence interval.

**Not measured here at all:** lyrical variance, melodic/harmonic variance,
vocal-take variance, or mix/master variance between sibling renders. A
future experiment that wants to claim a prompt effect on any of those
dimensions needs its own baseline for that dimension — this document only
covers what ID3 tags and `ffprobe` can observe.

## Known gaps

- Two files in the source folder failed to download (see
  `catalog/render-register/OPEN_CORRECTIONS.md` §2) and could not be
  evaluated for sibling-pair membership. If they turn out to be siblings of
  an already-registered render, n grows to 9.
- This baseline draws entirely from the Steel catalog's own Suno usage
  (one account, `kgabelev`, Suno v5.5 per the one available style-page
  export). It is not a general claim about Suno's variance behavior across
  accounts, model versions, or generation settings.
