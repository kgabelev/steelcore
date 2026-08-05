# Steelcore AI Disclosure Statement — Draft Template

**Status:** Draft framework only. Do not publish without matching artifact-level provenance, `disclosure.public_disclosure_status: "approved"`, and explicit `release_clearance` review when the statement is release-facing.

## Label-level statement

Steelcore develops fictional digital artists through a human-led creative process that may use generative AI in composition, production, vocals, visuals, analysis, or editing. Human contributors define the artist direction, make creative selections and revisions, approve canonical identity and releases, and document the tools used for each published work.

## Release-specific statement

> **Release:** `[TITLE]`  
> **Human contribution:** `[SPECIFIC HUMAN-WRITTEN, PERFORMED, ARRANGED, EDITED, OR DIRECTED ELEMENTS]`  
> **AI-assisted elements:** `[VOCALS / INSTRUMENTAL / COMPOSITION / ARTWORK / VIDEO / OTHER]`  
> **Tools used:** `[PROVIDER, PRODUCT, MODEL OR VERSION]`  
> **Canon approval reviewer:** `[HUMAN OWNER/REVIEWER OR UNKNOWN]`
> **release_clearance.status:** `[CLEARED / PENDING / REJECTED / UNRESOLVED / UNKNOWN / NOT_APPLICABLE]`

This work is presented as an AI-assisted creative production. It does not represent or imitate a real person unless that involvement and permission are explicitly disclosed.

## Rules for use

- Describe actual contribution; do not use vague language to conceal fully generated components.
- Do not claim that a human wrote, performed, or composed an element unless the provenance record supports it.
- Do not claim full ownership or copyright protection when known exclusions or unresolved rights exist.
- Align public wording with `disclosure.public_disclosure_status` and `disclosure.platform_metadata_status` in the provenance record.
- Do not imply canon approval; canon approval is recorded separately in `approvals` with `approval_type: "canon"`.
- Do not imply release clearance unless `release_clearance.status` is `cleared` with reviewer, timestamp, and evidence.
- Revalidate platform-specific disclosure requirements before every submission.
- Preserve the approved wording and submission evidence with the release record.

## Approval fields

- **Artifact provenance record:**
- **Policy verification date:**
- **disclosure.public_disclosure_status:** approved / pending / rejected / unresolved / unknown / not_applicable
- **disclosure.platform_metadata_status:** prepared / submitted / pending / rejected / unresolved / unknown / not_applicable
- **Legal approval:** approved / pending / rejected / unknown / not_applicable
- **Owner approval:** approved / pending / rejected / unknown / not_applicable
- **release_clearance.status:** cleared / pending / rejected / unresolved / unknown / not_applicable
- **Approved public wording version:**
