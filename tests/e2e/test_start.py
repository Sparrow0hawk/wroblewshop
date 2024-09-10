from __future__ import annotations

import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.oidc_server.users import StubUser
from tests.e2e.oidc_server.web_client import OidcClient
from tests.e2e.pages import StartPage


@pytest.mark.usefixtures("live_server")
def test_start_shows_heading(app: Flask, page: Page) -> None:
    start_page = StartPage.open(page)

    assert start_page.is_visible


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_start_shows_home(app: Flask, oidc_client: OidcClient, page: Page) -> None:
    oidc_client.add_user(StubUser(id="shopper", email="shopper@gmail.com"))
    start_page = StartPage.open(page)

    home_page = start_page.start()

    assert home_page.is_visible
