from typing import Generator

import pytest
from flask import Flask
from playwright.sync_api import BrowserContext
from pytest_flask.live_server import LiveServer

from wroblewshop import create_app


@pytest.fixture(name="app", scope="package")
def app_fixture() -> Generator[Flask, None, None]:
    app = create_app({"TESTING": True, "SERVER_NAME": "localhost"})
    yield app


@pytest.fixture(name="browser_context_args", scope="package")
def browser_context_args_fixture(
    browser_context_args: dict[str, str], live_server: LiveServer
) -> dict[str, str]:
    browser_context_args["base_url"] = _get_url(live_server)
    return browser_context_args


@pytest.fixture(name="context")
def browser_context_fixture(
    context: BrowserContext,
) -> Generator[BrowserContext, None, None]:
    context.set_default_timeout(5_000)
    yield context


def _get_url(live_server: LiveServer) -> str:
    return f"http://{live_server.host}:{live_server.port}"
