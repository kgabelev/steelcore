# Steelcore Authorship and Provenance Log

> Complete this record while creating the artifact. Unknown legacy values must remain explicitly marked `unknown`, `unresolved`, `pending`, `not_applicable`, `null`, or empty evidence arrays as allowed by `schemas/provenance/artifact-provenance.schema.json`; do not infer or backfill them.

## Artifact Identity

- **schema_version:** `0.2`
- **artifact_id:**
- **artifact_version:**
- **title:**
- **artifact_type:** lyrics / composition / audio / image / video / persona / prompt / document / mixed
- **created_at:** ISO 8601 timestamp or `unknown`
- **classification:** unresolved / evidence / experiment / candidate / canon
- **Repository paths:**

## human_contributors

For each human contributor record:

- **name:** name or `unknown`
- **role:** role or `unknown`
- **contribution:** specific expressive contribution or known gap
- **evidence_status:** documented / self_attested / unknown
- **evidence_refs:** drafts / recordings / commits / session notes / files; may be empty for unknown legacy facts

## ai_systems

For each system record:

- **provider:** provider or `unknown`
- **product:** product or `unknown`
- **model_or_version:** model/version or `unknown`
- **plan:** account plan/tier or `unknown`
- **used_for:** lyrics / composition / vocals / instrumentals / arrangement / artwork / video / analysis / editing / other
- **usage_date:** ISO 8601 timestamp or `unknown`
- **prompt_or_session_refs:** prompt/session references; may be empty when unavailable
- **terms_snapshot_status:** captured / pending / unavailable / unknown
- **terms_snapshot_ref:** evidence reference or `null`

## source_inputs

For each source:

- **source_id:**
- **source_type:**
- **description:**
- **rights_status:** owned / licensed / public_domain / permission_pending / unresolved / unknown / not_applicable
- **source_ref:** evidence reference or `null`

## transformations

| timestamp | actor | input_version | action | output_version | evidence_refs |
|---|---|---|---|---|---|
| ISO 8601 or `unknown` | name or `unknown` | | | | |

## rights

- **human_authorship_status:** documented / partial / unknown / none_claimed
- **ai_generated_material:**
- **ownership_status:** cleared / partially_cleared / pending / rejected / unresolved / unknown / not_applicable
- **ownership_evidence_refs:** required when `ownership_status` is `cleared`
- **voice_likeness_status:** cleared / pending / rejected / unresolved / unknown / not_applicable
- **voice_likeness_evidence_refs:** required when `voice_likeness_status` is `cleared`
- **cultural_review_status:** cleared / pending / rejected / unresolved / unknown / not_applicable
- **cultural_review_evidence_refs:** required when `cultural_review_status` is `cleared`
- **limitations_or_exclusions:**

## disclosure

- **ai_involvement_summary:**
- **public_disclosure_status:** approved / pending / rejected / unresolved / unknown / not_applicable
- **platform_metadata_status:** prepared / submitted / pending / rejected / unresolved / unknown / not_applicable
- **disclosure_ref:** evidence reference or `null`

## approvals

Approved records require reviewer, timestamp, and evidence references. Pending, rejected, unknown, and not-applicable records may keep reviewer or timestamp unknown/null if that is accurate.

| approval_type | status | reviewer | timestamp | evidence_refs | notes |
|---|---|---|---|---|---|
| canon | pending | | | | |
| legal | pending | | | | |
| cultural | pending | | | | |
| release | pending | | | | |

## release_clearance

- **status:** cleared / pending / rejected / unresolved / unknown / not_applicable
- **reviewer:** required when `status` is `cleared`
- **timestamp:** required when `status` is `cleared`
- **evidence_refs:** required when `status` is `cleared`
- **notes:**

## release

- **status:** unreleased / scheduled / released / withdrawn / blocked
- **destinations:**
- **release_date:** ISO 8601 timestamp or `null`
- **release_refs:** submission identifiers, distributor records, takedown records, or other release evidence
