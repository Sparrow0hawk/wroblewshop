from __future__ import annotations

import pytest
from flask import Flask
from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self._page = page

    @classmethod
    def open(cls, page: Page) -> HomePage:
        page.goto("/home")
        return cls(page)

    @property
    def is_visible(self) -> bool:
        return self._page.get_by_role("heading", name="Home", exact=True).is_visible()


@pytest.mark.usefixtures("live_server")
def test_home_shows_heading(app: Flask, page: Page) -> None:
    home_page = HomePage.open(page)

    assert home_page.is_visible
