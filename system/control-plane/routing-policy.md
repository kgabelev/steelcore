# AI Resource Routing Policy

## Dispatch order

1. Define the objective, owned files, acceptance tests, budget class, and forbidden actions.
2. Assign the cheapest capable primary worker.
3. Escalate only when evidence shows the worker cannot pass the acceptance tests.
4. Verify through deterministic tests, artifact inspection, and an independent reviewer for critical changes.
5. Append the result to `build-history.jsonl` and update routing evidence.

## Default ownership

- **GPT-5.6 Sol:** architecture, hard judgment, release gate, adversarial review.
- **GPT-5.6 Terra / Claude Sonnet 5:** primary implementation agents.
- **Claude Opus 5:** major refactors, long-horizon engineering, independent senior review.
- **Gemini Pro:** multimodal and UI architecture review.
- **Gemini Flash / Luna / Haiku:** economical parallel subagents and repetitive work.
- **Perplexity:** current research and source-backed synthesis; never primary repository owner.
- **Grok:** real-time culture and X intelligence; claims require source-quality review.
- **GitHub Actions:** canonical reproducible verification.
- **Ubuntu laptop:** trusted control node for credentials, rapid local checks, and repository operations.
- **Second laptop:** isolated browser-authenticated or long-running integration work when it prevents blocking the control node.

## Parallel agents

Use parallel agents only when scopes are independent and outputs can be merged mechanically or reviewed independently. Every agent receives:

- one branch or worktree;
- explicit file ownership;
- acceptance tests;
- budget and call ceiling;
- required artifacts;
- a stop condition.

Do not assign two implementation agents to the same files. Duplicate effort is reserved for independent verification, security review, or a measured model benchmark.

## Graphs, workflows, and loops

- **Graph:** dependent multi-stage work with branching decisions, retries, and typed handoffs.
- **Workflow:** a bounded objective that benefits from fan-out, verification, and fan-in.
- **Loop:** repeated empirical improvement against a measurable evaluator.
- **Routine:** scheduled maintenance with no unresolved shared context.

Never use a loop without a score, stopping threshold, maximum iterations, and cost ceiling.

## Branch and collision control

Branch names use `<domain>/<objective>-<agent>`. The orchestrator maintains a task ledger containing branch, owner, file paths, dependencies, and status. Agents may not edit unowned paths without requesting reassignment. Integration order follows dependency order, not completion time.

Before merge:

1. inspect the full diff;
2. run required tests in GitHub Actions;
3. inspect generated artifacts;
4. compare actual cost and duration with policy;
5. require independent review for critical releases.

## Learning loop

After every task, append one JSON object to `build-history.jsonl`. Promote a routing change only after repeated evidence, not one anecdote. Re-evaluate model instructions and scaffolding after major model releases; preserve useful evals until they saturate.
