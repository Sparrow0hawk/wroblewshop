from __future__ import annotations

from bs4 import BeautifulSoup
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class HomePage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        heading = self._soup.select_one("h2")
        assert heading
        self.is_visible = heading.string == "Home" if heading.string else False

    @classmethod
    def open(cls, client: FlaskClient) -> HomePage:
        response = client.get("/home")
        return HomePage(response)


def test_home_shows_heading(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    home_page = HomePage.open(client)

    assert home_page.is_visible
