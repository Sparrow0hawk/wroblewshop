from __future__ import annotations

from playwright.sync_api import Page


class StartPage:
    def __init__(self, page: Page):
        self._page = page
        self._button = page.get_by_role("button")

    @classmethod
    def open(cls, page: Page) -> StartPage:
        page.goto("/")
        return cls(page)

    @property
    def is_visible(self) -> bool:
        return self._page.get_by_role("heading", name="Welcome to Wroblewshop", exact=True).is_visible()

    def start(self) -> HomePage:
        self._button.click()
        return HomePage(self._page)


class HomePage:
    def __init__(self, page: Page):
        self._page = page
        self._heading = page.get_by_role("heading")

    @classmethod
    def open(cls, page: Page) -> HomePage:
        page.goto("/home")
        return cls(page)

    @property
    def heading(self) -> str | None:
        return self._heading.text_content()

    @classmethod
    def open_when_unauthenticated(cls, page: Page) -> LoginPage:
        cls.open(page)
        return LoginPage(page)

    @classmethod
    def open_when_unauthorized(cls, page: Page) -> ForbiddenPage:
        cls.open(page)
        return ForbiddenPage(page)


class LoginPage:
    def __init__(self, page: Page):
        self._page = page

    @property
    def is_visible(self) -> bool:
        return self._page.get_by_role("heading", name="Login", exact=True).is_visible()


class ForbiddenPage:
    def __init__(self, page: Page):
        self._page = page

    @property
    def is_visible(self) -> bool:
        return self._page.get_by_role("heading", name="Forbidden", exact=True).is_visible()
