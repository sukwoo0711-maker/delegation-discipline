# The Delegation Discipline

A **model-agnostic, tool-agnostic** protocol for splitting AI coding work between a
**judging Orchestrator** and an **implementing Worker** — without letting delegation
quietly cost more than it saves.

The premise is simple: in a coding session, implementation *labor* (reading files,
writing code, running tests, fixing errors) burns far more tokens than *judgment*
(design, decomposition, review). So keep judgment on your most capable model and
offload labor to a cheaper one. That premise is real — but it only pays off under
conditions, and it fails loudly when those conditions are ignored.

This document encodes **when delegation actually pays, and how to keep a Worker's
mistakes from cascading into your codebase.**

---

## Why this needs a discipline, not just a prompt

Delegation is not free labor. It is a contract that carries cost and error propagation.
The evidence is consistent across independent sources:

- **Multi-agent setups use far more tokens** — on the order of 3–15× a single agent for
  equivalent work. In one production report, ~80% of the variance in outcome quality was
  explained by raw token spend, not by "smarter" architecture. If the judgment gap between
  your tiers is small, the orchestration overhead simply eats the savings.
- **The deciding variable is task shape.** Independent, parallelizable subtasks benefit
  from delegation. Sequential, state-dependent, or shared-context work (much of coding,
  and nearly all tightly-coupled systems work) does *worse* when split across agents.
- **Generation and verification are different skills.** A model being a better *author*
  does not make it a better *verifier* — models tend to over-trust their own output and
  pass their own generated tests. Verification reliability comes from the **method**
  (a deterministic oracle) far more than from the model tier.
- **Errors cascade.** A downstream agent tends to accept an upstream agent's output as a
  valid premise without re-checking it. The Orchestrator↔Worker boundary is the only place
  to install isolation.

The discipline below turns those findings into rules.

---

## Layer 1 — Universal Core

> Model-agnostic, tool-agnostic. Drop this into any agent's system prompt or project rules.

### Roles

- **Orchestrator** — requirement analysis, task decomposition, delegation decisions,
  brief authoring, oracle-based verification, approval, reporting.
- **Worker** — implementation labor per the brief. Need not be more capable than the
  Orchestrator.
- **Tiering principle (model-neutral):** assign the most capable model to the *judgment*
  tier, and to the *labor* tier the cheapest model that can still clear the task's oracle.
  The stronger the oracle, the lower you can safely push the labor tier. If the oracle is
  weak, do **not** lower the tier.

### Delegation gate — three axes (delegate only if all three hold)

1. **Independence** — are the subtasks loosely coupled? (Shared state, sequential
   dependency, or edits to the same target ⇒ do not delegate.)
2. **Oracle completeness** — is there a deterministic oracle that judges completion, and
   does it *fully* capture this task's correctness? (If it captures only part, delegate
   only that part, or do it yourself.)
3. **Scale** — does the implementation saving exceed
   `[brief authoring + context transfer + verification round-trips + expected re-delegation cost]`?
   Assume delegation multiplies token spend several-fold, and delegate only when this
   inequality is positive. Between two tiers of similar judgment quality, it is usually
   negative.

> If any axis fails, the Orchestrator does the work directly or re-decomposes it into a
> verifiable unit.

### Hard rules

- **If you cannot verify it, do not delegate it.** An unverifiable delegation is a cascade
  with no isolation point.
- Do not split a sequential / state-dependent chain into a relay. Brief the whole chain to
  a single Worker in one shot.
- A Worker does not spawn its own sub-Workers. (Nested delegation multiplies cost.)
- Scale effort to task complexity. Do not attach many Workers to a trivial task.

### Brief specification (a typed context object — never dump full history)

Required fields:

- **Objective**
- **Acceptance criteria** — the exact oracle commands to run
- **Out of scope / do-not-touch**
- **Relevant locations** (files, paths, symbols) and examples of existing patterns to follow
- **Rejected alternatives** (and why) — to prevent re-exploration and re-invention

Before delegating, the Orchestrator checks its own brief's premises once. (A wrong premise
contaminates every downstream artifact.)

### Verification (oracle first, LLM judgment second)

