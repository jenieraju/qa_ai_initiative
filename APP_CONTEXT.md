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

## Cross-feature relationships (check this before writing tests for any mutation)

The "Domain model" above states these links in prose; this table makes
them checkable. Read it before writing test cases for anything that
**creates, edits, or deletes** a shared entity — a change in one feature
can silently break another if the dependency isn't accounted for in the
test cases.

| Entity | Depended on by | What to verify when it's created/edited/deleted |
|---|---|---|
| **Branch** | Groups, Members | No delete-branch flow documented yet — n/a until one exists |
| **Group** | Payment links (interval/amount config lives on the group); Members (roster) | Deleting/editing a group with an active payment cycle or non-empty roster — **unconfirmed, no delete-group API exists yet** (see "Groups" below) |
| **Member** | Group rosters; Payment links (recipients); Attendance records; Team role assignment (Branch Admin / Group Admin) | Deleting/editing a member — does it cascade, block if dependents exist, or orphan the related group/payment/attendance/role record? **Unconfirmed — no deletion feature exists yet; see "Members" below** |
| **Team role** (Branch Admin / Group Admin) | Assigned to a Member | If the member holding a role is deleted or demoted — does the role vanish, block the action, or reassign? Unconfirmed |
| **Payment link** | Group members (recipients); Quick Collect payers | Member/group deletion while a cycle is active or pending — still unconfirmed, but now *testable*: Quick Collect creates a payment order against an existing member, and a `DELETE .../member/{memberId}` endpoint exists. A *Cancel a Payment Order* operation is documented in the app's API reference but its REST path is unconfirmed — see `context_docs/quick-collect.md` |

**Rule:** when a new feature's PRD touches an entity in the left column,
add/update its row here in the same pass as adding the feature's own
section below — and make sure the resulting test cases include the
cascade/block/orphan behavior explicitly (not just the happy-path create
flow). If the behavior isn't confirmed, say so in both this table and the
feature's own section — don't leave it undocumented, and don't guess.

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
| Quick Collect | One-off payment link generation, no group membership — see "Quick Collect" below |

## Environments

- Production: `web.cofee.life`
- Sandbox (for testing): `web.sandbox.cofee.life` — also seen used as
  `web.dev.cofee.life` for this framework's `dev` env (see `.env.dev.example`)
- API URL is a separate host, set via the app's own `REACT_APP_API_URL` —
  not documented here; confirm with the app team before wiring a new
  `API_BASE_URL` in this framework's settings.

## Authentication & onboarding flow

Already automated in this repo.
Detail: [context_docs/authentication-onboarding.md](context_docs/authentication-onboarding.md).

```
/login (mobile number + terms → OTP on same route)
  → new user, 0 orgs → /select-account
      → name + Individual/Organization choice
          Individual → business name → Continue → onboards directly → /groups
          Organization → business name → Continue → /document-upload
              → PAN/GSTIN + certificate file + business-license file → Continue
              → /select-payment → bank account + IFSC verification → Proceed
              → /groups
  → existing user, 1 org → /groups (or /dashboard / lead-management for some roles)
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

## Groups

Already automated in this repo.
Detail: [context_docs/groups.md](context_docs/groups.md).

```
Authenticated session → /groups → New Group → /groups/create
    → name + payment-collection interval (monthly/weekly/by-terms) + amount
    → Save and next → "Group created successfully" → group appears on /groups
```

Notes:
- Session reuse: tests prefer cookies from `.auth/{profile}.json` (saved by
  a prior login test) via `@pytest.mark.auth_profile`; fall back to a real
  UI login via `user_ensures_logged_in()` if that file is missing/expired.
- No teardown yet: confirm a delete-group API with the app team before
  wiring `teardown_registry` (see `AGENTS.md` → "Teardown").
- Only the create wizard's "basic details" step (name, interval, amount)
  is automated so far — editing, member assignment, and any further
  wizard steps are not yet covered.

## Quick Collect

Automated in this repo (happy path + amount validation).
Detail: [context_docs/quick-collect.md](context_docs/quick-collect.md).

```
Authenticated session → /quick-collect/create-link
    → Fee Amount (2–200000) + Notes  [+ "Do not send payment link to payers"]
    → select payer(s) from the members list
    → CTA "Send" (notifying) or "Create" (suppressed)
    → confirm dialog → /quick-collect/success
