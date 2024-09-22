from __future__ import annotations

from bs4 import BeautifulSoup, Tag
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class StartPage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        navbar = self._soup.select_one("header.navbar")
        assert navbar
        self.navbar = NavbarComponent(navbar)
        heading = self._soup.select_one("h2")
        assert heading
        self.is_visible = heading.string == "Welcome to Wroblewshop" if heading.string else False

    @classmethod
    def open(cls, client: FlaskClient) -> StartPage:
        response = client.get("/")
        return StartPage(response)


class NavbarComponent:
    def __init__(self, navbar: Tag):
        navbar_link = navbar.select_one("a")
        assert navbar_link
        self.link = navbar_link["href"]


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
