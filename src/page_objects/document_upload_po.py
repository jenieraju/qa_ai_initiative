"""Document-upload page object — locators only (organization onboarding path).

Covers AUTH.DOCUMENT_UPLOAD ("/document-upload"): certificate type (PAN/GSTIN),
card number, certificate file, and business-license type + file.
All page.locator() / page.get_by_*() calls must live in this file only.
"""

from playwright.sync_api import Locator

from src.core.base_page import BasePage

# Certificate type keys — src/features/authentication/constants/common.ts (app repo)
CERTIFICATE_TYPE_PAN = "pan"
CERTIFICATE_TYPE_GSTIN = "gstin"

CERTIFICATE_FILE_LABELS = {
    CERTIFICATE_TYPE_PAN: "PAN Certificate",
    CERTIFICATE_TYPE_GSTIN: "GST Certificate",
}

BUSINESS_LICENSE_FILE_LABEL = "Business License"


class DocumentUploadPage(BasePage):
    """Page object for the organization document-upload screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        self.lbl_section_title = self.get_by_data_test_id("authentication_title")
        self.btn_continue = self.get_by_button("Continue")
        self.msg_card_number_error = self.get_by_data_test_id("error_text")

        self.rdo_certificate_pan = self.get_by_data_test_id("groups_addKycPopup_panBtn")
        self.rdo_certificate_gstin = self.get_by_data_test_id("groups_addKycPopup_gstinBtn")
        self.input_card_number = self.get_by_locator('input[name="cardNumber"]')

        self.btn_business_license_dropdown = self.get_by_button("Select document")

    def _loc_certificate_file_input(self, certificate_type: str) -> Locator:
        label = CERTIFICATE_FILE_LABELS[certificate_type]
        return self.get_by_locator(f'input[id="{label}_input_id"]')

    def _loc_business_license_file_input(self) -> Locator:
        return self.get_by_locator(f'input[id="{BUSINESS_LICENSE_FILE_LABEL}_input_id"]')

    def _loc_business_license_option(self, option_value: str) -> Locator:
        return self.get_by_locator(f"#dropdown_{option_value}")