```

Notes:
- Gated on permission `PAYMENT_ORDER_CREATE` and on completed KYC.
- **The CTA label depends on the suppress-notifications checkbox** — "Send"
  becomes "Create" when it is checked. Don't hardcode "Send".
- Automation always suppresses notifications: the dev member list contains a
  real phone number, and the payment order is created either way.
- Only the "Add from members list" tab renders on the dev account; "Add
  manually" / "Import file" / "Add from group" are conditional and unconfirmed.
- Teardown gap: created payment orders are not cleaned up — a cancel operation
  is documented but its REST path is unconfirmed (see the context doc).

## Members

Route confirmed from the live bundle: `/members` list, `/members/add` (a
route, not a modal), `/members/:memberId` details. A
`DELETE v1/organisation/{orgId}/branch/{branchId}/member/{memberId}` endpoint
exists, so member teardown is wireable.

The creation-flow scaffold is still otherwise unconfirmed against the live app. A creation-flow scaffold exists
(`src/page_objects/{members,member_create}_po.py`,
`tests/test/members/test_member_create.py`) but every locator, the route,
and the required field set are placeholders — the test stays
`@pytest.mark.ignore` until someone runs `discover-locators-from-ui`
against the real Members tab and this section gets filled in with
confirmed facts (route, real flow, fields, any role/permission rules).

**If/when a member-deletion (or edit) feature lands**, per the
"Cross-feature relationships" table above, its test cases must explicitly
cover — not just assume — what happens to:
- the member's **group roster** membership(s)
- any **payment link** cycle they're currently a recipient on
- their **attendance** history, if attendance tracking is live by then
- any **team role** (Branch Admin / Group Admin) they hold

None of these cascade behaviors are confirmed yet — that's the point of
listing them here now, before the feature exists, so whoever picks up
that PRD checks with the app team instead of assuming "delete just
deletes."

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
| Helper text under an `Input` | `text-grey60`, **always rendered** — not a validation error. Invalid input is signalled by disabling the submit CTA instead (confirmed on Quick Collect). Probe with a valid value before asserting on it |
| Primary CTA label | can be **state-dependent** — Quick Collect's flips "Send" → "Create" when notifications are suppressed. Don't assume one label |

General rule: check the actual shared component in the app's
`src/components/` before assuming a locator doesn't exist or guessing a
selector — the pattern is usually one of the above.

## Writing new tests

Follow `AGENTS.md`'s four-layer architecture. Context is two-tier for the
long run — see `.claude/skills/get-context/SKILL.md`.

1. **Check this file first.** High-level only: Features table, domain,
   cross-feature table, existing `##` sketches. Use what's here; don't
   re-derive it. Keep this file lean — no locator essays.
2. **Then open `context_docs/<slug>.md`.** Via `Detail:` or slug match.
   That living record is the source for flows, coverage, and gaps from
   discovery through later steps. Do not start from a blank page.
3. **New flow (no context doc)?** Same turn, required:
   - Add a short `##` section here (what it does, route sketch, labeled
     unknowns — see "Members") plus `Detail: context_docs/<slug>.md`
   - Create `context_docs/<slug>.md` with `Status: discovery` (template
     in the get-context skill)
   Facts from PRD/app only — never invented.
4. **After automation lands**, enrich the **same** context doc
   (`Status: partially-automated` or `automated`; Coverage; confirmed
   locator/session notes). Do not create a second file for the same slug.
5. **Check "Cross-feature relationships" above.** If the feature creates,
   edits, or deletes a listed entity, update that row and cover
   cascade/block/orphan in the test cases — not just the happy path.
6. Read the real component source for that screen in the app repo —
   never guess selectors. Check "Locator strategy notes" first.
7. **If the new feature's test stays `@pytest.mark.ignore`d**, add it to
   `README.md` → "Next steps" in the same turn.
