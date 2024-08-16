import pytest
from flask import Flask
from flask.testing import FlaskClient

from wroblewshop import create_app


@pytest.fixture(name="app")
def app_fixture() -> Flask:
    app = create_app({"TESTING": True})
    return app


@pytest.fixture(name="client")
def client_fixture(app: Flask) -> FlaskClient:
    return app.test_client()
