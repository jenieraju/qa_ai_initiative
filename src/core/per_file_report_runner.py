"""Run each test file in isolation and generate a dedicated report set."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from src.core.report_urls import file_url, print_report_urls

REPO_ROOT = Path(__file__).resolve().parents[2]
TESTS_ROOT = REPO_ROOT / "tests" / "test"
REPORTS_ROOT = REPO_ROOT / "output" / "reports"


@dataclass(frozen=True)
class FileRunResult:
    test_file: str
    slug: str
    exit_code: int
    report_dir: str
    allure_report: str | None
    collected: bool


def discover_test_files(tests_root: Path = TESTS_ROOT) -> list[Path]:
    """Return all test modules under tests/test/, sorted for stable runs."""
    return sorted(tests_root.rglob("test_*.py"))


def report_slug(test_file: Path) -> str:
    """Stable folder name for a test module (e.g. test_onboarding)."""
    return test_file.stem


def _allure_cli() -> str | None:
    return shutil.which("allure")


def run_test_file(
    test_file: Path,
    *,
    env: str,
    markers: str,
    pytest_args: list[str],
) -> FileRunResult:
    """Run one test module and write reports under output/reports/<slug>/."""
    slug = report_slug(test_file)
    report_dir = REPORTS_ROOT / slug
    allure_results = report_dir / "allure-results"
    allure_report = report_dir / "allure-report"

    report_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test_file.relative_to(REPO_ROOT)),
        "-m",
        markers,
        "--env",
        env,
        f"--alluredir={allure_results}",
        f"--html={report_dir / 'report.html'}",
        "--self-contained-html",
        f"--junitxml={report_dir / 'junit-results.xml'}",
        f"--log-file={report_dir / 'execution.log'}",
        # Each file runs in its own pytest process; without this every one of
        # them would open its own Allure browser tab. This runner prints a
        # single index at the end instead.
        "--open-allure=false",
        "-ra",
        "--strict-markers",
        *pytest_args,
    ]

    completed = subprocess.run(cmd, cwd=REPO_ROOT, check=False)

    generated_allure: str | None = None
    allure_bin = _allure_cli()
    if allure_bin and any(allure_results.iterdir()):
        gen = subprocess.run(
            [allure_bin, "generate", str(allure_results), "-o", str(allure_report), "--clean"],
            cwd=REPO_ROOT,
            check=False,
        )
        if gen.returncode == 0:
            generated_allure = str(allure_report)

    print_report_urls(
        html_report=report_dir / "report.html",
        junit_report=report_dir / "junit-results.xml",
        allure_results=allure_results,
        allure_report=allure_report if generated_allure else None,
        execution_log=report_dir / "execution.log",
        title=f"Reports — {slug}",
    )

    return FileRunResult(
        test_file=str(test_file.relative_to(REPO_ROOT)),
        slug=slug,
        exit_code=completed.returncode,
        report_dir=str(report_dir.relative_to(REPO_ROOT)),
        allure_report=(str(allure_report.relative_to(REPO_ROOT)) if generated_allure else None),
        collected=True,
    )


def run_all_test_files(
    *,
    env: str = "dev",
    markers: str = "not ignore",
    pytest_args: list[str] | None = None,
    tests_root: Path = TESTS_ROOT,
) -> dict:
    """Run every test file and write a combined summary under output/reports/."""
    pytest_args = pytest_args or []
    test_files = discover_test_files(tests_root)
    if not test_files:
        raise FileNotFoundError(f"No test_*.py files found under {tests_root}")

    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    results: list[FileRunResult] = []

    for test_file in test_files:
        print(f"\n=== Running {test_file.relative_to(REPO_ROOT)} ===", flush=True)
        results.append(run_test_file(test_file, env=env, markers=markers, pytest_args=pytest_args))

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "env": env,
        "markers": markers,
        "total_files": len(results),
        "passed_files": sum(1 for r in results if r.exit_code == 0),
        "failed_files": sum(1 for r in results if r.exit_code != 0),
        "allure_cli": _allure_cli() is not None,
        "results": [asdict(r) for r in results],
    }
    summary_path = REPORTS_ROOT / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _write_summary_index(summary)
    return summary


def _write_summary_index(summary: dict) -> None:
    """Minimal HTML index linking to each per-file report set."""
    rows = []
    for item in summary["results"]:
        status = "passed" if item["exit_code"] == 0 else "failed"
        report_dir = item["report_dir"]
        links = [
            f'<a href="{report_dir}/report.html">pytest-html</a>',
            f'<a href="{report_dir}/junit-results.xml">junit</a>',
            f'<a href="{report_dir}/execution.log">log</a>',
        ]
        if item["allure_report"]:
            # Allure must be served over HTTP — file:// links show an empty UI.
            links.insert(
                0,
                f'<code>allure open {item["allure_report"]}</code>',
            )
        rows.append(
            f'<tr><td>{item["slug"]}</td>'
            f'<td class="{status}">{status}</td>'
            f"<td>{' | '.join(links)}</td></tr>"
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Per-file test reports</title>
  <style>
    body {{ font-family: sans-serif; margin: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5rem 0.75rem; text-align: left; }}
    th {{ background: #f5f5f5; }}
    .failed {{ color: #b00020; font-weight: 600; }}
    .passed {{ color: #1b5e20; font-weight: 600; }}
  </style>
</head>
<body>
  <h1>Per-file test reports</h1>
  <p>Generated: {summary["generated_at"]} | env={summary["env"]} | markers={summary["markers"]}</p>
  <p>Files passed: {summary["passed_files"]} / {summary["total_files"]}</p>
  <table>
    <thead><tr><th>Test file</th><th>Status</th><th>Reports</th></tr></thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""
    (REPORTS_ROOT / "index.html").write_text(html, encoding="utf-8")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", default="dev", help="Target environment (dev|stg|uat|prod)")
    parser.add_argument(
        "--markers",
        default="not ignore",
        help='Pytest marker expression (default: "not ignore")',
    )
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Extra pytest args after -- (e.g. -- --headless false -vv)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    pytest_args = [a for a in args.pytest_args if a != "--"]
    summary = run_all_test_files(env=args.env, markers=args.markers, pytest_args=pytest_args)

    print("\n=== Per-file report summary ===", flush=True)
    for item in summary["results"]:
        status = "PASS" if item["exit_code"] == 0 else "FAIL"
        report_dir = REPO_ROOT / item["report_dir"]
        print(f"  [{status}] {item['test_file']}", flush=True)
        print(f"           HTML:   {file_url(report_dir / 'report.html')}", flush=True)
        if item["allure_report"]:
            allure_dir = REPO_ROOT / item["allure_report"]
            print(f"           Allure: allure open {allure_dir}", flush=True)
    print_report_urls(
        index_report=REPORTS_ROOT / "index.html",
        title="All test files",
    )

    return 0 if summary["failed_files"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
