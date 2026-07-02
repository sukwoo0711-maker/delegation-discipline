# Test Matrix

The conformance suite checks that the document set remains a standard, not just a slogan.
Each case maps a risk to a machine-checkable expectation.

| ID | Area | Case | Expected Evidence |
|---|---|---|---|
| TC-01 | Existence | README exists. | `README.md` is present. |
| TC-02 | Portability | The repo does not require a specific AI vendor. | No required-vendor language. |
| TC-03 | Portability | Model-agnostic and tool-agnostic wording exists. | README includes model/tool neutral wording. |
| TC-04 | Roles | Orchestrator role is defined. | Analysis, decomposition, verification, approval. |
| TC-05 | Roles | Worker role is defined. | Bounded execution labor. |
| TC-06 | Boundary | Worker cannot approve own work. | Explicit prohibition. |
| TC-07 | Boundary | Orchestrator/Worker isolation is described. | Boundary or isolation language. |
| TC-08 | Gate | Delegation gate exists. | Decision procedure section. |
| TC-09 | Gate | Independence axis exists. | Independence heading or text. |
| TC-10 | Gate | Oracle Completeness axis exists. | Oracle completeness heading or text. |
| TC-11 | Gate | Scale/cost axis exists. | Scale, token, cost, overhead, or budget language. |
| TC-12 | Gate | All gates must pass. | "all three gates pass" or equivalent. |
| TC-13 | Fallback | Failed gate fallback exists. | Do not delegate, re-decompose, or upgrade oracle. |
| TC-14 | Oracle | Oracle-first verification exists. | Machine oracle before LLM judgment. |
| TC-15 | Oracle | Oracle grades are documented. | Full, strong partial, weak partial, none. |
| TC-16 | Brief | Machine-readable brief exists. | YAML, JSON, or TOML block. |
| TC-17 | Brief | Brief has objective. | `objective`. |
| TC-18 | Brief | Brief has acceptance criteria. | `acceptance_criteria`. |
| TC-19 | Brief | Brief has oracle commands. | `oracle` and `commands`. |
| TC-20 | Brief | Brief has out-of-scope. | `out_of_scope`. |
| TC-21 | Brief | Brief has relevant context. | `relevant_context`. |
| TC-22 | Brief | Brief has evidence required. | `evidence_required`. |
| TC-23 | Evidence | Claim and evidence are separated. | Claim/evidence language. |
| TC-24 | Evidence | Bulky output is artifact path plus summary/hash. | Artifact path, hash, or summary. |
| TC-25 | Cost | Token/cost warning exists. | Token or cost warning. |
| TC-26 | Safeguards | Retry cap exists. | Re-delegate at most twice. |
| TC-27 | Safeguards | Step cap, budget cap, and loop detector exist. | All three phrases. |
| TC-28 | Workers | Worker taxonomy exists. | Worker Taxonomy section. |
| TC-29 | Workers | Safe mechanical workers are documented. | Patch, cleanup, fixture, test. |
| TC-30 | Workers | Forbidden high-risk work is documented. | Auth, payment, production, data deletion. |
| TC-31 | Local LLM | Local/offline constraints exist. | Low-tier and Local LLM Policy. |
| TC-32 | Local LLM | Local LLM does not replace oracle. | Oracle strength still controls delegation. |
| TC-33 | Security | Secret handling rule exists. | Secrets denied or redacted. |
| TC-34 | Security | Sandbox/permission language exists. | Sandbox and approval policy. |
| TC-35 | Security | Prompt injection threat is referenced. | Setup/install/script/DNS/network warnings. |
| TC-36 | Evidence | Evidence references exist. | `docs/evidence.md` and URLs. |
| TC-37 | Hygiene | No mojibake or replacement characters. | No replacement characters or broken question-mark artifacts. |
| TC-38 | Hygiene | Internal markdown links resolve. | Link targets exist. |
| TC-39 | Hygiene | No unfinished markers. | No unfinished markers in docs. |
| TC-40 | Push Ready | Tests can run with standard-library Python. | `python -m unittest discover -s tests`. |
| TC-41 | Grill | Multi-agent grill protocol exists. | Grill Worker and grill workflow are documented. |
| TC-42 | Evidence | Evidence has checked date. | `Checked as of` line exists. |
| TC-43 | Evidence | Community sources are secondary. | Community source limitation is explicit. |
| TC-44 | Evidence | Primary evidence rows include URLs. | Primary source cells have concrete URLs. |
| TC-45 | Tests | Matrix promises TC-24/TC-30/TC-40 have direct tests. | Artifact/hash, high-risk forbidden work, and test command are tested. |

## Manual Review Cases

The automated tests prove document structure and key terms. They do not prove that the
discipline is correct for every project. Before adopting it in a sensitive environment,
review these manual cases:

- unfamiliar repo with install scripts;
- production hotfix;
- auth or permission change;
- large refactor;
- weak tests;
- local-only model with no network;
- cloud agent with broad network;
- parallel Workers on overlapping files;
- generated PR with failing CI;
- Worker-generated tests that pass but assert the wrong behavior.
