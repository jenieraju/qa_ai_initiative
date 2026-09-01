"""Invoke task runner for the UI automation framework."""

import sys
import tomllib
import webbrowser
from pathlib import Path

from invoke import task

# Always run pytest under the interpreter invoke itself is running on, so a
# venv-activated shell and a bare `invoke` never pick different Pythons.
PYTHON = sys.executable


@task
def clean(c):
    """Remove build artifacts and cached results."""
    c.run("rm -rf output/ target/ .pytest_cache/ .ruff_cache/ playwright-report/ test-results/")
    c.run("find . -type d -name __pycache__ -exec rm -rf {} +", warn=True)


@task
def install(c):
    """Install Python dependencies and Playwright browsers."""
    c.run("pip install -r requirements.txt")
    c.run("playwright install")


@task
def install_precommit(c):
    """Install pre-commit hooks."""
    c.run("pre-commit install")


@task
def lint(c):
    """Run ruff (with auto-fix) and black."""
    c.run("ruff check --fix .")
    c.run("black .")


@task(name="lint-check")
def lint_check(c):
    """Check formatting and lint without modifying any files (CI / pre-test)."""
    c.run("ruff check .")
    c.run("black --check .")


@task(name="sync-requirements")
def sync_requirements(c):
    """Regenerate requirements.txt from pyproject.toml's dependency lists."""
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]
    lines = [
        "# Generated from pyproject.toml — edit dependencies there, "
        "then run `invoke sync-requirements`.",
        "# tests/test/core/test_dependency_sync.py fails if the two drift apart.",
        *project["dependencies"],
        "",
        "# dev",
        *project["optional-dependencies"]["dev"],
    ]
    Path("requirements.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("requirements.txt regenerated from pyproject.toml")


@task
def unit(c):
    """Run the fast no-browser framework tests (what pre-commit and CI gate on)."""
    c.run(f"{PYTHON} -m pytest -m unit -q --no-header -p no:cacheprovider")


@task
def precommit(c):
    """Run all pre-commit hooks."""
    c.run("pre-commit run --all-files")


@task(
    name="scaffold-feature",
    help={
        "slug": "Feature slug, e.g. checkout (lowercase snake_case)",
        "route": "Route path, e.g. /checkout",
        "priority": "p0|p1|p2 (default p2)",
        "marker": "Feature marker name, defaults to slug",
        "area": "tests/test/<area>/ subdirectory, defaults to slug",
    },
)
def scaffold_feature(c, slug, route, priority="p2", marker=None, area=None):
    """Scaffold PO/actions/steps/dataprovider/test skeleton for a new feature.

    Backs the scaffold-feature-automation skill. Requires confirmed locators
    from discover-locators-from-ui — this only stamps out TODO placeholders,
    and refuses to overwrite files that already exist.
    """
    from src.core.scaffold_generator import scaffold_feature as run_scaffold

    result = run_scaffold(slug=slug, route=route, priority=priority, marker=marker, area=area)
    for path in result["created"]:
        print(f"created  {path.relative_to(Path.cwd())}")
    for path in result["skipped"]:
        print(f"skipped  {path.relative_to(Path.cwd())} (already exists)")
    print("\nNext: fill in locators (discover-locators-from-ui), then:")
    print(f"  invoke lint && pytest --collect-only --env dev -m {marker or slug}")


@task(
    help={
        "env": "Target environment (dev|stg|uat|prod)",
        "markers": "Pytest marker expression",
        "parallel": "Number of xdist workers (0 = no parallel)",
        "args": "Additional pytest arguments",
    }
)
def test(c, env="dev", markers="not ignore", parallel=0, args=""):
    """Clean, lint-check, and run pytest.

    Uses lint-check rather than lint: rewriting source as a side effect of
    running the tests is surprising mid-debug. Run `invoke lint` to autofix.
    """
    clean(c)
    lint_check(c)
    cmd = f'{PYTHON} -m pytest -m "{markers}" --env {env} {args}'
    if parallel and int(parallel) > 0:
        cmd += f" -n {parallel} --dist loadgroup"
    c.run(cmd)


@task(
    help={
        "env": "Target environment (dev|stg|uat|prod)",
        "markers": "Pytest marker expression",
        "args": "Additional pytest arguments (e.g. --headless false -vv)",
    }
)
def test_files(c, env="dev", markers="not ignore", args=""):
    """Run each test file separately; generate a report set per file under output/reports/."""
    cmd = f'{PYTHON} -m src.core.per_file_report_runner --env {env} --markers "{markers}"'
    if args:
        cmd += f" -- {args}"
    c.run(cmd)


@task
def report_files(c):
    """Open the per-file report index (output/reports/index.html)."""
    index = Path("output/reports/index.html")
    if not index.exists():
        raise SystemExit("No per-file reports found. Run `invoke test-files` first.")
    # webbrowser works on macOS/Linux/Windows; xdg-open is Linux-only.
    webbrowser.open(index.resolve().as_uri())


@task
def report(c):
    """Generate and open the Allure HTML report (requires the Allure CLI).

    For a quick one-off view without a persisted report directory, run
    `allure serve output/allure-results` instead.
    """
    c.run("allure generate output/allure-results -o output/allure-report --clean")
    c.run("allure open output/allure-report")


@task(
    help={
        "env": "Target environment (dev|stg|uat|prod)",
        "headless": "Run browser headless: true|false",
        "open_report": "Open Allure in browser after run: true|false",
    }
)
def onboarding(c, env="dev", headless="false", open_report="true"):
    """Run individual onboarding E2E and generate a readable Allure report."""
    cmd = (
        f"{PYTHON} -m pytest --env {env} --headless {headless} "
        f'-m "onboarding and not ignore" tests/test/auth/test_onboarding.py -vv'
    )
    c.run(cmd)
    c.run("allure generate output/allure-results -o output/allure-report --clean")
    if str(open_report).strip().lower() in {"1", "true", "yes", "on"}:
        c.run("allure open output/allure-report")
