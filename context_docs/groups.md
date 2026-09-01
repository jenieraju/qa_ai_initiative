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

## Confirmed locators

Source: live UI @ web.dev.cofee.life (automated suite green)
See `src/page_objects/{groups,group_create}_po.py` for full PO mapping.

| UI element | Strategy | PO attribute | Value |
|------------|----------|--------------|-------|
| New Group button | role+name | `btn_new_group` | `get_by_button("New Group")` |
| Group name field | placeholder/label | `input_group_name` | confirmed in `group_create_po.py` |
| Save and next | role+name | `btn_save_and_next` | confirmed in `group_create_po.py` |

Routes confirmed: `/groups`, `/groups/create`

## Notes

- Session reuse: cookies from `.auth/{profile}.json` via
  `@pytest.mark.auth_profile`; fall back to `user_ensures_logged_in()` if
  missing/expired.
- No teardown yet: confirm a delete-group API before wiring
  `teardown_registry`.
