import pytest
from flask import Flask
from flask.testing import FlaskClient

from wroblewshop import create_app


@pytest.fixture(name="app")
def app_fixture() -> Flask:
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": b"secret-key!",
            "GOOGLE_OAUTH_CLIENT_ID": "test",
            "GOOGLE_OAUTH_CLIENT_SECRET": "test",
            "GOOGLE_SERVER_METADATA_URL": "test",
        }
    )
    return app


@pytest.fixture(name="client")
def client_fixture(app: Flask) -> FlaskClient:
    return app.test_client()
