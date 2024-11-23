from typing import Generator

import inject
import pytest
from flask import Flask
from flask.testing import FlaskClient

from tests.integration.fakes import InMemoryCupboardRepository, InMemoryUserRepository
from wroblewshop import create_app
from wroblewshop.domain.cupboard import CupboardRepository
from wroblewshop.domain.user import UserRepository


@pytest.fixture(name="app", scope="class")
def app_fixture() -> Generator[Flask, None, None]:
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": b"secret-key!",
            "GOOGLE_OAUTH_CLIENT_ID": "test",
            "GOOGLE_OAUTH_CLIENT_SECRET": "test",
            "GOOGLE_SERVER_METADATA_URL": "test",
        }
    )
    inject.clear_and_configure(_test_bindings, bind_in_runtime=False, allow_override=True)
    yield app
    inject.clear()


@pytest.fixture(name="client")
def client_fixture(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(name="users")
def user_repository_fixture() -> Generator[UserRepository, None, None]:
    users = inject.instance(UserRepository)
    yield users
    users.clear()


@pytest.fixture(name="cupboards")
def cupboards_repository_fixture() -> Generator[CupboardRepository, None, None]:
    cupboards = inject.instance(CupboardRepository)
    yield cupboards
    cupboards.clear()


def _test_bindings(binder: inject.Binder) -> None:
    binder.bind_to_constructor(UserRepository, InMemoryUserRepository)
    binder.bind_to_constructor(CupboardRepository, InMemoryCupboardRepository)
