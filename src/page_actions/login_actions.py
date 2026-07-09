"""Login page actions — business logic and interactions."""

from playwright.sync_api import Page

from src.core.assert_helper import assert_element_visible
from src.core.page_actions import PageActions
from src.page_objects.login_po import LoginPage


class LoginPageActions(PageActions):
    """Actions for the login page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = LoginPage(page)

    def navigate_to_login_page(self) -> None:
        self.po.goto("/login")

    def verify_login_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_page_title)

    def enter_email(self, email: str) -> None:
        self.fill(self.po.input_email, email)

    def enter_password(self, password: str) -> None:
        self.fill(self.po.input_password, password)

    def click_login_button(self) -> None:
        self.click(self.po.btn_login)

    def login_with_credentials(self, email: str, password: str) -> None:
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def verify_error_message_visible(self, message: str) -> None:
        assert_element_visible(self.po._loc_error_message(message))

    def verify_login_form_visible(self) -> None:
        self.verify_login_page_visible()
        assert_element_visible(self.po.input_email)
        assert_element_visible(self.po.input_password)
        assert_element_visible(self.po.btn_login)
