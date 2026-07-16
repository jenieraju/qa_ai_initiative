"""Invoke task runner for the UI automation framework."""

from pathlib import Path

from invoke import task


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


@task
def precommit(c):
    """Run all pre-commit hooks."""
    c.run("pre-commit run --all-files")


@task(
    help={
        "env": "Target environment (dev|stg|uat|prod)",
        "markers": "Pytest marker expression",
        "parallel": "Number of xdist workers (0 = no parallel)",
        "args": "Additional pytest arguments",
    }
)
def test(c, env="dev", markers="not ignore", parallel=0, args=""):
    """Clean, lint, and run pytest."""
    clean(c)
    lint(c)
    cmd = f'pytest -m "{markers}" --env {env} {args}'
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
    cmd = f'python -m src.core.per_file_report_runner --env {env} --markers "{markers}"'
    if args:
        cmd += f" -- {args}"
    c.run(cmd)


@task
def report_files(c):
    """Open the per-file report index (output/reports/index.html)."""
    index = Path("output/reports/index.html")
    if not index.exists():
        raise SystemExit("No per-file reports found. Run `invoke test-files` first.")
    c.run(f"xdg-open {index}", warn=True)


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
        f'python3.11 -m pytest --env {env} --headless {headless} '
        f'-m "onboarding and not ignore" tests/test/auth/test_onboarding.py -vv'
    )
    c.run(cmd)
    c.run("allure generate output/allure-results -o output/allure-report --clean")
    if str(open_report).strip().lower() in {"1", "true", "yes", "on"}:
        c.run("allure open output/allure-report")
