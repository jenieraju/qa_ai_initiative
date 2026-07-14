"""Document-upload page actions — business logic and interactions (organization path)."""

from playwright.sync_api import Page

from src.constants.messages import SECTION_TITLE_DOCUMENT_UPLOAD, TITLE_DOCUMENT_UPLOAD
from src.core.assert_helper import assert_element_has_text, assert_page_title
from src.core.page_actions import PageActions
from src.page_objects.document_upload_po import CERTIFICATE_TYPE_PAN, DocumentUploadPage


class DocumentUploadPageActions(PageActions):
    """Actions for the organization document-upload screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = DocumentUploadPage(page)

    def verify_document_upload_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_DOCUMENT_UPLOAD)
        assert_page_title(self.page, TITLE_DOCUMENT_UPLOAD)

    def select_certificate_type(self, certificate_type: str) -> None:
        locator = (
            self.po.rdo_certificate_pan
            if certificate_type == CERTIFICATE_TYPE_PAN
            else self.po.rdo_certificate_gstin
        )
        self.click(locator)

    def enter_card_number(self, card_number: str) -> None:
        self.fill(self.po.input_card_number, card_number)

    def upload_certificate_file(self, certificate_type: str, file_path: str) -> None:
        self.po._loc_certificate_file_input(certificate_type).set_input_files(file_path)

    def select_business_license_type(self, option_value: str) -> None:
        self.click(self.po.btn_business_license_dropdown)
        self.click(self.po._loc_business_license_option(option_value))

    def upload_business_license_file(self, file_path: str) -> None:
        self.po._loc_business_license_file_input().set_input_files(file_path)

    def click_continue(self) -> None:
        self.click(self.po.btn_continue)

    def complete_document_upload(
        self,
        *,
        certificate_type: str,
        card_number: str,
        certificate_file_path: str,
        business_license_type: str,
        business_license_file_path: str,
    ) -> None:
        self.select_certificate_type(certificate_type)
        self.enter_card_number(card_number)
        self.upload_certificate_file(certificate_type, certificate_file_path)
        self.select_business_license_type(business_license_type)
        self.upload_business_license_file(business_license_file_path)
        self.click_continue()

    def verify_card_number_error(self, message: str) -> None:
        assert_element_has_text(self.po.msg_card_number_error, message)
