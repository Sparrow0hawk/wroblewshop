from flask.testing import FlaskClient

from tests.integration.pages import HomePage
from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.user import User, UserRepository


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
