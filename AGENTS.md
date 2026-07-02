# Agent Operating Rules

This repository defines a model-agnostic delegation standard. Apply it while editing the
repo.

## Required Behavior

- Treat Orchestrator and Worker as protocol roles, not as vendor or model names.
- Do not claim that delegation always saves tokens.
- Prefer evidence-backed claims and cite concrete sources in `docs/evidence.md`.
- Keep rules portable across single-agent, multi-agent, cloud, local CLI, and local LLM
  environments.
- When changing the standard, update tests or the test matrix if the contract changes.
- Run `python -m unittest discover -s tests` before reporting completion.

## Delegation Rule

Use delegated Workers only for scoped, independently verifiable work. The Orchestrator keeps
responsibility for goal framing, risk judgment, verification, and final approval.

## Safety Rule

Workers are execution subjects, not trust anchors. Advisors or Orchestrators are reviewers,
not security boundaries. Use scope, sandboxing, permissions, audit evidence, and human review
for consequential changes.
