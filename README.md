# The Delegation Discipline

A model-agnostic, tool-agnostic operating standard for deciding when an AI agent should
delegate work, how the delegated work must be scoped, and what evidence is required before
approval.

The central rule:

> Execution can be delegated. Judgment and accountability cannot.

This repository intentionally avoids depending on a specific vendor, model name, IDE,
agent runtime, or subagent feature. It is model-neutral by design. The roles below are
protocol roles. They can be implemented with multiple agents, a cloud coding agent, a local
CLI agent, a pull-request agent, or a single agent session with explicit plan, execute, and
review phases.

## Status, Scope, and Non-Goals

Status: draft standard, tested by repository-level document conformance tests.

Scope:

- AI-assisted coding, documentation, testing, review, and codebase exploration.
- Any environment where an agent can read context, produce artifacts, run tools, or ask
  another agent/process to do work.
- Online, offline, local LLM, cloud model, single-agent, and multi-agent workflows.

Non-goals:

- This is not a benchmark claiming universal token savings.
- This is not a prompt for one particular AI product.
- This is not permission to automate production, security, payment, data deletion, or
  compliance-sensitive work without human review.

## One-Page Rule

1. Use the strongest reasoning resource for framing, delegation, risk judgment, review,
   and approval.
2. Use execution resources for narrow implementation labor only when the task is
   independently verifiable.
3. Delegate only when the Independence, Oracle Completeness, and Scale gates all pass.
4. Give Workers typed briefs, not full chat history.
5. Workers return claims plus evidence. Claims alone do not count.
6. The Orchestrator independently verifies the evidence before approving.
7. If the task cannot be verified, do not delegate it.

## Normative Language

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used in the RFC 2119 sense:

- MUST means the rule is required for conformance.
- SHOULD means the rule is recommended unless there is a documented reason to deviate.
- MAY means the rule is optional.

## Definitions

- Orchestrator: the protocol role that owns requirement analysis, decomposition, risk
  judgment, delegation decisions, verification, approval, and reporting.
- Worker: the protocol role that performs bounded execution labor according to a brief.
- Oracle: an evidence source that can judge whether a task is complete. It can be a test
  command, build, type check, lint, static analysis rule, benchmark, reproducible artifact,
  or documented human review checklist.
- Brief: a typed task contract from Orchestrator to Worker.
- Evidence: reproducible output that supports or refutes a Worker claim. Examples include
  command output, exit code, artifact path, diff, test report, log excerpt, screenshot, or
  reviewer note.
- Independence: the degree to which a task can be completed without shared mutable state,
  sequential dependency, or concurrent edits to the same target.
- Oracle Completeness: how much of the task's correctness the oracle actually covers.
- Scale: the expected benefit of delegation after counting brief cost, context transfer,
  verification, retries, model cost, runtime, and risk.

## Roles and Accountability

### Orchestrator

The Orchestrator MUST:

- clarify objective, constraints, risks, and done criteria;
- split work into small, independently verifiable units;
- decide whether delegation is allowed;
- write the brief;
- assign scope, permissions, and evidence requirements;
- verify Worker output independently;
- own final quality and approval.

The Orchestrator MAY make tiny direct edits when delegation overhead exceeds the task.

### Worker

The Worker MUST:

- execute only the assigned scope;
- respect allowed files, tools, commands, and budget;
- avoid unrelated refactors and broad rewrites;
- run requested validation when permitted;
- report changed files, commands run, results, failures, skipped checks, and remaining
  risks;
- escalate when the brief is unclear, scope drifts, validation repeatedly fails, or a new
  risk appears.

The Worker MUST NOT approve its own work.

## Capability Model

Before delegation, record the environment:

- agent topology: single-agent, subagent, cloud agent, PR agent, local CLI, local LLM;
- filesystem permission: read-only, workspace-write, broad write, or unrestricted;
- command permission: none, allowlist, approval-gated, or unrestricted;
- network permission: disabled, allowlist, approval-gated, or unrestricted;
- secret access: denied by default;
- sandbox boundary and approval policy;
- budget cap: max Workers, max turns, max runtime, max retry count, and token/cost ceiling.

Orchestrator and Worker are not security boundaries. Sandboxes, permissions, audits, and
human approval are the security boundaries.

## Delegation Decision Procedure

Delegate only if all three gates pass.

### Gate 1: Independence

Passes when:

- the Worker can finish the unit without changing the same files as another Worker;
- the unit has no hidden sequential dependency;
- the unit does not require global architecture judgment;
- exclusive file ownership can be assigned.

Fails when shared state, state machines, timing, concurrency, migrations, or broad product
decisions are central to correctness.

### Gate 2: Oracle Completeness

Classify the oracle before delegating:

| Grade | Meaning | Delegation Rule |
|---|---|---|
| Full | The oracle covers the acceptance criteria. | Delegation allowed if other gates pass. |
| Strong partial | The oracle covers the risky part but not all style/design concerns. | Delegate only the covered part and review the remainder manually. |
| Weak partial | The oracle catches only syntax or shallow regressions. | Delegate mechanical work only. |
| None | No reproducible check exists. | Do not delegate. |

