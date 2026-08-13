---
name: scaffold-feature-automation
description: >-
  Scaffolds all four POM layers plus dataprovider and test file for a new UI
  feature. Use when adding automation for a new page, flow, or feature area.
---

# Scaffold Feature Automation

Read [AGENTS.md](../../AGENTS.md) first — this skill is a checklist, not a replacement.

Assumes a feature branch is already checked out (see `create-feature-branch`)
— don't scaffold new feature files directly on `main`.

**Required first step, before the checklist below:** follow `get-context`.
Read [APP_CONTEXT.md](../../../APP_CONTEXT.md), then
`context_docs/<slug>.md`. Don't scaffold an undocumented feature — if
either is missing, create the short index section + discovery context doc
now (see `get-context`).

**Required last step, after the checklist:** enrich the **same**
`context_docs/<slug>.md` (Coverage, confirmed locators/session notes;
`Status: partially-automated` or `automated`) and ensure
`Detail: context_docs/<slug>.md` is on the `APP_CONTEXT.md` section. If
the scaffolded test ships `@pytest.mark.ignore`d, also add it to
`README.md` → "Next steps" — same turn.

## Inputs needed

- Feature name (e.g. `login`, `checkout`)
- Route path(s)
- Real locators (from `discover-locators-from-ui` — never invent selectors)
- Priority (`p0`/`p1`/`p2`) and feature marker name

## Checklist

```
- [ ] src/page_objects/{feature}_po.py
- [ ] src/page_actions/{feature}_actions.py
- [ ] src/steps/{feature}_steps.py
- [ ] tests/dataprovider/dp_{feature}.py
- [ ] tests/test/{area}/test_{feature}.py
- [ ] pytest.ini marker (if new feature tag)
- [ ] invoke lint
- [ ] pytest --collect-only passes
```

## File order (create bottom-up: PO → actions → steps → test)

### 1. Page object — locators only

```python
# src/page_objects/{feature}_po.py
from playwright.sync_api import Locator
from src.core.base_page import BasePage

class {Feature}Page(BasePage):
    """Page object for {feature} screen."""

    def __init__(self, page) -> None:
        super().__init__(page)
        # --- Locators ---
        self.input_email = self.get_by_data_test_id("...")
```

### 2. Page actions — interactions

```python
# src/page_actions/{feature}_actions.py
from src.core.page_actions import PageActions
from src.page_objects.{feature}_po import {Feature}Page

class {Feature}PageActions(PageActions):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.po = {Feature}Page(page)
```

### 3. Steps — `@allure.step` user actions

```python
# src/steps/{feature}_steps.py
import allure
from src.page_actions.{feature}_actions import {Feature}PageActions

@allure.step("User navigates to {feature} page")
def user_navigates_to_{feature}_page(page) -> None:
    {Feature}PageActions(page).navigate_to_page()
```

### 4. Dataprovider

```python
# tests/dataprovider/dp_{feature}.py
import pytest

def get_{feature}_test_data() -> list:
    return [pytest.param("case_a", id="case_a")]
```

### 5. Test

```python
# tests/test/{area}/test_{feature}.py
@pytest.mark.e2e
@pytest.mark.{feature}
@pytest.mark.p1
@pytest.mark.parametrize("scenario", get_{feature}_test_data())
def test_{feature}(self, page, scenario):
    ...
```

## Parallel groups

If the suite shares org/branch/mutable state:

```python
from tests.parallel_groups import PARALLEL_GROUP_{NAME}
pytestmark = pytest.mark.xdist_group(PARALLEL_GROUP_{NAME})
```

## Verify

```bash
invoke lint
pytest --collect-only --env dev -m "{feature}"
```
