---
name: create-feature-branch
description: >-
  Creates the git feature branch a new automation task runs on, before any
  context-gathering or test-case work starts. Use when kicking off automation
  for a new feature/PRD/Jira ticket and no feature branch exists yet. Do NOT
  use for hotfixes on an already-checked-out branch, or when the user is
  already working on the right feature branch.
---

# Create Feature Branch

First step of the new-feature pipeline: `create-feature-branch` → `get-context`
→ `generate-test-cases` → `map-test-cases-to-automation` →
`scaffold-feature-automation`. Everything downstream reuses the slug decided
here — for the `APP_CONTEXT.md` section heading, the `context_docs/<slug>.md`
filename (created at get-context, enriched after automation), the branch
name, and the `pytest.ini` feature marker.

## 1. Derive the slug

From the feature name or Jira key, e.g. "Custom user role" → `custom-user-role`.
Confirm the slug with the user before creating anything if it's ambiguous.

## 2. Checklist

```
- [ ] git status — clean? if dirty, stop and ask the user to commit/stash first
- [ ] confirm current branch; if not main, ask before switching off it
- [ ] git fetch origin
- [ ] git pull --ff-only origin main  (only after the tree is confirmed clean)
- [ ] check feature/<slug> doesn't already exist locally or on origin — if it
      does, stop and ask (checkout existing vs. pick a different slug),
      never overwrite
- [ ] git checkout -b feature/<slug>
```

Branch naming follows this repo's existing convention (no ticket-id prefix):
`feature/onboarding-ui-automation`, `feature/reporting-framework`,
`feature/test-data-teardown` are real examples from `origin`.

## 3. Never

- Never push the new branch automatically.
- Never `git reset --hard`, force-checkout, or discard uncommitted changes to
  make room for the new branch — stop and ask instead.

## Done when

- [ ] Working tree is on `feature/<slug>`, branched from an up-to-date `main`
- [ ] Nothing was pushed, nothing uncommitted was discarded
- [ ] Reported to the user: "Branch `feature/<slug>` ready — next: get-context
      for `<slug>`."

## Self-check

Triggers: "let's automate the custom user role feature", "start a new branch
for the disable-payment-link PRD", "kick off automation for JIRA-1234".
Does not trigger: "fix the flaky login test on this branch" (already on a
branch, no new feature), "commit my changes" (not branch creation).