If the oracle is incomplete, the Orchestrator MUST either shrink the task to the oracle or
upgrade the oracle first.

### Gate 3: Scale and Risk

Delegation is justified only when expected value is positive:

```text
delegation_value =
  implementation_savings
  - brief_authoring_cost
  - context_transfer_cost
  - verification_cost
  - expected_retry_cost
  - model_runtime_cost
  - risk_penalty
```

Measure in the unit that matters for your environment: tokens, time, money, risk, or a
weighted score. If the task is trivial, tightly coupled, or has a weak oracle, assume the
value is negative.

## Decision Table

| Task Shape | Oracle | Risk | Decision |
|---|---|---|---|
| Mechanical rename across files | build/typecheck full | low | Delegate to Patch Worker. |
| Run tests and collect logs | command output full | low | Delegate to Test Worker. |
| Explore code ownership | file/line references partial | low | Delegate read-only Search Worker. |
| Untested business logic | weak or none | medium | Do not delegate; upgrade oracle first. |
| Auth, payment, production, data deletion | partial at best | high | Human-reviewed Orchestrator work only. |
| Parallel PR review dimensions | checklist plus diff | medium | Delegate to read-only Review Workers. |

## Brief Contract

Use a machine-readable brief whenever possible.

```yaml
objective: "Update deprecated API calls in the parser package."
scope:
  allowed_paths:
    - "src/parser/"
    - "tests/parser/"
  forbidden_paths:
    - "src/auth/"
    - "infra/"
permissions:
  filesystem: "workspace-write"
  commands:
    - "python -m pytest tests/parser"
    - "python -m mypy src/parser"
  network: "disabled"
  secrets: "denied"
acceptance_criteria:
  - "No deprecated API call remains in src/parser."
  - "Parser tests pass."
oracle:
  commands:
    - "python -m pytest tests/parser"
    - "python -m mypy src/parser"
out_of_scope:
  - "Formatting unrelated files"
  - "Changing parser behavior"
relevant_context:
  locations:
    - "src/parser/api.py"
    - "tests/parser/test_api.py"
  existing_patterns:
    - "Follow the adapter pattern in src/parser/api.py."
rejected_alternatives:
  - "Do not replace the parser package wholesale; it changes public behavior."
evidence_required:
  - "changed files"
  - "diff summary"
  - "command, exit code, and relevant output excerpt"
  - "unverified areas"
budget:
  max_turns: 6
  max_redelegations: 2
  max_runtime_minutes: 20
```

## Worker Lifecycle

1. Assign: Orchestrator writes a scoped brief.
2. Acknowledge: Worker restates objective, scope, oracle, and blocked permissions.
3. Execute: Worker performs only allowed actions.
4. Evidence: Worker returns claim and evidence separately.
5. Handback: Worker lists failures, skips, and risks.
6. Verify: Orchestrator independently runs or inspects the oracle.
7. Decide: Orchestrator approves, re-briefs the failure point, does the work directly, or
   escalates.

## Verification and Evidence Protocol

MUST:

- prefer machine oracle first and LLM judgment second;
- independently verify Worker output;
- separate claim from evidence;
- record command, exit code, and relevant output excerpt;
- store bulky logs as artifact path plus hash or summary;
- redact secrets, tokens, private keys, personal data, and customer data;
- quote enough final oracle output to be reproducible without copying entire logs.

MUST NOT:

- approve based only on "done" or "tests passed";
- accept Worker-generated tests as the only proof unless the test oracle itself was
  reviewed;
- paste raw logs containing secrets or private data;
- let the Worker define success after it has already produced the patch.

## Worker Taxonomy

| Worker Type | Safe Use | Required Check | Output Contract |
|---|---|---|---|
| Search Worker | Find symbols, files, references. | File and line spot check. | `path:line` findings. |
| Inventory Worker | Count files, configs, tests, owners. | Sampling and path list. | Table with counts and paths. |
| Patch Worker | Small mechanical edits. | Diff plus oracle commands. | Changed files, rationale, oracle output. |
| Test Worker | Run commands and collect failures. | Raw command output. | Command, exit code, key logs. |
| Log Triage Worker | Classify failures. | Evidence lines. | Suspected cause with log references. |
| Docs Worker | Draft fact-based docs. | Source traceability. | Draft plus source mapping. |
| Refactor Worker | Oracle-covered refactor. | Compile/type/test pass. | Invariant checklist. |
| Fixture Worker | Regenerate golden files. | Deterministic command. | Changed fixtures and command output. |
| Review Worker | Checklist review. | Orchestrator re-review. | Findings with severity and location. |
| Grill Worker | Pressure-test a plan from one adversarial angle. | Question tree plus evidence. | Decision questions, recommended answers, blocking objections. |
| Cleanup Worker | Formatting/import/dead-code cleanup. | Lint/build pass. | Removed/changed items and oracle output. |

