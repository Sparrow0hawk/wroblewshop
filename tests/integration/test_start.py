from flask.testing import FlaskClient

from tests.integration.pages import StartPage


def test_start_shows_heading(client: FlaskClient) -> None:
    start_page = StartPage.open(client)

    assert start_page.is_visible


def test_start_nav_shows_start(client: FlaskClient) -> None:
    start_page = StartPage.open(client)

    assert start_page.navbar.link == "/"


def test_start_shows_home_when_logged_in(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    response = client.get("/")

    assert response.status_code == 302 and response.location == "/home"
