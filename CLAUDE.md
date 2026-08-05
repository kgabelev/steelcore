# Steelcore Agent Operating Contract

This file applies to Claude Code and every coding agent working in this repository.

## Read First

1. `PROJECT_CONTEXT.md`
2. `CURRENT_STATE.md`
3. `DECISIONS.md`
4. `ROADMAP.md`
5. `EXECUTION_LEDGER.yaml`
6. `system/control-plane/routing-policy.md`
7. `system/control-plane/budget-policy.yaml`

## Before Work

- Confirm the current milestone and dependency gate.
- Confirm your assigned branch and exact owned paths.
- Define verifiable acceptance tests and required artifacts.
- Check the control-plane budget and usage snapshot.
- Stop if another active workstream owns the same path.

## Execution Rules

- Work at the objective, guardrail, and exit-criteria level; do not wait for step-by-step instructions when the objective is clear.
- Prefer the simplest architecture that passes current acceptance tests.
- Do not silently change approved persona, legal, security, or product decisions.
- Preserve original source artifacts and provenance.
- Never place secrets, tokens, private credentials, or personal data in the repository.
- Do not publish, deploy, spend money, enable auto-reload, or perform destructive actions without explicit approval.
- Use deterministic tests and measurable evals wherever possible.
- Do not declare completion from an agent summary.

## Definition of Done

A task is complete only when all required conditions are met:

1. the full diff was inspected;
2. tests and evals passed;
3. required artifacts were opened and reviewed;
4. the branch changed only owned paths or documented exceptions;
5. actual cost and duration were recorded;
6. failures and lessons were appended to `system/control-plane/build-history.jsonl`;
7. the handoff states what is done, what is next, and what requires owner approval.

## Escalation

Stop and return evidence when:

- acceptance tests fail three times for the same reason;
- scope conflicts with an approved decision;
- files overlap another active workstream;
- quota or cost approaches a control-plane stop condition;
- required context or permissions are unavailable;
- legal, cultural-identity, security, or public-release judgment is required.
