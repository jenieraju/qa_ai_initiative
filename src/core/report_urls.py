"""Format local report paths as clickable file:// URLs for terminal output."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def file_url(path: Path | str) -> str:
    """Return a file:// URL for a local path (spaces encoded)."""
    resolved = Path(path).resolve()
    return resolved.as_uri()


def generate_allure_report(allure_results: Path, allure_report: Path) -> bool:
    """Build browsable Allure HTML from raw results. Returns True on success."""
    allure_bin = shutil.which("allure")
    if not allure_bin or not allure_results.exists() or not any(allure_results.iterdir()):
        return False
    allure_report.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [allure_bin, "generate", str(allure_results), "-o", str(allure_report), "--clean"],
        check=False,
    )
    return completed.returncode == 0 and (allure_report / "index.html").exists()


def open_allure_report(allure_report: Path, *, host: str = "127.0.0.1", port: int = 5050) -> bool:
    """Serve Allure over HTTP and open the browser (non-blocking).

    Opening via file:// leaves the UI empty; Allure must be served.
    """
    allure_bin = shutil.which("allure")
    if not allure_bin or not (allure_report / "index.html").exists():
        return False
    # Detach so pytest can exit; allure open otherwise blocks forever.
    subprocess.Popen(
        [allure_bin, "open", str(allure_report), "--host", host, "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    print(f"\n  Opening Allure at http://{host}:{port}/", flush=True)
    return True


def print_report_urls(
    *,
    html_report: Path | None = None,
    junit_report: Path | None = None,
    allure_results: Path | None = None,
    allure_report: Path | None = None,
    execution_log: Path | None = None,
    index_report: Path | None = None,
    title: str = "Reports",
) -> None:
    """Print report locations with file:// URLs after a test run."""
    lines: list[str] = [f"\n=== {title} ==="]
    if index_report and index_report.exists():
        lines.append(f"  Index:    {file_url(index_report)}")
    if html_report and html_report.exists():
        lines.append(f"  HTML:     {file_url(html_report)}")
    if junit_report and junit_report.exists():
        lines.append(f"  JUnit:    {file_url(junit_report)}")
    if execution_log and execution_log.exists():
        lines.append(f"  Log:      {file_url(execution_log)}")
    if allure_report and (allure_report / "index.html").exists():
        # Do NOT print file:// for Allure — browsers block local JSON and the UI looks empty.
        lines.append(f"  Allure:   {allure_report}  (do not open via file://)")
        lines.append(f"            Open: allure open {allure_report}")
        lines.append(
            f"            Or:   allure serve {allure_results or allure_report.parent / 'allure-results'}"
        )
    elif allure_results and allure_results.exists() and any(allure_results.iterdir()):
        lines.append(f"  Allure:   {allure_results} (raw results — generate first)")
        lines.append(f"            Open: allure serve {allure_results}")
    if len(lines) == 1:
        lines.append("  (no report artifacts found)")
    print("\n".join(lines), flush=True)
