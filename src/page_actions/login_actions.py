"""Login page actions — business logic and interactions."""

from playwright.sync_api import Page

from src.constants.messages import (
    MSG_INVALID_OTP,
    SECTION_TITLE_LOGIN,
    SECTION_TITLE_OTP_VERIFICATION,
    TITLE_LOGIN,
    TITLE_OTP_VERIFICATION,
)
from src.core.assert_helper import (
    assert_element_has_text,
    assert_element_visible,
    assert_page_title,
)
from src.core.page_actions import PageActions
from src.page_objects.login_po import LoginPage


class LoginPageActions(PageActions):
    """Actions for the login + OTP verification screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = LoginPage(page)

    def navigate_to_login_page(self) -> None:
        self.po.goto("/login")

    def verify_login_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_LOGIN)
        assert_page_title(self.page, TITLE_LOGIN)

    def enter_mobile_number(self, mobile_number: str) -> None:
        self.fill(self.po.input_mobile_number, mobile_number)

    def accept_terms(self) -> None:
        # force=True: the checkbox's decorative check-icon overlay (absolutely
        # positioned sibling <svg>) intercepts pointer events on the real input.
        self.click(self.po.chk_agree_terms, force=True)

    def click_continue(self) -> None:
        self.click(self.po.btn_continue)

    def submit_mobile_number(self, mobile_number: str) -> None:
        self.enter_mobile_number(mobile_number)
        self.accept_terms()
        self.click_continue()

    def verify_otp_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_OTP_VERIFICATION)
        assert_page_title(self.page, TITLE_OTP_VERIFICATION)

    def enter_otp(self, otp: str) -> None:
        for index, digit in enumerate(otp):
            self.fill(self.po.input_otp_boxes.nth(index), digit)

    def submit_otp(self, otp: str) -> None:
        self.enter_otp(otp)
        self.click_continue()

    def login_with_mobile_and_otp(self, mobile_number: str, otp: str) -> None:
        self.submit_mobile_number(mobile_number)
        self.verify_otp_page_visible()
        self.submit_otp(otp)

    def verify_invalid_mobile_number_error(self, message: str) -> None:
        assert_element_has_text(self.po.msg_input_error, message)

    def verify_invalid_otp_error(self) -> None:
        assert_element_visible(self.po.msg_otp_invalid)
        assert_element_has_text(self.po.msg_otp_invalid, MSG_INVALID_OTP)
