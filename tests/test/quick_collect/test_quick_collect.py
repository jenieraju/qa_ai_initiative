"""End-to-end Quick Collect tests.

Live flow (confirmed against https://web.dev.cofee.life on 2026-08-31):

  Authenticated session → /quick-collect/create-link
      → Fee Amount (2–200000) + Notes
      → [x] Do not send payment link to payers      (relabels CTA Send → Create)
      → select a payer from the members list
      → Create → confirm dialog → /quick-collect/success
      → "Payment link created successfully!"

Notifications are suppressed in every test on purpose: the dev members list
holds a real phone number, and the payment order is created either way. See
context_docs/quick-collect.md → "Notes".

Session reuse: same pattern as Groups — prefer cookies from .auth/default.json
via @pytest.mark.auth_profile("default"), falling back to a real UI login via
user_ensures_logged_in().

Requires FEATURE_QUICK_COLLECT_PAYER_NAME (an existing member on the target
org) in .env.<env>; the suite skips with a clear message when it is unset.

No teardown: created payment orders are left behind. The app's API reference
documents a "Cancel a Payment Order" operation but its REST path is
unconfirmed — see context_docs/quick-collect.md → "Cross-feature impact".
"""

import allure
import pytest

from dataprovider.dp_quick_collect import (
    get_quick_collect_boundary_amount_test_data,
    get_quick_collect_create_test_data,
    get_quick_collect_invalid_amount_test_data,
)
from src.constants.routes import QUICK_COLLECT_SUCCESS_PATH
from src.core.assert_helper import assert_url_contains
from src.core.auth_storage import DEFAULT_AUTH_PROFILE
from src.core.settings import get_settings
from src.steps import quick_collect_steps
from src.steps.login_steps import user_ensures_logged_in
from tests.parallel_groups import PARALLEL_GROUP_QUICK_COLLECT

pytestmark = [
    pytest.mark.xdist_group(PARALLEL_GROUP_QUICK_COLLECT),
    pytest.mark.auth_profile(DEFAULT_AUTH_PROFILE),
]

NOTE = "QA automation smoke"


@pytest.fixture
def payer_name() -> str:
    """An existing member on the target org, to act as the payer."""
    name = get_settings().feature_quick_collect_payer_name
    if not name:
        pytest.skip(
            "FEATURE_QUICK_COLLECT_PAYER_NAME is not set — point it at an "
            "existing member on the target org (see .env.example)."
        )
    return name


@pytest.fixture
def on_quick_collect_page(page, payer_name):
    """Logged in and sitting on a fresh create-link form."""
    user_ensures_logged_in(page, DEFAULT_AUTH_PROFILE)
    quick_collect_steps.user_navigates_to_quick_collect_page(page)
    quick_collect_steps.user_verifies_quick_collect_page_is_displayed(page)
    return page


