---
name: scaffold-feature-automation
description: >-
  Scaffolds all four POM layers plus dataprovider and test file for a new UI
  feature. Use when adding automation for a new page, flow, or feature area, or
  when asked to "scaffold"/"set up the layers for" a feature. Do NOT use before
  locators are confirmed (run discover-locators-from-ui first) or before context
  exists (get-context), and do NOT use to add a case to a feature that already
  has all four layers — edit those files directly.
---

# Scaffold Feature Automation

Read [AGENTS.md](../../../AGENTS.md) first — this skill is a checklist, not a
replacement. Assumes a feature branch exists (`create-feature-branch`); never
scaffold on `main`.

**Required first step:** follow `get-context` —
[APP_CONTEXT.md](../../../APP_CONTEXT.md) then `context_docs/<slug>.md`. If
either is missing, create the short index section + discovery context doc now.

**Required last step:** enrich the **same** `context_docs/<slug>.md`
(Coverage, confirmed locator/session notes, `Status:`) and keep
`Detail: context_docs/<slug>.md` on the `APP_CONTEXT.md` section.

## Inputs needed

Feature name, route path(s), confirmed locators (from
`discover-locators-from-ui` — never invent selectors), priority
(`p0`/`p1`/`p2`), and the feature marker name.

## Checklist

```
- [ ] src/page_objects/{feature}_po.py
- [ ] src/page_actions/{feature}_actions.py
- [ ] src/steps/{feature}_steps.py
- [ ] tests/dataprovider/dp_{feature}.py
- [ ] tests/test/{area}/test_{feature}.py
- [ ] pytest.ini marker (if new feature tag) — **and** a matching `## {Feature}`
      heading in `APP_CONTEXT.md`, or `tests/test/core/test_app_context_sync.py`
      fails
- [ ] invoke lint
- [ ] pytest --collect-only passes
```

## File order (create bottom-up: PO → actions → steps → test)

### 1. Page object — locators only

Copy the shape of `src/page_objects/login_po.py`:
`class {Feature}Page(BasePage)`, every locator assigned in `__init__` under a
`# --- Locators ---` comment, dynamic ones as `loc_*()` methods returning a
`Locator`.

Only `BasePage` helpers, never `page.locator()` — helper priority order and the
`btn_`/`input_`/`msg_`/`lbl_` prefixes live in `discover-locators-from-ui`.

### 2. Page actions — interactions + assertions

Mirror `src/page_actions/login_actions.py`. Screen-level assertions live
**here** via `src/core/assert_helper.py` — see `verify_login_page_visible`.

```python
# src/page_actions/{feature}_actions.py
from playwright.sync_api import Page

from src.constants.messages import SECTION_TITLE_{FEATURE}
from src.core.assert_helper import assert_element_has_text
from src.core.page_actions import PageActions
from src.page_objects.{feature}_po import {Feature}Page


class {Feature}PageActions(PageActions):
    """Actions for the {feature} screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = {Feature}Page(page)

    def navigate_to_{feature}_page(self) -> None:
        self.po.goto("/{route}")

    def verify_{feature}_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_{FEATURE})
```

Constants (`SECTION_TITLE_*`, messages) go in `src/constants/messages.py`;
routes in `src/constants/routes.py`.

### 3. Steps — `@allure.step` user actions

Module-level functions taking `page: Page`, not a class. Mirror
`src/steps/login_steps.py`.

```python
# src/steps/{feature}_steps.py
import allure
from playwright.sync_api import Page

from src.page_actions.{feature}_actions import {Feature}PageActions


@allure.step("User navigates to {feature} page")
def user_navigates_to_{feature}_page(page: Page) -> None:
    {Feature}PageActions(page).navigate_to_{feature}_page()
```

### 4. Dataprovider

`tests/dataprovider/dp_{feature}.py` → `get_{feature}_test_data()`. Rows, ids,
marks, the import path, and the no-secrets / no-env-entity rules:
`create-dataprovider`.

### 5. Test — class-based, mirror `tests/test/auth/test_login.py`