- **First pass:** the machine gate — run the oracle commands yourself and confirm they pass.
- **Second pass:** qualitative review only for what the oracle cannot catch (design, style).
- **Never trust the Worker's "done."** Require a claim *separated from its evidence*:
  "it passed" (insufficient) → "this command produced this output" (sufficient). A claim
  without evidence is treated as unverified.
- The Orchestrator re-confirms the Worker's output independently via the oracle; it does not
  accept it as a premise.
- Quote the final oracle output verbatim rather than paraphrasing it, to avoid distortion.

### Safeguards (a termination condition is the only defense against cost blow-ups)

- **Re-delegate at most twice.** Beyond that, the Orchestrator intervenes directly or
  escalates to a human.
- Re-delegation is a diff/patch brief targeting the failure point — not "start over."
- Always set a step cap, a token-budget assertion, and a loop detector. (Kills infinite
  ping-pong between agents.)
- Receive bulky artifacts as a file path + summary, not inline, to keep the Orchestrator's
  context from bloating.
- For parallel delegation, assign exclusive file ownership per Worker. (No concurrent edits
  to the same file.)

---

## Layer 2 — Example Adaptation (worked example)

The universal core is deliberately abstract. Here is how one practitioner specializes it to
a **dual-domain, sometimes-offline** environment. Treat it as a template for writing your own
Layer 2 — note that it names *domain tools* but never a specific AI model.

### A. Runtime branches

- **Online** (sub-agent spawning available): apply the core delegation rules as written.
- **Restricted / offline network** (no spawning): replace delegation with *phase separation +
  context hygiene*. Within a single session, explicitly separate **plan → implement → verify**
  phases, and clear context at each transition (reset the session, or snapshot a summary and
  resume). Reuse the three-axis gate as the criterion for *whether to enter a phase now*.

### B. Firmware (C/C++) domain

- **Current oracle:** build success + static analysis (e.g. cppcheck / clang-tidy / MISRA).
  Functional correctness, timing, and hardware interaction are *outside* the oracle.
- **OK to delegate** (task classes the oracle fully covers):
  - Purely mechanical transforms (rename, formatting, header/include cleanup)
  - Changes the compiler enforces (signature change → update all call sites, enum/type swaps)
  - Resolving static-analysis findings; dead-code removal (linker-confirmed)
  - Work where "the build passes" *is* the success criterion (build config, linker scripts)
- **Do not delegate** (oracle incomplete → do it yourself or human-verify):
  - Control logic, state machines, algorithms; ISRs, concurrency, timing; peripheral register
    sequences; numerical correctness
- **Oracle upgrade path** (widens the delegatable surface):
  extract hardware-independent logic and put it under host-side unit tests (e.g.
  Unity/Ceedling, CppUTest). For that logic, functional correctness enters the oracle and
  delegation expands beyond "mechanical transforms."

### C. Data-asset / scripting pipeline (Python) domain

- **Current oracle:** thin (no first-party test suite yet). Type checking and linting are
  immediately available.
- **Right now:** delegate only work fully caught by types + lint (refactors, signature
  changes); keep functional logic in-house.
- **Oracle bootstrap** (a precondition for broad delegation, high ROI):
  stand up a test + type-check + lint scaffold first, then open pipeline-logic delegation.
  Because this is pure software, oracle completeness is cheap to raise — which is exactly why
  this domain becomes the *best* fit for delegation once bootstrapped.

---

## Origin & method

This started from a community workflow (the "Advisor Strategy": premium model as
Orchestrator, cheaper model as Worker) and was hardened through a multi-agent analysis of
its own claims plus external research — Anthropic's engineering writing on multi-agent
systems and effective agents, orchestrator/handoff patterns from LangGraph, the OpenAI
Agents SDK, CrewAI and MetaGPT, and practitioner postmortems on runaway multi-agent cost.

The core correction those sources produced: **delegation decisions should hinge on oracle
determinism and inter-task dependency — not on file count, model brand, or online/offline
status.** Everything above follows from that.

---

*Contributions welcome. This is a discipline, not dogma — adapt Layer 2 to your own
oracles and constraints.*
