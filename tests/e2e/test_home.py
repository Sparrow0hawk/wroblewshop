import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.app_client import AppClient, UserRepr
from tests.e2e.oidc_server.users import StubUser
from tests.e2e.oidc_server.web_client import OidcClient
from tests.e2e.pages import HomePage


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_home_shows_heading(app: Flask, page: Page, app_client: AppClient, oidc_client: OidcClient) -> None:
    oidc_client.add_user(StubUser(id="shopper", email="shopper@gmail.com"))
    app_client.add_user(UserRepr(email="shopper@gmail.com"))
    home_page = HomePage.open(page)

    assert home_page.is_visible


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_home_when_unauthorized_shows_unauthorized(app: Flask, page: Page, oidc_client: OidcClient) -> None:
    oidc_client.add_user(StubUser(id="shopper", email="shopper@gmail.com"))
    unauthorized_page = HomePage.open_when_unauthorized(page)

    assert unauthorized_page.is_visible


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_home_when_unauthenticated_shows_login(app: Flask, page: Page) -> None:
    login_page = HomePage.open_when_unauthenticated(page)

    assert login_page.is_visible
