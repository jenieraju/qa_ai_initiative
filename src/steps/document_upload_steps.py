"""Reusable document-upload steps decorated with Allure (organization path)."""

import allure
from playwright.sync_api import Page

from src.page_actions.document_upload_actions import DocumentUploadPageActions


@allure.step("User verifies document-upload page is displayed")
def user_verifies_document_upload_page_is_displayed(page: Page) -> None:
    DocumentUploadPageActions(page).verify_document_upload_page_visible()


@allure.step("User completes document upload with certificate type '{certificate_type}'")
def user_completes_document_upload(
    page: Page,
    *,
    certificate_type: str,
    card_number: str,
    certificate_file_path: str,
    business_license_type: str,
    business_license_file_path: str,
) -> None:
    DocumentUploadPageActions(page).complete_document_upload(
        certificate_type=certificate_type,
        card_number=card_number,
        certificate_file_path=certificate_file_path,
        business_license_type=business_license_type,
        business_license_file_path=business_license_file_path,
    )
