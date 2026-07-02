# Evidence and References

Checked as of 2026-07-03 KST.

This document records the evidence used to harden The Delegation Discipline. Primary sources
are official product documentation, official product blogs, surveys, and security research.
Community sources are used only as secondary signals and MUST NOT be the sole support for a
normative rule.

## Evidence Table

| Claim | Primary Source | Second Signal | Discipline Implication |
|---|---|---|---|
| Coding agents can perform bounded issue work such as bug fixes, tests, and PR creation. | GitHub describes Copilot coding agent background work and PR workflows in its product updates: https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/ | GitHub Agent HQ positions agents as selectable tools for different steps: https://github.blog/news-insights/company-news/pick-your-agent-use-claude-and-codex-on-agent-hq/ | Delegation should target scoped issue or PR units with reviewable output. |
| Model routing is a product trend, but routing should follow task risk. | GitHub Copilot coding agent includes model picker and self-review/security scanning in the product direction: https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/ | Claude Code subagents support model and tool selection per subagent: https://code.claude.com/docs/en/sub-agents | Strong reasoning belongs on judgment, review, and high-risk tasks; lower-tier resources belong only where the oracle is strong. |
| Subagents help with parallelism and context isolation, but do not guarantee token savings. | OpenAI Codex docs state subagents are useful for parallel exploration and multi-step plans, and consume more tokens than comparable single-agent runs: https://developers.openai.com/codex/subagents | Reddit users report that subagents help mainly when a cheaper/different model is used and can be slower: https://www.reddit.com/r/codex/comments/1ttqfac/stop_wasting_tokens_use_sub_agents/ | Do not sell delegation as automatic token savings. Treat it as a quality, isolation, and parallelism tool. |
| Agent work should be configured with durable repo context and explicit done criteria. | Codex best practices recommend goal, context, constraints, and done-when criteria, plus AGENTS.md for durable rules: https://developers.openai.com/codex/learn/best-practices | GeekNews reports recurring interest in Claude.md, skills, and subagents as reusable context: https://news.hada.io/topic?id=29957 | Briefs must be typed, scoped, and reusable. Durable guidance beats repeated long prompts. |
| Sandboxing and approvals are separate controls. | Codex sandboxing docs distinguish technical sandbox boundaries from approval policy: https://developers.openai.com/codex/concepts/sandboxing | GitHub Copilot responsible-use docs describe workspace isolation and human review before merge: https://docs.github.com/en/copilot/responsible-use/agents | Orchestrator review is not a security boundary. Scope and sandbox Workers separately. |
| Human review remains required for consequential work. | GitHub responsible-use docs state that Copilot code review supplements rather than replaces human review: https://docs.github.com/en/copilot/responsible-use/agents | Stack Overflow 2025 shows limited trust in AI output accuracy: https://survey.stackoverflow.co/2025/ai | Agent output needs independent review, especially where accountability matters. |
| Agents with shell, file, install, and network tools expand the prompt injection threat model. | 0DIN disclosed a 2026 agentic coding exploit using an apparently clean repo and runtime payload delivery: https://0din.ai/blog/clone-this-repo-and-i-own-your-machine | GitHub and OpenAI docs both emphasize permission, sandbox, and approval controls. | Untrusted repos, setup scripts, package install hooks, DNS, and network behavior require extra approval or isolation. |
| Developer adoption is constrained by trust, security, and cost. | Stack Overflow 2025 reports heavy AI tool usage but low high-trust rates and caution around complex tasks: https://survey.stackoverflow.co/2025/ai | Reddit and Hacker News discussions repeatedly question token cost and quality of subagent workflows: https://news.ycombinator.com/item?id=45181577 | The standard needs budget caps, privacy boundaries, permission boundaries, and explicit escalation. |
| Community attention is high, but community content is not a primary authority for normative rules. | Primary rule support remains the official agent and safety documentation above, such as OpenAI subagent docs: https://developers.openai.com/codex/subagents | Recent YouTube, GeekNews, Reddit, and Hacker News content shows strong interest in subagents and reusable agent workflows. | Community adoption may inform examples and objections, but conformance rules must be grounded in primary sources or local tests. |

## Source Weighting

Authoritative sources:

- GitHub Blog and GitHub Docs for GitHub Copilot and Agent HQ behavior.
- OpenAI Codex docs for Codex subagents, best practices, and sandboxing.
- Claude Code docs for subagent context, tools, model routing, and permissions.
- Stack Overflow Developer Survey for developer sentiment and trust signals.
- 0DIN security research as a primary disclosure for agentic coding attack surface.

Secondary signals:

- Reddit: useful for cost and workflow anecdotes, not for normative claims.
- GeekNews: useful for Korean developer attention and curation signals.
- YouTube: useful for trend visibility, not for authoritative rules.
- Hacker News: useful for practitioner objections and failure anecdotes.

## Rules Derived From Evidence

1. Delegation MUST be explicit or rule-authorized.
2. Subagents SHOULD be justified by parallelism, isolation, specialization, or quality, not
   assumed token savings.
3. Every delegated Worker MUST have role, scope, tool limits, evidence requirements, and
   budget caps.
4. Read-heavy exploration SHOULD be read-only and return file evidence, not raw context.
5. Unknown setup, install, script, DNS, and network behavior MUST require approval or
   sandbox isolation.
6. Agent-generated changes MUST pass tests or documented review gates before merge.
7. Consequential work MUST receive human review.
8. Agent output MUST be traceable to task source, commands run, artifacts produced, and
   unresolved risks.
