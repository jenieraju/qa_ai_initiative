# UI Automation Skills

Optional Cursor Agent Skills for this repo. **Standards live in [AGENTS.md](../../AGENTS.md)** — skills add workflows, not duplicate rules.

## Level guide

| Level | Who it's for | Focus |
|-------|--------------|-------|
| **Basic** | New contributors, first tests | Scaffolding, locators, layers |
| **Test design** | QA analysts, before coding | Test cases, coverage, mapping to code |
| **Implementation** | Automation engineers | Dataproviders, auth, API setup |
| **Execution** | Running and reporting | CI, parallel, Allure |
| **Maintenance** | Fixing broken/flaky tests | Debug, refactor, review |

## Implemented skills

| Skill | Level | Folder |
|-------|-------|--------|
| Scaffold feature automation | Basic | `scaffold-feature-automation/` |
| Discover locators from UI | Basic | `discover-locators-from-ui/` |
| Generate test cases | Test design | `generate-test-cases/` |
| Map test cases to automation | Test design | `map-test-cases-to-automation/` |
| Create dataprovider | Implementation | `create-dataprovider/` |
| Auth storage state setup | Implementation | `auth-storage-state-setup/` |
| API test setup/teardown | Implementation | `api-test-setup-teardown/` |
| Debug flaky E2E test | Maintenance | `debug-flaky-e2e-test/` |

## Planned (add when needed)

| Skill | Level | When to add |
|-------|-------|-------------|
| `interact-with-common-controls` | Basic | Dropdown/modal/wizard pain |
| `handle-new-tab-window` | Implementation | Payment/OAuth flows |
| `parallel-group-design` | Execution | Parallel race failures |
| `generate-allure-report` | Execution | CI report triage |
| `review-automation-pr` | Maintenance | Team PR reviews |
| `convert-ac-to-automation` | Test design | Openspec/Jira AC heavy teams |
| `fix-broken-locator` | Maintenance | Frequent UI churn |
| `refactor-test-layers` | Maintenance | Layer violations in PRs |

## Usage

Skills load when relevant or when you @-mention them in chat. Invoke explicitly:

> Use the generate-test-cases skill for the login flow

Do **not** create skills for rules already in AGENTS.md (naming prefixes, markers, import rules, etc.).