@allure.epic("Quick Collect")
@allure.suite("Quick Collect")
@allure.feature("Payment link creation")
class TestQuickCollectCreateLink:
    """Create a one-off payment link from the Quick Collect screen."""

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p0
    @allure.story("Create payment link — single payer")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("amount", get_quick_collect_create_test_data())
    def test_create_payment_link_for_single_payer(self, on_quick_collect_page, payer_name, amount):
        """TC-QC-001/002: a payment link is created and the amount is echoed back."""
        page = on_quick_collect_page
        allure.dynamic.title(f"Create Quick Collect link: ₹{amount}")

        quick_collect_steps.user_creates_quick_collect_link(page, payer_name, amount, NOTE)

        quick_collect_steps.user_verifies_payment_link_created(page)
        quick_collect_steps.user_verifies_success_shows_amount(page, amount)
        assert_url_contains(page, QUICK_COLLECT_SUCCESS_PATH)

        allure.attach(page.url, name="post-create-url", attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p1
    @allure.story("Suppressing notifications relabels the CTA")
    @allure.severity(allure.severity_level.NORMAL)
    def test_suppressing_notifications_relabels_cta(self, on_quick_collect_page):
        """TC-QC-003: the CTA is 'Send' until notifications are suppressed, then 'Create'."""
        page = on_quick_collect_page

        quick_collect_steps.user_verifies_cta_is_send(page)
        quick_collect_steps.user_suppresses_payer_notifications(page)
        quick_collect_steps.user_verifies_cta_is_create(page)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p1
    @allure.story("Amount validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("amount", get_quick_collect_invalid_amount_test_data())
    def test_amount_outside_allowed_range_is_rejected(
        self, on_quick_collect_page, payer_name, amount
    ):
        """TC-QC-004/005: an otherwise-complete form is not submittable outside 2–200000.

        The screen shows no error text for a bad amount — the 2–200000 line is
        static helper text that never turns red. The only signal is the CTA
        staying disabled, so that is what this asserts.
        """
        page = on_quick_collect_page
        allure.dynamic.title(f"Reject out-of-range amount: {amount}")

        quick_collect_steps.user_enters_amount_and_note(page, amount, NOTE)
        quick_collect_steps.user_suppresses_payer_notifications(page)
        quick_collect_steps.user_selects_payer(page, payer_name)

        quick_collect_steps.user_verifies_amount_range_hint(page)
        quick_collect_steps.user_verifies_submission_is_blocked(page)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p2
    @allure.story("Amount validation")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("amount", get_quick_collect_boundary_amount_test_data())
    def test_amount_at_allowed_boundaries_is_accepted(
        self, on_quick_collect_page, payer_name, amount
    ):
        """TC-QC-006: both inclusive bounds leave the form submittable.

        Stops short of submitting — proving the bound is accepted does not
        require creating two more payment orders per run.
        """
        page = on_quick_collect_page
        allure.dynamic.title(f"Accept boundary amount: {amount}")

        quick_collect_steps.user_enters_amount_and_note(page, amount, NOTE)
        quick_collect_steps.user_suppresses_payer_notifications(page)
        quick_collect_steps.user_selects_payer(page, payer_name)

        quick_collect_steps.user_verifies_submission_is_allowed(page)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p1
    @allure.story("Submission guards")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_payer_selected_blocks_submission(self, on_quick_collect_page):
        """TC-QC-007: a valid amount and note are not enough — a payer is required."""
        page = on_quick_collect_page

        quick_collect_steps.user_enters_amount_and_note(page, "100", NOTE)
        quick_collect_steps.user_suppresses_payer_notifications(page)

        quick_collect_steps.user_verifies_submission_is_blocked(page)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p1
    @allure.story("Submission guards")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_note_blocks_submission(self, on_quick_collect_page, payer_name):
        """TC-QC-009: Notes is a required field."""
        page = on_quick_collect_page

        quick_collect_steps.user_enters_amount(page, "100")
        quick_collect_steps.user_suppresses_payer_notifications(page)
        quick_collect_steps.user_selects_payer(page, payer_name)

        quick_collect_steps.user_verifies_submission_is_blocked(page)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p1
    @allure.story("Cancelling creation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cancelling_the_confirm_dialog_creates_nothing(self, on_quick_collect_page, payer_name):
        """TC-QC-008: Cancel dismisses the dialog and stays on the form."""
        page = on_quick_collect_page

        quick_collect_steps.user_enters_amount_and_note(page, "100", NOTE)
        quick_collect_steps.user_suppresses_payer_notifications(page)
        quick_collect_steps.user_selects_payer(page, payer_name)
        quick_collect_steps.user_submits_payment_link(page)
        quick_collect_steps.user_verifies_confirmation_dialog_is_displayed(page)

        quick_collect_steps.user_cancels_payment_link_creation(page)

        quick_collect_steps.user_verifies_confirmation_dialog_is_dismissed(page)
        quick_collect_steps.user_verifies_quick_collect_page_is_displayed(page)

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p2
    @allure.story("Payer search")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_filters_the_payer_list(self, on_quick_collect_page, payer_name):
        """TC-QC-010: searching by name keeps the matching payer listed."""
        page = on_quick_collect_page

        quick_collect_steps.user_searches_for_payer(page, payer_name)

        quick_collect_steps.user_verifies_payer_is_listed(page, payer_name)


@allure.epic("Quick Collect")
@allure.suite("Quick Collect")
@allure.feature("Payment link creation")
class TestQuickCollectSuccessNavigation:
    """Navigation out of the success screen."""

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p2
    @allure.story("Success page navigation")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_new_link_returns_to_an_empty_form(self, on_quick_collect_page, payer_name):
        """TC-QC-011: 'Create New Link' goes back to a usable create-link form."""
        page = on_quick_collect_page

        quick_collect_steps.user_creates_quick_collect_link(page, payer_name, "100", NOTE)
        quick_collect_steps.user_verifies_payment_link_created(page)

        quick_collect_steps.user_clicks_create_new_link(page)

        quick_collect_steps.user_verifies_quick_collect_page_is_displayed(page)
