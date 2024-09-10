from __future__ import annotations

import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.oidc_server.users import StubUser
from tests.e2e.oidc_server.web_client import OidcClient
from tests.e2e.pages import HomePage


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_home_shows_heading(app: Flask, page: Page, oidc_client: OidcClient) -> None:
    oidc_client.add_user(StubUser(id="shopper", email="shopper@gmail.com"))
    home_page = HomePage.open(page)

    assert home_page.is_visible
