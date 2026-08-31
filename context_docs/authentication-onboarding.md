# Authentication & onboarding

Status: partially-automated (individual onboarding is BROKEN by app drift — see Notes)

## Summary

Login and first-time onboarding for cofee-web. High-level sketch:
`APP_CONTEXT.md` → "Authentication & onboarding flow".

## Flow

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

## Coverage

- Already automated: `src/page_objects/{login,onboarding,document_upload,payment_selection}_po.py`,
  `tests/test/auth/{test_login,test_onboarding}.py`
- Not yet covered: referral-code path (unreachable in product today)
- **Currently failing**: `test_individual_onboarding` — app drift, see Notes.

## Cross-feature impact

Creates org/user with no delete API — no teardown possible today.

## Notes

- **App drift, found 2026-08-31: individual onboarding gained a
  `/select-category` step.** `test_individual_onboarding` asserts it lands on
  `/groups` after account selection; the app now routes to `/select-category`,
  so the test fails at that assertion. The app's auth route map also lists a
  `/create-branch` step this suite has never seen. Both are recorded in
  `src/constants/routes.py` as `SELECT_CATEGORY_PATH` / `CREATE_BRANCH_PATH`.
  Nothing is known yet about either screen's fields or required data — that
  needs a `discover-locators-from-ui` pass against a fresh mobile number
  before the test can be repaired. Unrelated to the login landing-route fix
  made the same day (the onboarding test files were untouched by it).
- Post-login landing route is **account- and role-dependent**: an org Owner
  lands on `/dashboard`, other accounts on `/groups`. Neither the login test
  nor `user_ensures_logged_in()` may assert a specific landing route — they
  assert only that `/login` was left behind.
- Referral-code screen exists in app source but is **currently unreachable** —
  gating defaults to already-passed. Flows skip OTP → account-selection.
- Onboarding is a **one-time, irreversible transition per identity**. Every
  new onboarding test needs a mobile number with **zero existing
  organizations**.
- No teardown: no delete API for the org/user this flow creates
  (see `AGENTS.md` → Teardown).
