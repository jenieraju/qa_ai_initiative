"""Capture browser failure artifacts for Allure and pytest-html reports."""

from __future__ import annotations

import contextlib
import re
from pathlib import Path

import allure
from playwright.sync_api import Page
from pytest_html import extras as html_extras

from src.core.session_state import session_state

SCREENSHOTS_DIR_NAME = "screenshots"


def safe_filename(nodeid: str) -> str:
    """Turn a pytest nodeid into a filesystem-safe artifact name."""
    return re.sub(r"[^\w.-]+", "_", nodeid).strip("_")[:180]


def _failure_details_text(page: Page, *, error_message: str = "") -> str:
    lines = [
        f"URL: {page.url}",
        f"Title: {page.title()}",
    ]
    if session_state.metadata.get("mobile_number"):
        lines.append(f"Mobile: {session_state.metadata['mobile_number']}")
    if session_state.active_profile:
        lines.append(f"Auth profile: {session_state.active_profile}")
    if error_message:
        lines.append("")
        lines.append("Error:")
        lines.append(error_message)
    return "\n".join(lines)


@allure.step("Capture failure artifacts")
def capture_failure_artifacts(
    page: Page,
    *,
    output_dir: Path,
    nodeid: str,
    error_message: str = "",
    console_logs: list[str] | None = None,
) -> list:
    """Attach screenshot + context to Allure; return pytest-html extras."""
    html_extra: list = []
    screenshots_dir = output_dir / SCREENSHOTS_DIR_NAME
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    details = _failure_details_text(page, error_message=error_message)
    allure.attach(
        details,
        name="failure-details",
        attachment_type=allure.attachment_type.TEXT,
    )
    html_extra.append(html_extras.text(details, name="Failure details"))

    try:
        screenshot = page.screenshot(full_page=True)
    except Exception as exc:
        msg = f"Could not capture screenshot: {exc}"
        allure.attach(
            msg, name="failure-screenshot-error", attachment_type=allure.attachment_type.TEXT
        )
        html_extra.append(html_extras.text(msg, name="Screenshot error"))
        return html_extra

    screenshot_path = screenshots_dir / f"{safe_filename(nodeid)}.png"
    screenshot_path.write_bytes(screenshot)

    allure.attach(
        screenshot,
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    html_extra.append(
        html_extras.image(
            screenshot,
            name="Failure screenshot",
            mime_type="image/png",
            extension="png",
        )
    )
    html_extra.append(
        html_extras.text(
            str(screenshot_path.relative_to(output_dir.parent)),
            name="Screenshot file",
        )
    )

    with contextlib.suppress(Exception):
        allure.attach(
            page.content(),
            name="page-source",
            attachment_type=allure.attachment_type.HTML,
        )

    if console_logs:
        log_text = "\n".join(console_logs)
        allure.attach(
            log_text,
            name="browser-console-logs",
            attachment_type=allure.attachment_type.TEXT,
        )
        html_extra.append(html_extras.text(log_text, name="Browser console logs"))

    return html_extra
