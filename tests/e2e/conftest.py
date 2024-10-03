import os
import socket
from typing import Any, Generator

import inject
import pytest
from _pytest.fixtures import FixtureRequest
from flask import Flask
from playwright.sync_api import BrowserContext
from pytest_flask.live_server import LiveServer

from tests.e2e.app_client import AppClient
from tests.e2e.oidc_server.app import OidcServerApp
from tests.e2e.oidc_server.app import create_app as oidc_server_create_app
from tests.e2e.oidc_server.clients import StubClient
from tests.e2e.oidc_server.web_client import OidcClient
from wroblewshop import create_app


@pytest.fixture(name="app", scope="package")
def app_fixture(oidc_server: LiveServer) -> Generator[Flask, None, None]:
    client_id = "app"
    client_secret = "secret"
    port = _get_random_port()

    app = create_app(
        {
            "TESTING": True,
            "SERVER_NAME": f"localhost:{port}",
            "LIVESERVER_PORT": port,
            "SECRET_KEY": b"secret-key",
            "GOOGLE_OAUTH_CLIENT_ID": client_id,
            "GOOGLE_OAUTH_CLIENT_SECRET": client_secret,
            "GOOGLE_SERVER_METADATA_URL": oidc_server.app.url_for("openid_configuration", _external=True),
        }
    )

    app_oidc_client = StubClient(
        client_id=client_id,
        redirect_uri=app.url_for("auth.callback", _external=True),
        client_secret=client_secret,
        scope="openid email",
    )
    oidc_client = OidcClient(_get_url(oidc_server))
    oidc_client.add_client(app_oidc_client)
    yield app
    inject.clear()
    oidc_client.clear_clients()


@pytest.fixture(name="oidc_server_app", scope="package")
def oidc_server_app_fixture() -> OidcServerApp:
    os.environ["AUTHLIB_INSECURE_TRANSPORT"] = "true"
    port = _get_random_port()
    return oidc_server_create_app({"TESTING": True, "SERVER_NAME": f"localhost:{port}"})


@pytest.fixture(name="oidc_server", scope="package")
def oidc_server_fixture(oidc_server_app: OidcServerApp, request: FixtureRequest) -> Generator[LiveServer, Any, Any]:
    port = int(oidc_server_app.config["SERVER_NAME"].split(":")[1])
    server = LiveServer(oidc_server_app, "localhost", port, 5, True)
    server.start()
    request.addfinalizer(server.stop)
    yield server


@pytest.fixture(name="oidc_client")
def oidc_client_fixture(oidc_server: LiveServer) -> Generator[OidcClient, Any, Any]:
    client = OidcClient(_get_url(oidc_server))
    yield client
    client.clear_users()


@pytest.fixture(name="app_client")
def app_client_fixture(live_server: LiveServer) -> Generator[AppClient, None, None]:
    client = AppClient(_get_url(live_server))
    yield client
    client.clear_users()


@pytest.fixture(name="browser_context_args", scope="package")
def browser_context_args_fixture(browser_context_args: dict[str, str], live_server: LiveServer) -> dict[str, str]:
    browser_context_args["base_url"] = _get_url(live_server)
    return browser_context_args


@pytest.fixture(name="context")
def browser_context_fixture(
    context: BrowserContext,
) -> Generator[BrowserContext, None, None]:
    context.set_default_timeout(5_000)
    yield context


def _get_random_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port: int = sock.getsockname()[1]
    sock.close()
    return port


def _get_url(live_server: LiveServer) -> str:
    return f"http://{live_server.host}:{live_server.port}"
