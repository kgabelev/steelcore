# Steelcore Decisions

## D-001 - GitHub is canonical

**Status:** Approved  
**Date:** 2026-08-04

The private GitHub repository is the permanent source of truth. Buzz, Claude, ChatGPT, Gemini, Perplexity, Grok, Suno, and local machines are execution or research surfaces.

## D-002 - Control plane before agent fan-out

**Status:** Approved, scope clarified 2026-08-07  
**Date:** 2026-08-05

Every major build uses the model registry, budget policy, usage snapshot, routing policy, build history, and automated validation before parallel agents are launched.

**Scope clarification (D-011):** This governs concurrent multi-agent builds. It does not gate single-operator work or a single agent session.

## D-003 - Isolated ownership

**Status:** Approved, scope clarified 2026-08-07  
**Date:** 2026-08-05

Every implementation agent receives one branch or worktree, explicit file ownership, acceptance tests, budget limits, and stop conditions. Two implementation agents may not edit the same files concurrently.

**Scope clarification (D-011):** Applies when two or more implementation agents run concurrently. When one operator or one agent is working, normal branch-and-review is sufficient.

## D-004 - Steel's musical identity is protected

**Status:** Approved  
**Date:** 2026-08-04

Steel remains rooted in underground trap-flamenco: aggressive modern trap, percussive nylon-string guitar, deep 808s, hard drums, sharp wordplay, and a plosive-heavy rap flow. Later optimization may improve commercial strength but may not flatten or replace this identity.

## D-005 - Dual creative perspectives

**Status:** Approved  
**Date:** 2026-08-04

Steel's creative engine preserves both:

- an experimental art-critic perspective that challenges generic or safe work;
- a mainstream hustler/hitmaker perspective that pushes hooks, clarity, replay value, and audience impact.

The final workflow compares and synthesizes both perspectives.

## D-006 - First vertical slice

**Status:** Approved, superseded in part by D-010 on 2026-08-07  
**Date:** 2026-08-05  
**Approved by:** Kirill Gabelev

The first end-to-end product is the **Steel Creative Session** described in `PROJECT_CONTEXT.md`. No autonomous social, release, or large-scale fan system is built before this slice passes acceptance tests.

**Superseded in part.** The Steel Creative Session remains the first vertical slice of the Build track. It is no longer a precondition for a human-directed commercial release. The original wording made shipping any music depend on first completing an agent runtime; that dependency was unintended and is removed by D-010. The restriction on **autonomous** social, release, and fan systems stands unchanged.

## D-007 - Provenance from the first artifact

**Status:** Approved  
**Date:** 2026-08-05

Every canonical creative artifact records its human contribution, AI tools used, source inputs, generation date, edits, approval status, and release status. Legal and disclosure records are built into the workflow rather than added later.

## D-008 - Human approval boundaries

**Status:** Approved  
**Date:** 2026-08-05

Human approval is always required for persona canon, legal posture, external publication, commercial release, spending, destructive actions, secret access expansion, and production deployment.

## D-009 - Isolated-path precedent for path-ownership conflicts

**Status:** Approved, scope clarified 2026-08-07  
**Date:** 2026-08-06  
**Approved by:** Kirill Gabelev

When a new task's requested output paths overlap an active, unmerged workstream's `owned_paths` in `EXECUTION_LEDGER.yaml` (triggering the `branch_conflict_or_scope_overlap_detected` stop condition in `system/control-plane/budget-policy.yaml`), the agent must stop and surface the conflict rather than write into the contested path. If the owner then chooses to proceed rather than wait, the agent writes to new, clearly isolated subdirectories instead (e.g. `catalog/render-register/` instead of `catalog/`) and records the deferred reconciliation explicitly - never silently into the contested path. First applied to the `render-register-v1` workstream, whose requested paths (`catalog/`, `research/`, `tests/`) overlapped `creative-catalog-import` and `research-import`.

**Scope clarification (D-011):** This is a conflict-resolution procedure for concurrent agents, not a general writing rule. It should not be invoked when no other workstream is actively unmerged.

## D-010 - Ship track and build track are independent

**Status:** Approved  
**Date:** 2026-08-07  
**Approved by:** Kirill Gabelev

Releasing music and building the Steel agent system are independent efforts and are tracked separately in `ROADMAP.md` as Track A (Ship) and Track B (Build).

A commercial release requires artistic approval, a verified master, a complete provenance and disclosure package, and distribution readiness. It does not require the memory architecture, the evaluation suite, or the creative-session runtime.

**What this does not change:** D-007 (provenance from the first artifact) and D-008 (human approval boundaries) apply in full to every release. Nothing here reduces the evidence or approval requirements. It removes a sequencing constraint only.

**Rationale:** finished catalog material exists. Gating its release on an unbuilt agent runtime delays revenue, real-world platform feedback, and the operational learning that would inform the Build track anyway.

## D-011 - Governance is scoped to concurrency, not ceremony

**Status:** Approved  
**Date:** 2026-08-07  
**Approved by:** Kirill Gabelev

D-002, D-003, and D-009 were written to coordinate multiple concurrent implementation agents. They apply when that condition holds. They are dormant when a single operator or a single agent is working, and invoking them in that case adds process cost without reducing risk.

This clarification does not repeal them. When parallel agents are launched again, they apply in full.

**What remains unconditional regardless of concurrency:** provenance records (D-007), human approval boundaries (D-008), no secrets in the repository, and no publication, spending, or destructive action without explicit approval.

## D-012 - Graded compliance states, never a generic PASS

**Status:** Approved  
**Date:** 2026-08-07  
**Approved by:** Kirill Gabelev

Compliance and rights controls record one of: `EVIDENCE_PRESENT`, `EVIDENCE_MISSING`, `HUMAN_REVIEW_REQUIRED`, `CLEARED_BY_AUTHORIZED_REVIEWER`, `BLOCKED`.

A system may verify that evidence exists - that an authorship log is present, that a subscription tier is recorded, that disclosure fields are populated. A system may not determine that a work is copyrightable, legally cleared, trademark-safe, or free of right-of-publicity exposure. Those are human determinations and are recorded as reviewer, determination, evidence, and date.

## D-013 - Public classification of Steel

**Status:** Approved  
**Date:** 2026-08-07  
**Approved by:** Kirill Gabelev

Steel is publicly described as an AI-native virtual recording artist, human-directed, with human-in-the-loop production. The terms "autonomous artist" and "fully self-running artist" are not used publicly.

Human-in-the-loop is a permanent governance principle, not a temporary developmental stage. Operational autonomy may expand substantially underneath it. Authority over releases, rights assertions, legal determinations, contracts, financial commitments, and canon identity changes does not transfer to the system.

This wording also supports the human-authorship position that the copyright and PRO registration strategy depends on. Describing Steel as autonomous would argue against the human control that position requires.
