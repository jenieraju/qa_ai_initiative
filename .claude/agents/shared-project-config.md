# Shared Project Config

Copied from `agents/shared-project-config.md` on the `ui-automation` branch of
[KeyValueSoftwareSystems/group_b_api_automation](https://github.com/KeyValueSoftwareSystems/group_b_api_automation).
These fields describe the project itself, not any one automation type — every
agent this project uses reads them from here instead of asking again.

- **Project name:** cofee-web (the app under test)
- **Repo:** https://github.com/KeyValueSoftwareSystems/cofee-web
- **Team / owner:** <FILL IN>
- **Doc/artifact locations:** `artifacts/` for PRDs (default, not yet created) — Figma export for the LMS feature supplied directly as a PDF (`LMS.pdf`), not a live Figma link — <FILL IN if there are additional locations, e.g. Jira project key>

## How agent files use this

`ui-automation-agent.md`'s own "Project config" section holds only what's
genuinely specific to UI automation (app base URL, auth type, framework/
language, repo path for generated tests) and opens with a one-line pointer
back here for the fields above.
