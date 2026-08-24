# cofee-web LMS UI Automation

Playwright (TypeScript) UI test automation for the Lead Management System (LMS) module of `cofee-web`, focused on validating the LMS revamp (lead status/stage taxonomy unification) alongside baseline LMS coverage.

## Stack

- **Framework:** Playwright (TypeScript), `@playwright/test`
- **Reporting:** Allure (`allure-playwright` reporter → `allure-results/` → `npm run report:generate` → `allure-report/`)
- **CI:** GitHub Actions (`.github/workflows/ui-tests.yml`, manual `workflow_dispatch` only)
- **Browsers:** Chromium, Firefox, WebKit — desktop viewport only
- **Environments:** `dev` only (`https://web.dev.cofee.life`)

## Setup

```bash
npm install
npx playwright install --with-deps
cp .env.example .env   # fill in TEST_MOBILE_NUMBER / TEST_OTP for the dev test account
```

## Running

```bash
npm test                  # full suite, all 3 browser projects
npm run test:smoke        # @smoke-tagged tests only
npm run test:sanity       # @sanity-tagged tests only
npm run test:regression   # @regression-tagged tests only
```

## Reporting

```bash
npm run report:generate
npm run report:open
```

## Project layout

| Path | Purpose |
|---|---|
| `config/config.ts` | Environment base URL(s) and timeouts |
| `playwright.config.ts` | Browser projects, retries, Allure reporter, global setup |
| `global-setup.ts` | One-time authenticated-session setup (real mobile+OTP login) |
| `src/pages/` | Page objects, one per real LMS page |
| `src/core/assertHelper.ts` | Shared UI assertions and explicit-wait helpers |
| `tests/` | Feature-grouped spec files + shared `fixtures.ts` |
| `auth/` | Cached `storageState.json` (gitignored) |
| `context/` | Test design artifacts (`ui-context.md`, `ui-auth.md`, `ui-test-case-matrix.md`) |

## The LMS revamp this suite verifies

The lead status/stage taxonomy has been unified into one 10-value enum (`Prospect, Contacted, Market Qualified, Parked, Sales Qualified, Interested, In Discussion, Onboarded, Won, Lost`), now used consistently across the Dashboard's Conversion Funnel, the Leads list Status column, Leads Analytics, and the Reports filter — where the Dashboard funnel and Leads list Status previously each had their own separate vocabulary. See `context/ui-context.md`'s "⚠ The revamp" section and `context/ui-test-case-matrix.md` rows 10, 15, 19, 20, 22, 30, 31 for the tests that verify this directly.
