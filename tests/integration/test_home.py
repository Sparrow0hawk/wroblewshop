from typing import Generator

import inject
import pytest
from flask.testing import FlaskClient

from tests.integration.pages import HomePage
from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
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


def test_home_shows_heading(users: UserRepository, cupboards: CupboardRepository, client: FlaskClient) -> None:
    cupboards.add(Cupboard(id_=1, name="Palace"))
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    home_page = HomePage.open(client)

    assert home_page.heading == "Palace Cupboard"


def test_home_shows_sign_out(users: UserRepository, cupboards: CupboardRepository, client: FlaskClient) -> None:
    cupboards.add(Cupboard(id_=1, name="Palace"))
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    home_page = HomePage.open(client)

    assert home_page.navbar.sign_out == "/auth/logout"
