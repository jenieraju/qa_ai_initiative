# Authentication & onboarding

Status: automated

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

## Cross-feature impact

Creates org/user with no delete API — no teardown possible today.

## Notes

- Referral-code screen exists in app source but is **currently unreachable** —
  gating defaults to already-passed. Flows skip OTP → account-selection.
- Onboarding is a **one-time, irreversible transition per identity**. Every
  new onboarding test needs a mobile number with **zero existing
  organizations**.
- No teardown: no delete API for the org/user this flow creates
  (see `AGENTS.md` → Teardown).
