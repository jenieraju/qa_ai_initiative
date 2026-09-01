---
name: extend-feature-automation
description: >-
  Adds the next step to existing automation (PO methods, steps, tests). Use when
  a feature is partially automated. Do NOT use for brand-new features — use
  scaffold-feature-automation instead.
---

# Extend Feature Automation

Prerequisites: `get-context` updated + `discover-locators-from-ui` appended locators.
Extend PO → actions → steps → test. Update context **Coverage**; hand off to
`run-and-verify-tests` for **Status**.

## Done when

- [ ] Layers extended; lint + collect pass; verify invoked
