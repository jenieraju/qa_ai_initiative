# UI Automation Skills

Agent Skills for this repo. **Standards live in [AGENTS.md](../../AGENTS.md)** — skills add workflows, not duplicate rules.

Skills live here, in `.claude/skills/`, which is what Claude Code discovers.
`.cursor/skills` is a **symlink** to this directory so Cursor sees the same
files — one copy, no drift. Never add a second copy under `.cursor/`.

## Level guide

| Level | Who it's for | Focus |
|-------|--------------|-------|
| **Setup** | Anyone starting a new feature | Branching before work begins |
| **Discovery** | QA analysts, before test design | APP_CONTEXT.md index + living context_docs/<slug>.md |
| **Basic** | New contributors, first tests | Scaffolding, locators, layers |
| **Test design** | QA analysts, before coding | Test cases, coverage, mapping to code |
| **Implementation** | Automation engineers | Dataproviders, auth, API setup |
| **Maintenance** | Fixing broken/flaky tests | Debug, refactor, review |
| **Meta** | Adding to this catalog | Writing new skills |

## Implemented skills

| Skill | Level | Folder |
|-------|-------|--------|
| Create feature branch | Setup | `create-feature-branch/` |
| Get context | Discovery | `get-context/` |
| Scaffold feature automation | Basic | `scaffold-feature-automation/` |
| Discover locators from UI | Basic | `discover-locators-from-ui/` |
| Generate test cases | Test design | `generate-test-cases/` |
| Map test cases to automation | Test design | `map-test-cases-to-automation/` |
| Create dataprovider | Implementation | `create-dataprovider/` |
| Auth storage state setup | Implementation | `auth-storage-state-setup/` |
| API test setup/teardown | Implementation | `api-test-setup-teardown/` |
| Test data teardown | Implementation | `test-data-teardown/` |
| Debug flaky E2E test | Maintenance | `debug-flaky-e2e-test/` |
| Review automation PR | Maintenance | `review-automation-pr/` |
| Create skill | Meta | `create-skill/` |

## New feature — full pipeline

```
create-feature-branch → get-context → generate-test-cases (approve) →
map-test-cases-to-automation → scaffold-feature-automation →
run against the live app → fix what the run disproves → repeat
```

The last two arrows are where the real work happens. Locators, copy and flows
confirmed from source still get disproved by the running app, and a suite that
goes green first try usually means an assertion that cannot fail.

## Planned (add when needed)

| Skill | Level | When to add |
|-------|-------|-------------|
| `resync-feature` | Maintenance | FE churn breaks suites / context_docs drift |
| `interact-with-common-controls` | Basic | Dropdown/modal/wizard pain |
| `handle-new-tab-window` | Implementation | Payment/OAuth flows |
| `parallel-group-design` | Execution | Parallel race failures |
| `generate-allure-report` | Execution | CI report triage |
| `convert-ac-to-automation` | Test design | Openspec/Jira AC heavy teams |

Dropped from this list as already covered: `fix-broken-locator`
(`discover-locators-from-ui` does it) and `refactor-test-layers`
(`tests/test/core/test_layer_boundaries.py` now detects violations
mechanically). Keep this list short — a long "planned" list reads as
capability that exists.

## Usage

Skills load when relevant, when you `@`-mention them (Cursor), or via
`/<skill-name>` (Claude Code). Invoke explicitly:

> Use the generate-test-cases skill for the login flow

Claude Code discovers project skills relative to the directory it was started
in — launch it **inside `qa_ai_initiative/`**, not the parent folder, or none
of these load.

Do **not** create skills for rules already in AGENTS.md (naming prefixes,
markers, import rules, etc.). Use `create-skill` to add one;
`tests/test/core/test_skills_sync.py` keeps this table, the frontmatter, and
every framework symbol these files name honest.

## Budget

Two limits, both enforced by `test_skills_sync.py`: **220 lines per skill** and
**1,800 lines for the whole catalog** (check headroom with
`cat .claude/skills/*/SKILL.md | wc -l`). The per-skill cap alone doesn't stop the
catalog growing past what anyone reads — every one of these files competes for
the same attention. Adding to a skill that is near its cap means cutting
something else in it, and adding a skill means the catalog total has to still
fit. Prefer editing an existing skill over adding a new one.
