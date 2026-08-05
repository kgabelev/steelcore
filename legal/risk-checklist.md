# Steelcore Risk Checklist

Use this checklist before promoting an artifact to canon and again before any public or commercial release.

## Provenance

- [ ] Original source files are preserved or referenced in approved storage.
- [ ] Human contributors and their specific contributions are documented.
- [ ] AI systems, model/version, plan, usage date, and session references are documented.
- [ ] Source inputs and rights status are documented.
- [ ] Material edits and transformations are traceable by version.
- [ ] Unknowns remain explicit as schema-valid `unknown`, `unresolved`, `pending`, `not_applicable`, `null`, or empty evidence arrays and have an owner for resolution when resolution is required.

## Rights and authorship

- [ ] Human-authored expression is identified separately from AI-generated material.
- [ ] No unsupported claim of full copyright or ownership appears in metadata or contracts.
- [ ] Generation-platform terms applicable on the generation date are captured.
- [ ] Required limitations, exclusions, or disclaimers are identified.
- [ ] Third-party samples, lyrics, images, recordings, fonts, or datasets are cleared.

## Voice, likeness, and identity

- [ ] Voice and visual outputs have been screened for resemblance to identifiable real people.
- [ ] No unauthorized impersonation or false endorsement is implied.
- [ ] Any reference material involving a real person has documented permission or a defensible basis.
- [ ] Artist naming and branding have received trademark-conflict review before launch.

## Cultural and reputational risk

- [ ] Persona ethnicity, nationality, language, and cultural claims are accurately grounded.
- [ ] Human creative ownership and standing are documented for sensitive identity claims.
- [ ] Stereotypes, slurs, caricature, and exploitative imagery have been reviewed.
- [ ] A separate cultural reviewer has approved high-risk persona or release elements.

## Platform and disclosure

- [ ] Distributor and platform policies were verified from official sources close to submission.
- [ ] AI involvement is recorded by component: lyrics, composition, vocals, instrumental, artwork, and video.
- [ ] Public disclosure language matches the provenance record.
- [ ] Required platform metadata is prepared and reviewed.
- [ ] Catalog structure, artist profile, and streams do not resemble spam or manipulation.

## Operational security

- [ ] No secrets, credentials, private personal information, or hidden tokens are committed.
- [ ] External tools have minimum necessary permissions.
- [ ] Destructive actions, spending, publication, and deployment have explicit approval.
- [ ] Release artifacts, metadata, and approvals are backed up and reproducible.

## Canon gate

Canon promotion requires `classification: "canon"` and a matching `approvals` record with `approval_type: "canon"`, `status: "approved"`, reviewer, timestamp, and evidence. Canon approval does not imply legal, commercial-release, platform, or disclosure clearance.

## Release clearance gate

`release_clearance.status: "cleared"` is blocked if any required item is unchecked, marked `unknown`, `unresolved`, `pending`, or contradicted by the provenance record. Clearance requires resolved material rights, required voice/likeness and cultural review states, release approval evidence, and explicit owner or professional review where required. A blocked or unresolved `release_clearance` may coexist with `release.status: "unreleased"` or `release.status: "blocked"`.
