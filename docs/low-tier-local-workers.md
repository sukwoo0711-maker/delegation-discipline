# Low-Tier and Local Worker Policy

This policy exists because small, cheap, or local models can be useful Workers, but only
when their limits are treated as design constraints.

## Representative Limits

Low-tier and local LLM Workers commonly struggle with:

1. long-context retention;
2. instruction hierarchy;
3. missing or ambiguous briefs;
4. repository-wide architecture inference;
5. hallucinated APIs, files, flags, or commands;
6. multi-step dependency ordering;
7. patch precision;
8. unrelated formatting or refactor churn;
9. confusing test symptoms with root causes;
10. over-trusting their own verification;
11. hidden risks such as security, concurrency, timing, and numerical edge cases;
12. rigid output contracts.

## Good Worker Jobs

Use low-tier/local Workers for work where the oracle is strong:

- Search Worker: find symbols, references, files, and owners.
- Inventory Worker: count files, tests, settings, and coverage areas.
- Test Worker: run commands and return exit codes plus key logs.
- Log Triage Worker: classify failures using cited log lines.
- Patch Worker: make narrow mechanical edits.
- Fixture Worker: regenerate deterministic snapshots or golden files.
- Cleanup Worker: run formatting, import cleanup, and dead-code cleanup.
- Docs Worker: extract facts from cited sources into a draft.

## Bad Worker Jobs

Do not assign low-tier/local Workers to:

- requirements interpretation;
- product or architecture decisions;
- security-sensitive logic;
- auth, authorization, payment, privacy, compliance, legal, or production changes;
- state machines, concurrency, timing, interrupt logic, distributed state, or migrations;
- numerical correctness or financial calculations;
- public API contract changes;
- broad refactors;
- untested business logic;
- tasks where the Worker must invent the oracle.

## Worker Contracts

| Worker | Brief Must Include | Check | Output Contract |
|---|---|---|---|
| Search Worker | query, paths, exclusions | spot-check file lines | `path:line` findings |
| Inventory Worker | scope and grouping rule | count sampling | table with paths and counts |
| Test Worker | command, cwd, expected signal | raw output | command, exit code, key logs |
| Log Triage Worker | log source and categories | cited lines | cause hypothesis with evidence |
| Patch Worker | exact files and edit class | diff plus oracle | changed files and command output |
| Fixture Worker | generation command | deterministic rerun | changed fixtures and hash/summary |
| Docs Worker | source files and audience | source traceability | draft plus source mapping |
| Review Worker | checklist and file list | Orchestrator re-review | findings with severity and location |

## Optimization Rules

1. Give typed briefs, not full history.
2. Keep file scope small.
3. Split search, patch, test, and review into different Workers.
4. Use commands and expected outputs as acceptance criteria.
5. Require claim/evidence separation.
6. Require path-based output for bulky artifacts.
7. Use allowlists for commands and paths.
8. Re-brief only the failure point.
9. Stop after two failed repairs.
10. Lower model tier only when oracle strength rises.

## Local LLM Notes

Local LLMs can reduce provider-side data exposure and provider cost, but local execution
often shifts risk to the machine running the model. Treat local does not send to cloud as
only one privacy property. It does not prove correctness, safety, permission control, or
prompt injection resistance.

Local Worker briefs SHOULD be shorter, stricter, and more schema-driven than briefs for
strong cloud models.
