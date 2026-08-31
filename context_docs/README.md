# context_docs

Living per-feature records for cofee-web automation.

`APP_CONTEXT.md` is the always-on **index** (domain, features table,
cross-feature links, short sketches). This folder holds the **detail** each
feature needs for test design and later steps.

| When | What to do |
|------|------------|
| New flow (`get-context`) | Create `context_docs/<slug>.md` with `Status: discovery`. Add a short `##` + `Detail:` link in `APP_CONTEXT.md`. |
| Generate test cases / scaffold | Read that file — do not re-derive. |
| Automation lands | Enrich the **same** file; set `Status: partially-automated` or `automated`. |
| Next step of same feature | Read + update the same file. Never a second doc for the same slug. |

Filename = `create-feature-branch` slug (`feature/<slug>` → `<slug>.md`).
Aliases: `login` / `onboarding` → `authentication-onboarding.md`.

See `.claude/skills/get-context/SKILL.md` for the template and rules.
