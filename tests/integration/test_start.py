from __future__ import annotations

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class StartPage:
    def __init__(self, response: TestResponse):
        self._response = response
        self.is_visible = "<h2>Welcome to Wroblewshop</h2>" in self._response.text

    @classmethod
    def open(cls, client: FlaskClient) -> StartPage:
        response = client.get("/")
        return StartPage(response)


def test_start_shows_heading(client: FlaskClient) -> None:
    start_page = StartPage.open(client)

    assert start_page.is_visible
