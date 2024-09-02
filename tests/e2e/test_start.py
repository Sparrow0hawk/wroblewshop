from __future__ import annotations

import pytest
from flask import Flask
from playwright.sync_api import Page

from tests.e2e.pages import StartPage


@pytest.mark.usefixtures("live_server")
def test_start_shows_heading(app: Flask, page: Page) -> None:
    start_page = StartPage.open(page)

    assert start_page.is_visible
