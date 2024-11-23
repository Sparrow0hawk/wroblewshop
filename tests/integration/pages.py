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


class HomePage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        navbar = self._soup.select_one("header.navbar")
        assert navbar
        self.navbar = SignedInNavBarComponent(navbar)
        heading = self._soup.select_one("h2")
        assert heading
        self.heading = heading.string if heading.string else False

    @classmethod
    def open(cls, client: FlaskClient) -> HomePage:
        response = client.get("/home")
        return HomePage(response)


class SignedInNavBarComponent:
    def __init__(self, navbar: Tag):
        navbar_links = navbar.select("a")
        assert navbar_links
        sign_out_link = navbar_links[1]
        self.sign_out = sign_out_link["href"]
