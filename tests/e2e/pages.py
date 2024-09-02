from __future__ import annotations

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