```python
# tests/test/{area}/test_{feature}.py
"""End-to-end {feature} tests."""

import allure
import pytest

from dataprovider.dp_{feature} import get_{feature}_test_data
from src.steps.{feature}_steps import user_navigates_to_{feature}_page
from tests.parallel_groups import PARALLEL_GROUP_{NAME}  # add the constant there first

pytestmark = pytest.mark.xdist_group(PARALLEL_GROUP_{NAME})


@allure.epic("{Epic}")
@allure.suite("{Feature}")
@allure.feature("{Feature}")
class Test{Feature}:
    """{Feature} flow end-to-end tests."""

    @pytest.mark.e2e
    @pytest.mark.{feature}
    @pytest.mark.p1
    @allure.story("{Story}")
    @pytest.mark.parametrize("scenario", get_{feature}_test_data())
    def test_{feature}(self, page, scenario):
        """Verify {feature} behaviour per scenario."""
        allure.dynamic.title(f"{Feature} scenario: {scenario}")
        user_navigates_to_{feature}_page(page)
```

Needs an authenticated session? Add `@pytest.mark.auth_profile("default")` —
see `auth-storage-state-setup`.

**Parallel groups:** the `pytestmark` above is only needed if the suite shares
org/branch/mutable state. Add a constant to `tests/parallel_groups.py`
(see `tests/parallel_groups.py` for the current constants) and run with
`invoke test --env dev --parallel 2` — `--parallel` supplies `--dist
loadgroup`, which is what makes `xdist_group` effective. Otherwise drop both
the import and the `pytestmark` line.

## Verify — expect the first run to fail, and read why

```bash
invoke lint
pytest --collect-only --env dev -m "{feature}"      # imports, params, markers
pytest --env dev -m "{feature}" -k <one_test>       # one test first, not the suite
pytest --env dev -m "{feature}"                     # then the suite
pytest --env dev -m "{feature}" -n 2 --dist loadgroup
```

Scaffolding is not done when it collects — it is done when it passes twice and
survives parallel. Run one test before the suite: a shared-setup mistake fails
every test identically and buries the real cause in noise.

**A green first run on new code deserves suspicion**, not celebration. Check
each new assertion can actually fail — flip the expected value, or point it at a
value you know is wrong, and confirm it goes red. An assertion on an
always-present element (see `discover-locators-from-ui` → "Trap") passes against
a completely broken app.

Failures leave `output/traces/<nodeid>.zip` — open it with
`playwright show-trace` before editing the test.

## Actions with real-world side effects

Some flows **message a real person** (payment requests, invites, reminders) or
move money — a dev members list can hold a colleague's real mobile.

- **Use the app's own suppression control** — Quick Collect's "Do not send
  payment link to payers" still creates the order: coverage unaffected, nobody
  contacted. Default for automation; if none exists, stop and ask.
- **Expect the UI to change when suppressed** — Quick Collect relabels its CTA
  "Send" → "Create"; model both labels as separate locators.
- **Say so in the test docstring and context doc.**

## Done when

- [ ] All five files exist at the exact checklist paths; layers not skipped
- [ ] No `page.locator()` / `page.get_by_*` outside a `BasePage` helper
- [ ] Test sits inside a `Test{Feature}` class (no bare `self`)
- [ ] Dataprovider imported as `from dataprovider.dp_{feature} import ...`
- [ ] New marker in `pytest.ini` **and** a matching `APP_CONTEXT.md` heading
- [ ] `invoke lint` passes; `pytest --collect-only -m "{feature}"` collects it
- [ ] `context_docs/<slug>.md` enriched; if shipped `@pytest.mark.ignore`d,
      added to `README.md` → "Next steps"

## Self-check

Triggers: "scaffold automation for the payment-link feature", "set up the four
layers for the branch admin screen", "add automation for the new Members tab".
Does not trigger: "add one more negative case to the login dataprovider"
(edit `dp_login.py`), "find the locators for this screen first"
(`discover-locators-from-ui`).
