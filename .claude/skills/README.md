# UI Automation Skill Suite (reserved)

This mirrors `skills/api/` (in [KeyValueSoftwareSystems/group_b_api_automation](https://github.com/KeyValueSoftwareSystems/group_b_api_automation)) but for UI test automation. Each teammate picking up a UI skill should add it following the same conventions as the API suite: frontmatter, `## When to use`, `## Guardrails`, numbered `## Steps`, `## Output template`, `## Notes for reuse across projects`.

Note: unlike upstream's `skills/ui/` + `skills/api/` split, this repo keeps all skills flat under `.claude/skills/<name>/SKILL.md` (Claude Code's own discovery path) — adjust any upstream path references (`skills/ui/...`, `skills/api/...`) accordingly when copying a skill or agent file in from there.

## Skills needed

**Core build sequence** (mirrors the API suite's shape):

| Skill | Purpose |
|---|---|
| `create-ui-framework-structure` | ✅ **Drafted** — see `.claude/skills/create-ui-framework-structure/SKILL.md`. Scaffolds a UI framework from scratch. Step 0 genuinely confirms language/framework (Playwright Python, Playwright TS, Selenium Python, Cypress, etc.), reporting tool, CI platform, and browsers/viewports — no single fixed default the way the API suite defaults to Python/pytest — then builds a framework-agnostic layer structure, with concrete example trees for each of the four frameworks named above so `ui-test-automation` has a real, consistent layout to discover rather than a conceptual list. |
| `get-ui-context` | ✅ **Drafted** — see `.claude/skills/get-ui-context/SKILL.md`. Discovers the UI surface — pages, components, user flows — from the repo (frontend routes/component tree), Figma, PRD, other docs, and Jira. Writes `context/ui-context.md`. Also jointly responsible (with an edited `get-context`) for populating the shared `context/business-context.md` — implements its own section now, via a marker-delimited merge, so it doesn't block on the API-side edit landing first. |
| `get-ui-auth` | ✅ **Drafted** — see `.claude/skills/get-ui-auth/SKILL.md`. Resolves the UI-specific layer of authentication only: login page/selectors, how a session shows up in the browser (cookie/localStorage), UI error-state cues for negative auth cases, and what a stale (expired mid-run) session looks like in the browser plus the re-authenticate-and-recover recommendation. Reuses `context/api-auth.md` for the underlying auth mechanism rather than rediscovering it from scratch. |
| `ui-test-design` | ✅ **Drafted** — see `.claude/skills/ui-test-design/SKILL.md`. Turns `context/ui-context.md` + `context/business-context.md` into a reviewed UI test case matrix. |
| `ui-test-automation` | ✅ **Drafted** — see `.claude/skills/ui-test-automation/SKILL.md`. Generates, executes, and validates UI tests against whichever framework was confirmed/detected. Framework-agnostic at the file level (resolves the stack rather than hardcoding one), and works two ways: matrix-driven (full `context/ui-test-case-matrix.md`) or ad-hoc for a single/few scenarios with no matrix at all — same generation quality either way, just less required input. |
| `ui-coverage-audit` | ✅ **Drafted** — see `.claude/skills/ui-coverage-audit/SKILL.md`. Cross-checks the UI test case matrix against `context/ui-context.md` for gaps (untested pages/flows, missing case types), mirroring `skills/api/coverage-audit`. |

**Reused as-is from upstream `skills/api/`** (already domain-agnostic, no UI fork needed — not yet copied into this repo): `create-report`, `ci-integration`, `flaky-test-triage`.

**Shared, at `.claude/skills/teardown/`** (not UI-specific): clears stale (pre-today) resources from either suite's runtime registry — the cleanup logic never depended on which suite created an entry.

See `.claude/agents/ui-automation-agent.md` for how these skills plug into a single UI automation workflow, and `.claude/agents/shared-project-config.md` for the project-identity fields both the API and UI agents read from instead of duplicating.
