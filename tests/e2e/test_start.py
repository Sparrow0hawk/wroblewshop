import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.app_client import AppClient, UserRepr
from tests.e2e.oidc_server.users import StubUser
from tests.e2e.oidc_server.web_client import OidcClient
from tests.e2e.pages import StartPage


@pytest.mark.usefixtures("live_server")
def test_start_shows_heading(app: Flask, page: Page) -> None:
    start_page = StartPage.open(page)

    assert start_page.is_visible


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_start_shows_home(app: Flask, page: Page, app_client: AppClient, oidc_client: OidcClient) -> None:
    oidc_client.add_user(StubUser(id="shopper", email="shopper@gmail.com"))
    app_client.add_user(UserRepr(email="shopper@gmail.com"))
    start_page = StartPage.open(page)

    home_page = start_page.start()

    assert home_page.is_visible
