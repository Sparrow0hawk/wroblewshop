from typing import Generator

import pytest
from authlib.integrations.flask_client import OAuth
from authlib.oidc.core import UserInfo
from flask import current_app
from flask.testing import FlaskClient


class StubOidcServer:
    def __init__(self, client_id: str) -> None:
        self._url = "https://stub.example"
        self._client_id = client_id


class TestAuth:
    @pytest.fixture(name="oauth")
    def oauth_fixture(self) -> Generator[OAuth, None, None]:
        oauth = current_app.extensions["authlib.integrations.flask_client"]
        oauth_app = oauth.google
        previous_server_metadata = oauth_app.server_metadata
        yield oauth
        oauth_app.server_metadata = previous_server_metadata

    @pytest.fixture(autouse=True)
    def stub_server_metadata(self, oauth: OAuth) -> None:
        oauth.google.server_metadata = {"_loaded_at": 1}

    @pytest.fixture(name="oidc_server")
    def oidc_server_fixture(self, oauth: OAuth) -> StubOidcServer:
        oidc_server = StubOidcServer(client_id="test")
        oauth.google.server_metadata["authorization_endpoint"] = "https://stub.example/authorize"
        return oidc_server

    def test_logout_logs_out_from_oidc(self, client: FlaskClient) -> None:
        with client.session_transaction() as setup_session:
            setup_session["user"] = UserInfo({"email": "boardman@example.com"})
            setup_session["id_token"] = "jwt"

        response = client.get("/auth/logout")

        assert response.status_code == 302 and response.location == "/"

    def test_authorize_redirect_sets_secure_session_cookie(
        self, oidc_server: StubOidcServer, client: FlaskClient
    ) -> None:
        response = client.get("/home")

        value = response.headers["Set-Cookie"].split("; ")
        assert value[0].startswith("session=") and "Secure" in value
