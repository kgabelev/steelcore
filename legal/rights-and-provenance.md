# Rights and Provenance Controls

## Purpose

Steelcore records how every creative artifact was made so that canon, release, distribution, licensing, and disclosure decisions are based on evidence rather than memory.

This document defines operational controls, not legal advice or a final legal conclusion.

## Required record

Every lyrics, audio, image, video, persona, prompt, document, or mixed artifact must have a provenance record conforming to:

`schemas/provenance/artifact-provenance.schema.json`

Records use `schema_version: "0.2"`. Later 0.x schema changes may add optional fields or additional explicit unknown states, but importers must write the exact schema version they validate against. Unknown values must remain explicit as `unknown`, `unresolved`, `pending`, `not_applicable`, `null`, or an empty evidence array as the schema permits. Do not infer or backfill legacy facts.

## State model

Keep these fields separate:

1. `classification`: artifact classification only: `unresolved`, `evidence`, `experiment`, `candidate`, or `canon`.
2. `rights`: provenance completeness and rights assessment, including `ownership_status`, `voice_likeness_status`, `cultural_review_status`, and evidence reference arrays.
3. `approvals`: human approval records for canon, legal, cultural, release, publication, production, owner, or professional review.
4. `release_clearance`: release clearance gate. `cleared` requires reviewer, timestamp, evidence, resolved material rights, and release approval.
5. `release`: actual release status: `unreleased`, `scheduled`, `released`, `withdrawn`, or `blocked`.

Canon approval does not imply legal, rights, platform, disclosure, or commercial-release clearance. Release clearance does not change artifact classification.

## Provenance minimums

1. Stable `artifact_id` and `artifact_version`.
2. `human_contributors` and their specific expressive contributions, or explicit unknowns for incomplete legacy imports.
3. `ai_systems` including provider, product, `model_or_version`, plan, date, purpose, and session references, or explicit unknowns where legacy facts are unavailable.
4. `source_inputs` and their ownership, license, unresolved, not-applicable, or unknown rights status.
5. Traceable `transformations` by version, preserving originals without silent rewriting.
6. `rights.human_authorship_status` and `rights.ai_generated_material` assessment.
7. `rights.voice_likeness_status` and `rights.cultural_review_status` review states.
8. `disclosure.public_disclosure_status` and `disclosure.platform_metadata_status`.
9. Human `approvals` for required canon, legal, cultural, and release decisions.
10. `release_clearance` and `release` destinations, dates, and identifiers.

## Classification gates

### `experiment`

May have incomplete provenance. It can validate with explicit unknowns, but it cannot be treated as Steel canon or release-cleared.

### `candidate`

Must identify known source inputs, known creators, AI systems, and unresolved gaps. Eligible for evaluation but not release-cleared until all release gates pass.

### `canon`

Requires an `approvals` record where `approval_type` is `canon` and `status` is `approved`, with reviewer, timestamp, and evidence. Canon status means the artifact represents Steel; it is not a legal conclusion and does not imply `release_clearance.status: "cleared"`.

## Release clearance gate

`release_clearance.status: "cleared"` requires:

- `rights.ownership_status: "cleared"` with `rights.ownership_evidence_refs`;
- `rights.voice_likeness_status` of `cleared` or `not_applicable`, with evidence when `cleared`;
- `rights.cultural_review_status` of `cleared` or `not_applicable`, with evidence when `cleared`;
- generation-platform terms and plan evidence in the provenance record where material AI output is used;
- disclosure text and platform metadata reviewed when required;
- an `approvals` record where `approval_type` is `release` and `status` is `approved`, with reviewer, timestamp, and evidence;
- `release_clearance.reviewer`, `release_clearance.timestamp`, and non-empty `release_clearance.evidence_refs`.

`pending`, `rejected`, `unresolved`, `unknown`, and `not_applicable` remain valid clearance states and must not be presented as cleared.

## Evidence preservation

Preserve originals without silent rewriting. Derived Markdown, transcripts, edits, and optimized media must reference the original file or approved object-storage record. Checksums should be added when binary import is implemented.

## No unsupported warranties

Steelcore must not state or imply full ownership, copyrightability, originality, platform eligibility, clean rights, canon status, or release clearance unless the evidence record supports that exact claim and required review has occurred.
