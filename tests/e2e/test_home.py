from __future__ import annotations

import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.pages import HomePage


@pytest.mark.usefixtures("live_server")
def test_home_shows_heading(app: Flask, page: Page) -> None:
    home_page = HomePage.open(page)

    assert home_page.is_visible
