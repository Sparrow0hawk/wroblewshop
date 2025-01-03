import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.app_client import AppClient, CupboardRepr, ItemRepr, UserRepr
from tests.e2e.oidc_server.users import StubUser
from tests.e2e.oidc_server.web_client import OidcClient
from tests.e2e.pages import HomePage


@pytest.mark.usefixtures("live_server", "oidc_server")
def test_add_item(app: Flask, page: Page, app_client: AppClient, oidc_client: OidcClient) -> None:
    oidc_client.add_user(StubUser(id="shopper", email="shopper@gmail.com"))
    app_client.add_cupboard(CupboardRepr(id=1, name="Palace", items=[ItemRepr(id=1, name="Rice")]))
    app_client.add_user(UserRepr(email="shopper@gmail.com", cupboard="Palace"))
    home_page = HomePage.open(page)

    home_page.actions.add_item().form.enter_name("Beans").confirm()

    assert app_client.get_cupboard(id_=1).items == [ItemRepr(id=1, name="Rice"), ItemRepr(id=2, name="Beans")]
