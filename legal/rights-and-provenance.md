# Rights and Provenance Controls

## Purpose

Steelcore records how every creative artifact was made so that canon, release, distribution, licensing, and disclosure decisions are based on evidence rather than memory.

This document defines operational controls, not legal advice or a final legal conclusion.

## Required record

Every lyrics, audio, image, video, persona, prompt, or mixed artifact must have a provenance record conforming to:

`schemas/provenance/artifact-provenance.schema.json`

Unknown values must remain explicit. An artifact may be retained as an experiment with unresolved provenance, but it may not be promoted to release-ready status.

## Provenance minimums

1. Stable artifact ID and version.
2. Human contributors and their specific expressive contributions.
3. AI provider, product, model/version, plan, date, purpose, and session references.
4. Source inputs and their ownership or license status.
5. Material transformation history.
6. Human-authorship and AI-generated-material assessment.
7. Voice/likeness and cultural-grounding review state.
8. Public and platform disclosure state.
9. Canon, legal, cultural, and release approvals.
10. Release destinations and identifiers.

## Classification gates

### Experiment

May have incomplete provenance. Cannot be treated as Steel canon or released commercially.

### Candidate

Must identify source inputs, known creators, AI systems, and unresolved gaps. Eligible for evaluation but not release.

### Canon

Requires human approval and sufficient provenance to explain why the artifact represents Steel. Canon status does not imply release clearance.

### Release-ready

Requires:

- rights status `cleared` or a specifically approved limitation;
- human contribution documented;
- generation-platform terms and plan evidence captured;
- voice/likeness review cleared;
- cultural review cleared when applicable;
- current distributor and platform requirements verified;
- disclosure text and metadata approved;
- explicit release approval.

## Evidence preservation

Preserve originals without silent rewriting. Derived Markdown, transcripts, edits, and optimized media must reference the original file or approved object-storage record. Checksums should be added when binary import is implemented.

## No unsupported warranties

Steelcore must not state or imply full ownership, copyrightability, originality, platform eligibility, or clean rights unless the evidence record supports that exact claim and required review has occurred.
