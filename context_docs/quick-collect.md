# Quick Collect

Status: partially-automated

## Summary

One-off payment collection: pick an amount + note, choose payers, and the app
creates a payment order (payment link) per payer. Unlike group collection there
is no recurring interval and no group membership required — the domain model
calls this the `once` frequency.

Sidebar entry "Quick Collect" is gated on permission `PAYMENT_ORDER_CREATE`;
without it the page renders "You don't have permission to add payers for Quick
Collect." Payment collection also requires completed KYC — a PAN/GSTIN-less org
sees "To enable payment collection, please provide your PAN or GSTIN" instead of
the form.

Confirmed against the live app (`web.dev.cofee.life`, bundle `main.887a1bd7.js`
plus chunks `6049` / `2110`) on 2026-08-31, logged in as an Owner.

## Flow

```
Authenticated session → /quick-collect/create-link
    ├─ "Enter amount" section
    │     Fee Amount*  (₹, placeholder "Enter Amount", allowed 2–200000)
    │     Notes*       (placeholder "Eg: Admission fee for Batch 7")
    │     [ ] Do not send payment link to payers      ← relabels the CTA
    │
    ├─ "Add Payers" section — tab(s) depend on org/context:
    │     "Add from members list"  (the only tab on the dev Owner account)
    │     "Add from group" / "Import file" / "Add manually"  ← conditional,
    │        not rendered for this account [Unknown — what enables them]
    │     search "Search by name"; click a member row to select it
    │        ("Selected" counter increments)
    │
    └─ CTA (top right):  "Send"    when payers WILL be notified
                         "Create"  when "Do not send…" is checked
           → confirm dialog "Are you sure you want to create the payment link?"
             [Cancel] [Confirm]
           → /quick-collect/success
                data-testid="quick_collect_success_text"
                  = "Payment link created successfully!"   (suppressed)
                  = "Payment link sent successfully"       (notified) [Assumption —
                     string exists in the bundle; only the suppressed path was run]
                "Your payment link successfully created for ₹<amount> request"
                [Create New Link] [Go To Home]
```

## Coverage

- Already automated: `tests/test/quick_collect/test_quick_collect.py`
  — 11 tests, green on 3 consecutive runs including `-n 2 --dist loadgroup`.
  Layers: `src/page_objects/quick_collect_po.py`,
  `src/page_actions/quick_collect_actions.py`,
  `src/steps/quick_collect_steps.py`,
  `tests/dataprovider/dp_quick_collect.py`.

  | TC | Covered by |
  |---|---|
  | TC-QC-001/002 | `test_create_payment_link_for_single_payer` |
  | TC-QC-003 | `test_suppressing_notifications_relabels_cta` |
  | TC-QC-004/005 | `test_amount_outside_allowed_range_is_rejected` |
  | TC-QC-006 | `test_amount_at_allowed_boundaries_is_accepted` |
  | TC-QC-007 | `test_no_payer_selected_blocks_submission` |
  | TC-QC-008 | `test_cancelling_the_confirm_dialog_creates_nothing` |
  | TC-QC-009 | `test_empty_note_blocks_submission` |
  | TC-QC-010 | `test_search_filters_the_payer_list` |
  | TC-QC-011 | `test_create_new_link_returns_to_an_empty_form` |

  Not automated and why: TC-QC-014 (no restricted test account),
  TC-QC-015 (dev org already KYC-verified), TC-QC-016 (member-deletion
  cascade unconfirmed), TC-QC-017 (Import tab not rendered),
  TC-QC-018 (dev org has members).
- Not yet covered:
  - The notifying path ("Send"): deliberately not automated — it sends a real
    payment request to a real mobile number. See "Notes".
  - `Add manually` / `Import file` / `Add from group` tabs — not rendered for
    the dev account, so untestable from here.
  - Fee-category split ("Enable Fee category", "Switch Fee Category?").
  - CSV/XLSX import rules that the bundle documents but the UI doesn't expose
    here: max 100 rows, max 2MB, headers `name`/`phoneNumber`/
    `quick_collect_amount`/`quick_collect_note`.
  - "Try demo" mode (`payment-order/demo/send-link`).

## Cross-feature impact

Creates a **payment link / payment order** — a row in `APP_CONTEXT.md`'s
cross-feature table.

- **Members**: payers are selected from the existing members list, so a member
  with an open Quick Collect order is exactly the "member deleted while a
  payment cycle is pending" case that table flags as unconfirmed. A
  `DELETE v1/organisation/{orgId}/branch/{branchId}/member/{memberId}` endpoint
  **does** exist (found in the bundle) — so that cascade is now testable, which
  it previously was not.
- **Teardown**: the create response returns `payment_order_ids`, and the app's
  own API reference documents a *Cancel a Payment Order* operation
  ("cancels a pending payment order",
  `/docs/api-reference/operations/cancel-payment-order`). The REST path and
  method are **[Unknown — needs confirmation]** — the frontend never calls it
  outside the LMS/lead flow, which uses `.../payment-order/{id}/close` and
  `.../payment-order/{id}/disable`. Until confirmed, Quick Collect tests leave
  a cancelled-nothing payment order behind on dev.

## Notes

- **"Allowed amount is between 2 and 200000" is static helper text**, not a
  validation error: it is `text-grey60`, always visible, and never turns red.
  There is no error element for a bad amount — `amountInput_error_message`
  exists in the bundle but never renders on this screen. The *only* signal for
  an invalid amount is the **CTA staying disabled**. A test asserting that the
  range text "appears" passes on every input, valid or not — this suite made
  exactly that mistake first time round and the boundary cases caught it.
- Confirmed by probing the live form: amount `1`, `200001` and empty all leave
  the CTA disabled; `2`, `100` and `200000` all enable it (bounds inclusive).
  An empty Notes field also disables the CTA.
- **Amount bounds are 2–200000** (inclusive language on screen: "Allowed amount
  is between 2 and 200000"). Both Fee Amount and Notes are required (`*`).
- **The CTA label is state-dependent** — "Send" normally, "Create" once "Do not
  send payment link to payers" is checked. A test that hardcodes "Send" breaks
  the moment it suppresses notifications. This is the single most surprising
  thing about the screen.
- **Automation checks "Do not send payment link to payers" on purpose.** The dev
  environment's member list holds a real phone number (+91 94469…); leaving
  notifications on means every suite run fires a real payment request at a real
  person. The checkbox is the app's own supported way to avoid that, and the
  order is still created, so coverage is unaffected.
- Login on this account lands on **`/dashboard`**, not `/groups`. Both
  `user_ensures_logged_in()` and the login test used to assert `/groups` and
  failed for every test in this suite; they now assert only that the login page
  was left behind, since the landing route depends on account and role.
- Locators: this screen has almost no `data-testid` — only
  `quick_collect_success_text` and the `fileUpload_*` set. Amount/notes/search
  are placeholder-only; the CTA and dialog buttons are role+name. Consistent
  with `APP_CONTEXT.md` → "Locator strategy notes".
- The success sentence is split across DOM nodes — the prefix is its own
  `<span>` with the ₹ symbol, amount and "request" as siblings — so an
  amount assertion has to scope to the wrapper, not the prefix span.
- Selecting a payer is a click on the **member row** (a `<button>` whose
  accessible name is the member's name); the row's checkbox is decorative
  enough that clicking the row is the reliable interaction.
- API: `POST v1/organisation/{orgId}/branch/{branchId}/payment-order/instant-link`
  with `member_details[]` of `{name, mobile, country_code, quick_collect_amount,
  quick_collect_note}` plus top-level `amount` / `note` / `group_id`.
