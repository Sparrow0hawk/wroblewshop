from flask.testing import FlaskClient

from tests.integration.pages import HomePage


def test_home_shows_heading(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    home_page = HomePage.open(client)

    assert home_page.is_visible


def test_home_shows_sign_out(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    home_page = HomePage.open(client)

    assert home_page.navbar.sign_out == "/auth/logout"