Workers SHOULD be specialized by role, permission, and output schema rather than by brand
or model name.

## Multi-Agent Grill Protocol

Use grill only when the decision is consequential, ambiguous, or likely to become durable
policy. A grill is not a brainstorming session. It is a structured adversarial review.

The Orchestrator SHOULD split the grill into independent angles:

- scope and non-goals;
- portability across agent environments;
- oracle and testability;
- token, cost, and latency;
- security, privacy, and permissions;
- local/low-tier Worker limits;
- failure modes and escalation;
- evidence quality.

Each Grill Worker MUST return:

1. decision questions;
2. as-is risk;
3. to-be rule;
4. recommended answer;
5. evidence or missing evidence;
6. blocking objections.

The Orchestrator MUST resolve the questions, record accepted and rejected objections, and
turn accepted objections into brief fields, tests, safeguards, or documentation changes.
Unresolved blocking objections prevent approval.

## Low-Tier and Local LLM Policy

A low-tier or local LLM is not a weaker Orchestrator. It is a bounded labor process.

Use low-tier/local Workers for:

- search and inventory;
- mechanical patches;
- lint, formatting, type, and build fixes;
- test execution and log collection;
- fixture regeneration;
- documentation extraction from cited sources;
- small bug fixes with one failing test and one target file.

Do not use low-tier/local Workers for:

- requirement interpretation;
- architecture choice;
- security-sensitive logic;
- auth, payment, privacy, compliance, or production changes;
- concurrency, timing, state machines, numerical correctness, or untested business logic;
- broad refactors or migrations;
- public API contract changes.

Optimization rules:

- give typed briefs instead of full chat history;
- keep files and commands allowlisted;
- use rigid output schemas;
- split search, patch, and test into different worker types;
- use file paths and summaries for bulky output;
- re-brief only the failure point;
- stop after two failed repair attempts;
- lower model tier only when oracle strength rises.

See [docs/low-tier-local-workers.md](docs/low-tier-local-workers.md).

## Safeguards and Security

Workers MUST NOT receive default access to:

- secrets, `.env`, private keys, tokens, cookies, credentials;
- production databases, production shells, deployment controls;
- IAM/RBAC, billing, refunds, payments, legal approvals;
- unrestricted network access;
- arbitrary package installation or setup scripts;
- protected branch direct push or force push;
- audit log deletion;
- customer data export.

Stop or escalate when:

- a Worker edits out-of-scope files;
- a Worker asks for broader permissions;
- a secret or private datum appears in output;
- tests fail repeatedly;
- the oracle is weaker than expected;
- setup scripts, install hooks, DNS calls, or network behavior appear in an unfamiliar repo;
- concurrent Workers touch the same file;
- audit evidence is missing.

## Failure Handling and Escalation

- Re-delegate at most twice.
- Re-delegation MUST target the failure point, not restart the whole task.
- Use step caps, token-budget assertions, runtime caps, and loop detectors.
- Escalate high-risk changes to a human reviewer.
- Do not treat "more agents" as a fix for unclear requirements.

## Conformance Levels

Core:

- roles defined;
- three-gate decision used;
- brief includes objective, scope, oracle, out-of-scope, and evidence;
- Worker claims independently verified.

Recommended:

- machine-readable brief;
- worker taxonomy;
- sandbox and permission policy;
- retry and budget caps;
- evidence log with redaction.

Strict:

- all Recommended controls;
- human review for high-risk work;
- security scan where applicable;
- audit trail for agent, model class, commands, artifacts, and unresolved risks;
- conformance tests pass.

## Evidence and Method

This standard is grounded in:

- official documentation and product behavior from GitHub, OpenAI, and Anthropic;
- developer adoption and risk data from Stack Overflow;
- security research on agentic coding prompt injection;
- community signals from Reddit, YouTube, GeekNews, and Hacker News used only as secondary
  signals;
- local pilot tests comparing baseline prompting with Advisor/Worker prompting.

Main findings:

- subagents help with parallelism, isolation, and specialization, but do not guarantee token
  savings;
- clear context, durable repo rules, tests, diff review, and sandbox policy improve agent
  reliability;
- human review remains required for consequential work;
- cost and privacy concerns are real adoption blockers;
- prompt injection risk rises when agents can run shell, file, install, and network tools.

See [docs/evidence.md](docs/evidence.md) and [docs/test-matrix.md](docs/test-matrix.md).

## Running the Tests

This repository uses standard-library Python tests.

```bash
python -m unittest discover -s tests
```

The tests verify document contract, source coverage, security guardrails, worker taxonomy,
local LLM constraints, and at least 25 matrixed conformance cases.

## Final Sentence

> Ask the strongest AI agent to decide what work should be done, who should do it, under
> what constraints, and what evidence is required before approval. Let execution be
> delegated; never delegate judgment or accountability.

## Contributing

Contributions should improve the discipline by adding stronger oracles, clearer briefs,
better security boundaries, more realistic evidence, or new tested domain adaptations.
