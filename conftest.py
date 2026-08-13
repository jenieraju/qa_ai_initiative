import os

from src.utils.logger import configure_logging


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Environment to run against (dev/stg)")
    parser.addoption("--browser-name", action="store", default="chromium", help="Browser to run against")


def pytest_configure(config):
    configure_logging()
    env = config.getoption("--env")
    if env:
        os.environ["COFEE_ENV"] = env
