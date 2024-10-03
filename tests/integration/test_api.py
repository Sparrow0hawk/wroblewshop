from typing import Generator

import inject
import pytest
from flask.testing import FlaskClient

from wroblewshop.domain.user import User, UserRepository


@pytest.fixture(name="users")
def user_repository_fixture() -> Generator[UserRepository, None, None]:
    users = inject.instance(UserRepository)
    yield users
    users.clear()


def test_add_users(client: FlaskClient, users: UserRepository) -> None:
    response = client.post("/user", json={"email": "foo@example.com"})

    assert response.status_code == 201
    assert users.get_by_email("foo@example.com")


def test_delete_users(client: FlaskClient, users: UserRepository) -> None:
    users.add(User(email="foo@example.com"))
    response = client.delete("/user")

    assert response.status_code == 204
    assert not users.get_all()
