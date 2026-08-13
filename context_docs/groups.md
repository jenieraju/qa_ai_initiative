# Groups

Status: automated

## Summary

Create a group from the authenticated groups list. High-level sketch:
`APP_CONTEXT.md` → "Groups".

## Flow

```
Authenticated session → /groups → New Group → /groups/create
    → name + payment-collection interval (monthly/weekly/by-terms) + amount
    → Save and next → "Group created successfully" → group appears on /groups
```

## Coverage

- Already automated: `src/page_objects/{groups,group_create}_po.py`,
  `tests/test/groups/test_group_create.py`
- Not yet covered: editing, member assignment, further wizard steps,
  delete-group

## Cross-feature impact

Group is depended on by payment links (interval/amount) and member rosters —
see `APP_CONTEXT.md` → Cross-feature relationships. Delete/edit cascade
behavior still unconfirmed (no delete-group API yet).

## Notes

- Session reuse: cookies from `.auth/{profile}.json` via
  `@pytest.mark.auth_profile`; fall back to `user_ensures_logged_in()` if
  missing/expired.
- No teardown yet: confirm a delete-group API before wiring
  `teardown_registry`.
