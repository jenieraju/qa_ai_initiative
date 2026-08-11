---
name: setup-project
description: The entry point for a brand-new target project that wants to use this suite. Asks whether the project needs API automation, UI automation, or both, then tells the human exactly which skill folders and agent template(s) to copy into the target repo's `.claude/` and which config files to fill in — it never copies files itself, never invents a skill that doesn't exist yet, and never generates any test code. Use once, before any other skill, when a target project has no `.claude/skills/` or `.claude/agents/` from this suite yet.
---

# Setup Project

The first thing to run against a brand-new target project. This skill doesn't build a framework or generate anything — it just resolves one question ("which automation type(s) does this project need?") and turns the answer into a concrete, ordered checklist of what to copy from this template repo and what to fill in, so the human doesn't have to reverse-engineer the README's copy commands themselves or guess which of the two agent templates applies.

## When to use

- A target project has never used this suite before (no `.claude/skills/<name>/SKILL.md` or `.claude/agents/*-automation-agent.md` from this repo yet).
- Someone asks "how do I set this up for my project?" or "I need both API and UI tests for this app."
- Re-run it later if the same project wants to add the automation type it didn't pick the first time (e.g. API now, UI in a future session) — it's not a one-time-only gate.

## Guardrails

These are hard constraints, not style preferences. If a step below seems to conflict with one of these, the guardrail wins.

- **Never copy files itself.** This skill produces a checklist of `cp`/`git mv`-style instructions for the human to run (or approve running) — it doesn't reach into the target repo and place files unprompted, since that's a repo-structure change in someone else's project.
- **Never invent a skill that doesn't exist yet.** Check `skills/api/` and `skills/ui/` (and `skills/ui/README.md` for what's still pending) before recommending anything — never tell the human to copy `skills/ui/ui-test-design` if that folder doesn't exist on disk yet. If the human asks for UI automation before the UI skills are written, say so plainly and point at `skills/ui/README.md`'s list instead of fabricating a folder to copy.
- **One shared config, never duplicated.** Always direct the human to `agents/shared-project-config.md` for project-identity fields (name, repo, team/owner, doc locations) regardless of which automation type(s) they pick — never tell them to fill those fields into `api-automation-agent.md` or `ui-automation-agent.md` directly, since that's exactly the duplication those files were split to avoid.
- **No fabrication about project specifics.** This skill doesn't know the target project's API base URL, UI framework, or auth type — it only tells the human *which* placeholders exist to fill in, never guesses plausible-sounding values for them.
- **Idempotent re-runs.** If some pieces are already copied (e.g. API automation was set up last month, now the project wants UI too), detect what's already present and only checklist what's missing — don't tell the human to re-copy or re-fill fields that already exist.
- **Stay inside scope.** Read this repo's `skills/`, `agents/`, and `README.md` to answer the question; don't wander into the target project's unrelated source code.

## Steps

1. **Ask which automation type(s) this project needs.** If not already stated: "Set up API automation, UI automation, or both?" A "both" answer is common when the same target repo has a backend and a frontend to cover.
2. **Check what's actually available to copy.** For API: `skills/api/*` (all 11 exist). For UI: `skills/ui/*` — read `skills/ui/README.md` for current status; some or all UI skills may not be written yet. Never recommend copying a folder that doesn't exist.
3. **Produce the checklist**, scoped to the answer from Step 1:
   - Always: copy `agents/shared-project-config.md` into the target repo's `.claude/agents/`, fill in its placeholders once.
   - If API (or both): copy every folder under `skills/api/` the project wants into `.claude/skills/`, copy `agents/api-automation-agent.md` into `.claude/agents/`, fill in its Project config section.
   - If UI (or both): copy every folder that actually exists under `skills/ui/` into `.claude/skills/`, copy `agents/ui-automation-agent.md` into `.claude/agents/`, fill in its Project config section. If some UI skills are still pending, say so and note the workflow will have gaps until they land.
4. **Point at the next step.** For API: `create-framework-structure` (or straight to `get-context` if a framework already exists). For UI: `create-ui-framework-structure` once it exists, or flag that UI automation can't start yet if it doesn't.
5. **Report and hand off.** Summarize what was recommended for copying, what's still pending (if UI is incomplete), and which config files need a human to fill in placeholders before any other skill runs.

## Output template

This skill's output is a checklist printed in conversation, not a file — nothing under `context/` or `reports/` belongs to it. Shape to follow:

```markdown
## Setup checklist for <target project>

**Automation type(s):** API / UI / both

**Always:**
- [ ] Copy `agents/shared-project-config.md` → `.claude/agents/shared-project-config.md`; fill in Project name, Repo, Team/owner, Doc/artifact locations.

**API automation:** <omit this block if not selected>
- [ ] Copy `skills/api/<name>/` → `.claude/skills/<name>/` for each skill needed (or all 11 for the full workflow).
- [ ] Copy `agents/api-automation-agent.md` → `.claude/agents/api-automation-agent.md`; fill in API base URL(s), auth type, primary language/framework, repo path for generated tests.
- [ ] Next step: `create-framework-structure` (greenfield) or `get-context` (framework already exists).

**UI automation:** <omit this block if not selected>
- [ ] Copy `skills/ui/<name>/` → `.claude/skills/<name>/` for each skill that exists yet (see `skills/ui/README.md` for what's pending).
- [ ] Copy `agents/ui-automation-agent.md` → `.claude/agents/ui-automation-agent.md`; fill in app base URL(s), UI framework/language, auth type (UI layer), repo path for generated tests.
- [ ] Next step: `create-ui-framework-structure` — <"ready" or "not written yet, see skills/ui/README.md">.

## Open questions / follow-ups

- <any UI skills still pending that block part of the workflow, or "none">
```

## Bias to counter

Models tend to (a) recommend copying a UI skill folder that doesn't exist yet because the agent template lists its intended name, (b) tell the human to fill project-identity fields into both agent files instead of the one shared config, or (c) silently skip re-checking what's already copied and recommend redundant work on a project that's only adding a second automation type. Force a real directory check for (a), always point at `shared-project-config.md` for (b), and always check for existing `.claude/skills/`/`.claude/agents/` content for (c) rather than assuming a clean slate.

## Notes for reuse across projects

- Never hardcode a project-specific name, repo, or URL in this skill file itself — it only ever talks about *this template repo's* structure, not any target project's specifics.
- The set of available `skills/ui/*` folders will grow over time as the team fills them in — re-read `skills/ui/README.md` fresh each run rather than trusting a previous run's list of what existed.
- If a target project's `.claude/` already has some pieces from a previous setup-project run, checklist only the delta — don't re-list steps already done.
