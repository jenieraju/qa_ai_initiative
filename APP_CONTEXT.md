# APP_CONTEXT.md — cofee-web functional context

This repo tests **cofee-web**, a separate application (its own source repo,
not part of this codebase). This file is the shared reference for what that
app *does*, so anyone here can plan and write new tests without re-reading
the application source from scratch. It captures the app's domain, features,
and routes — see [AGENTS.md](AGENTS.md) for how *this* framework is built.

Sourced from the app's own `AGENTS.md` and a direct read of its
`src/features/authentication/**` source (see "Locator strategy notes"
below). If anything here looks stale, the app's source is the source of
truth — update this file when you notice drift.

## What it is

cofee-web is the frontend for a **recurring payment collection system**,
built with React 18 + TypeScript, Redux Toolkit/RTK Query, MUI, and
Tailwind.

## Domain model

- Two account types: **individual** (single branch) and **organization**
  (multiple branches).
- Each branch contains **groups** and **members**.
- **Payment links** go out to group members on a configured interval:
  monthly, weekly, by terms, or **quick collect** (one-off, no group
  membership needed).
- Organizations manage team members via roles (Branch Admin, Group Admin,
  etc.).

## Features

| Feature | What it does |
|---|---|
| Attendance | Track member attendance; attendance-based fee collection |
| Events | Create events with registration links |
| Team Management | Invite/manage team members with roles |
| Lead Management | Track sales/enquiry leads |
| Expense Tracker | Record and categorize expenses |
| Tally Integration | Sync with Tally accounting software |
| Webhook Configuration | Configure outgoing webhooks |
| Reports | Multiple report types, Excel/CSV export |
| Docs | In-app API reference, API keys, webhook event reference |
| Subscription | Plan management, KYC verification, billing |
| Quick Collect | One-off payment link generation, no group membership |

## Environments

- Production: `web.cofee.life`
- Sandbox (for testing): `web.sandbox.cofee.life` — also seen used as
  `web.dev.cofee.life` for this framework's `dev` env (see `.env.dev.example`)
- API URL is a separate host, set via the app's own `REACT_APP_API_URL` —
  not documented here; confirm with the app team before wiring a new
  `API_BASE_URL` in this framework's settings.

## Authentication & onboarding flow

Already automated in this repo — see `src/page_objects/{login,onboarding,
document_upload,payment_selection}_po.py` and
`tests/test/auth/{test_login,test_onboarding}.py`.

```
/login (mobile number + OTP)
  → new user, 0 orgs → /select-account
      → name + Individual/Organization choice
          Individual → business name → Continue → onboards directly → /dashboard
          Organization → business name → Continue → /document-upload
              → PAN/GSTIN + certificate file + business-license file → Continue
              → /select-payment → bank account + IFSC verification → Proceed
              → /dashboard
  → existing user, 1 org → /dashboard (or /lead-management/dashboard for lead roles)
  → existing user, >1 org → /organization-selection
```

Notes:
- A referral-code screen (`ReferralCode` component) exists in the source
  but is **currently unreachable** — its gating state defaults to
  already-passed, confirmed by live testing. Don't assume it appears.
  Automated flows skip straight from OTP to the account-selection form.
- Onboarding is a **one-time, irreversible transition per identity** — once
  a mobile number completes it, that number becomes a normal existing user
  forever. Every new onboarding test needs a mobile number with **zero
  existing organizations**; reusing one from a previous run will skip
  straight past `/select-account`.
  - This is also why the onboarding tests register **no teardown**: there is
    no delete API for the org/user this flow creates, so there's nothing a
    `teardown_registry` cleanup could call (see AGENTS.md → "Teardown"). If
    the app ever adds one, wire it in — don't leave this exception stale.

## Locator strategy notes (hard-won, don't rediscover these)

The app has **sparse `data-testid` coverage** — most values are defined
centrally in the app's `src/constants/testId.ts`, but plenty of screens
have none. Shared components behave predictably once you know the pattern:

| Component | Locator signal |
|---|---|
| `Button` | renders `label` as the button's accessible text — use role+name, not testid |
| `Input` | `id`/`name` = the `name` prop; often the *only* stable signal is `placeholder` |
| `Checkbox` | only has a `data-testid` if explicitly passed one |
| `AuthSection` (auth-area chrome) | `data-testid="authentication_title"` / `"authentication_description"`; also sets the page `<title>` via `Head` — both are reusable "page loaded" assertions for any new auth-area screen |
| `RadioGroup`/`RadioButton` | the underlying `<input>` gets `data-testid={option.id}` — check the `options` array passed in for a real id before assuming there's none |
| `Dropdown` | the closed-state button has no testid by default; open it and target options by their generated `id="{filterLabel or 'dropdown'}_{value}"` |
| `FileUpload` | hidden file input's `id` follows `"{label}_input_id"` — target with an attribute selector |

General rule: check the actual shared component in the app's
`src/components/` before assuming a locator doesn't exist or guessing a
selector — the pattern is usually one of the above.

## Writing new tests

Follow `AGENTS.md`'s four-layer architecture and "Adding a new feature"
checklist. Before automating a new cofee-web screen:
1. Read the real component source for that screen/feature in the app repo
   — never guess selectors.
2. Check the table above for the shared-component locator pattern first.
3. Update this file if you learn something that would have saved you time.
