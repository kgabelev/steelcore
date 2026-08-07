# Steelcore Decisions

## D-001 — GitHub is canonical

**Status:** Approved  
**Date:** 2026-08-04

The private GitHub repository is the permanent source of truth. Buzz, Claude, ChatGPT, Gemini, Perplexity, Grok, Suno, and local machines are execution or research surfaces.

## D-002 — Control plane before agent fan-out

**Status:** Approved  
**Date:** 2026-08-05

Every major build uses the model registry, budget policy, usage snapshot, routing policy, build history, and automated validation before parallel agents are launched.

## D-003 — Isolated ownership

**Status:** Approved  
**Date:** 2026-08-05

Every implementation agent receives one branch or worktree, explicit file ownership, acceptance tests, budget limits, and stop conditions. Two implementation agents may not edit the same files concurrently.

## D-004 — Steel's musical identity is protected

**Status:** Approved  
**Date:** 2026-08-04

Steel remains rooted in underground trap-flamenco: aggressive modern trap, percussive nylon-string guitar, deep 808s, hard drums, sharp wordplay, and a plosive-heavy rap flow. Later optimization may improve commercial strength but may not flatten or replace this identity.

## D-005 — Dual creative perspectives

**Status:** Approved  
**Date:** 2026-08-04

Steel's creative engine preserves both:

- an experimental art-critic perspective that challenges generic or safe work;
- a mainstream hustler/hitmaker perspective that pushes hooks, clarity, replay value, and audience impact.

The final workflow compares and synthesizes both perspectives.

## D-006 — First vertical slice

**Status:** Approved  
**Date:** 2026-08-05  
**Approved by:** Kirill Gabelev

The first end-to-end product is the **Steel Creative Session** described in `PROJECT_CONTEXT.md`. No autonomous social, release, or large-scale fan system is built before this slice passes acceptance tests.

## D-007 — Provenance from the first artifact

**Status:** Approved  
**Date:** 2026-08-05

Every canonical creative artifact records its human contribution, AI tools used, source inputs, generation date, edits, approval status, and release status. Legal and disclosure records are built into the workflow rather than added later.

## D-008 — Human approval boundaries

**Status:** Approved  
**Date:** 2026-08-05

Human approval is always required for persona canon, legal posture, external publication, commercial release, spending, destructive actions, secret access expansion, and production deployment.

## D-009 — Isolated-path precedent for path-ownership conflicts

**Status:** Approved  
**Date:** 2026-08-06  
**Approved by:** Kirill Gabelev

When a new task's requested output paths overlap an active, unmerged workstream's `owned_paths` in `EXECUTION_LEDGER.yaml` (triggering the `branch_conflict_or_scope_overlap_detected` stop condition in `system/control-plane/budget-policy.yaml`), the agent must stop and surface the conflict rather than write into the contested path. If the owner then chooses to proceed rather than wait, the agent writes to new, clearly isolated subdirectories instead (e.g. `catalog/render-register/` instead of `catalog/`) and records the deferred reconciliation explicitly — never silently into the contested path. First applied to the `render-register-v1` workstream, whose requested paths (`catalog/`, `research/`, `tests/`) overlapped `creative-catalog-import` and `research-import`.
