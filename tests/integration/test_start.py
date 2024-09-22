from __future__ import annotations

from bs4 import BeautifulSoup
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class StartPage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        heading = self._soup.select_one("h2")
        assert heading
        self.is_visible = heading.string == "Welcome to Wroblewshop" if heading.string else False

    @classmethod
    def open(cls, client: FlaskClient) -> StartPage:
        response = client.get("/")
        return StartPage(response)


def test_start_shows_heading(client: FlaskClient) -> None:
    start_page = StartPage.open(client)

    assert start_page.is_visible


def test_start_shows_home_when_logged_in(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    response = client.get("/")

    assert response.status_code == 302 and response.location == "/home"
