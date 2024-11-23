from typing import Generator

import inject
import pytest
from flask.testing import FlaskClient

from wroblewshop.domain.cupboard import CupboardRepository
from wroblewshop.domain.user import User, UserRepository


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


def test_add_users(client: FlaskClient, users: UserRepository) -> None:
    response = client.post("/user", json={"email": "foo@example.com", "cupboard": "Palace"})

    assert response.status_code == 201
    user = users.get_by_email("foo@example.com")
    assert user and user.cupboard == "Palace"


def test_delete_users(client: FlaskClient, users: UserRepository) -> None:
    users.add(User(email="foo@example.com", cupboard="Palace"))
    response = client.delete("/user")

    assert response.status_code == 204
    assert not users.get_all()


def test_add_cupboard(client: FlaskClient, cupboards: CupboardRepository) -> None:
    response = client.post("/cupboard", json={"id": 1, "name": "Palace"})

    assert response.status_code == 201
    (cupboard,) = cupboards.get_all()
    assert cupboard and cupboard.id == 1 and cupboard.name == "Palace"


def test_delete_cupboards(client: FlaskClient, cupboards: CupboardRepository) -> None:
    response = client.delete("/cupboard")

    assert response.status_code == 204
    assert not cupboards.get_all()
