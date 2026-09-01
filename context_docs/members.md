# Members

Status: discovery

## Summary

Add and list members for a branch. High-level sketch: `APP_CONTEXT.md` → "Members".

## Flow

```
[Unconfirmed — run discover-locators-from-ui against live Members tab]
Authenticated session → /members → Add Member → …
```

## Coverage

- Placeholder scaffold only: `src/page_objects/{members,member_create}_po.py`,
  `tests/test/members/test_member_create.py` — `@pytest.mark.ignore`
- Not yet covered: any confirmed flow

## Cross-feature impact

Member is depended on by group rosters, payment links, attendance, team roles —
see `APP_CONTEXT.md` → Cross-feature relationships.

## Confirmed locators

**None confirmed.** Placeholder locators in PO files were guessed — do not
remove `@pytest.mark.ignore` until this section is filled via
`discover-locators-from-ui`.

| UI element | Strategy | PO attribute | Value |
|------------|----------|--------------|-------|
| — | — | — | Run discover-locators-from-ui |

Routes confirmed: none

Unconfirmed: `/members` path, Add Member (modal vs route), required fields

## Notes

- Run `discover-locators-from-ui` before any scaffold rewrite of member POs.
- Confirm delete-member API before wiring `teardown_registry`.
