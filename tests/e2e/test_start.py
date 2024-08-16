from __future__ import annotations

import pytest
from flask import Flask
from playwright.sync_api import Page


class StartPage:
    def __init__(self, page: Page):
        self._page = page

    @classmethod
    def open(cls, page: Page) -> StartPage:
        page.goto("/")
        return cls(page)

    @property
    def is_visible(self) -> bool:
        return self._page.get_by_role(
            "heading", name="Wroblewshop", exact=True
        ).is_visible()


@pytest.mark.usefixtures("live_server")
def test_start_shows_heading(app: Flask, page: Page) -> None:
    start_page = StartPage.open(page)

    assert start_page.is_visible
