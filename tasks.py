"""Invoke task runner for the UI automation framework."""

from invoke import task


@task
def clean(c):
    """Remove build artifacts and cached results."""
    c.run("rm -rf target/ .pytest_cache/ .ruff_cache/ playwright-report/ test-results/")
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


@task
def report(c):
    """Generate and open the Allure HTML report."""
    c.run("allure generate target/allure-results -o target/allure-report --clean")
    c.run("allure open target/allure-report")
