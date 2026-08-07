# Steelcore Roadmap

**Restructured 2026-08-07.** Previously a single chain, M0 through M6, in which every
milestone blocked the next. That structure made shipping a release depend on first
building the Steel agent runtime. Those two efforts are independent and are now
tracked separately.

**Provenance (D-007) and human approval (D-008) apply to both tracks without
exception.** This restructure removes a sequencing constraint, not a control.

---

## TRACK A - SHIP

**Goal:** Release 001 live on DSPs, correctly, with complete provenance evidence.

**Does not depend on Track B.** No agent runtime, memory system, or eval suite is
required to release a finished song.

### S1 - Catalog register closed

**Status:** In progress. **Owner: Kirill. This is the binding constraint.**

The creator-assessment and identity-analysis sections of the track records can only
be written by the owner. Everything downstream in this track waits on them.

**Exit criteria:**

- open items in `catalog/render-register/OPEN_CORRECTIONS.md` resolved or explicitly
  deferred with a reason;
- every registered track has creator assessment and identity analysis completed;
- known missing tracks added to the register;
- unknowns recorded as "unknown", never reconstructed.

### S2 - Release 001 selected and master identified

**Status:** Blocked by S1. **Owner selects; agent verifies.**

**Exit criteria:**

- one named track chosen, with the artistic rationale recorded;
- the master file identified by SHA-256, not by filename;
- the Drive divergence resolved. `Steelcore Audio Vault` and the Suno workspace export
  contain same-named files with different byte sizes. These are distinct renders. The
  canonical master must be identified by hash and the decision recorded.

### S3 - Rights and disclosure package

**Status:** Blocked by S2.

Compliance states are `EVIDENCE_PRESENT`, `EVIDENCE_MISSING`, `HUMAN_REVIEW_REQUIRED`,
`CLEARED_BY_AUTHORIZED_REVIEWER`, or `BLOCKED`. Never a generic PASS. A script can verify
that an authorship log exists; it cannot determine that a work is copyrightable.

**Exit criteria:**

- provenance record complete for the selected track and valid against
  `schemas/provenance/artifact-provenance.schema.json`;
- Suno subscription tier at generation time evidenced;
- human contribution documented specifically, not generically;
- disclosure wording drafted from `legal/disclosure-statement.md` and matched to actual
  evidence, never exceeding it;
- items requiring licensed counsel listed explicitly, not guessed at.

### S4 - Distribution and identity setup

**Status:** Not blocked. **Start now, in parallel with S1.**

Longest external lead times: handle availability, distributor review, account
verification. Sequencing this last would add weeks for no reason.

**Exit criteria:**

- distributor account created with AI-disclosure fields understood;
- artist name and handles secured;
- artwork prepared to distributor spec;
- credentials stored outside this repository, with MFA.

### S5 - Deliver and verify

**Status:** Blocked by S3 and S4.

**Exit criteria:**

- delivered with complete metadata and disclosure;
- live on target platforms;
- post-publication metadata check passes;
- release record committed with artifact provenance.

---

## TRACK B - BUILD

**Goal:** Steel as a persistent creative agent.

**Does not block Track A.** Work this when Track A is waiting on an external dependency
or on owner input.

### B1 - Artist canon

Persona, backstory, voice, visual identity, cultural grounding, derived from catalog
evidence rather than invented. Requires owner approval per D-008.

The cultural-grounding question around flamenco and gitano musical tradition is
deliberate work, not a formality.

**Public classification is fixed:** AI-native virtual recording artist, human-directed,
human-in-the-loop production. Not "autonomous artist." Human-in-the-loop is a permanent
governance principle, not a temporary developmental stage. Operational autonomy may
expand underneath it; authority over releases, rights, money, and identity does not.

### B2 - Memory and evaluation

**Blocked by B1.** Memory contracts, promotion rules, retrieval tests, eval suite.
Evaluation starts as pairwise preference plus rubric plus creator judgment. Machine
metrics are supplemental, not gating.

### B3 - Creative session runtime

**Blocked by B2.** The vertical slice in `PROJECT_CONTEXT.md`.

### B4 - Buzz / ACP integration

**Blocked by B3.**

### B5 - Production hardening

**Blocked by B4.**

---

## Completed

**M0 - AI Resource Control Plane.** Complete. Model routing, budgets, quota evidence,
build history, automated validation on `main`.

**M1 - Canonical Project Foundation.** Complete. Context, decisions, roadmap, agent
contract, handoff template, execution ledger merged.

**M2 - Canonical Source Import and Provenance.** Requires verification.
`EXECUTION_LEDGER.yaml` marks the three M2 workstreams `rework_required`, but their owned
paths contain content on `main` and the repository reports zero open pull requests.
Actual merge state must be confirmed against git history before this is marked complete.

---

## Critical path

```
S1 (Kirill) -> S2 -> S3 -> S5
         S4 (parallel, start now) --^
```

Track B runs alongside and gates nothing in Track A.
