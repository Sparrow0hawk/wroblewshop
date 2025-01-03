from __future__ import annotations

from playwright.sync_api import Locator, Page


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
        self._main = page.get_by_role("main")
        self.actions = ActionsListComponent(self._main.get_by_role("list"))

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


class ActionsListComponent:
    def __init__(self, actions_list: Locator):
        self.actions_list = actions_list

    def add_item(self) -> AddItemPage:
        self.actions_list.get_by_role("link", name="Add item").click()
        return AddItemPage(self.actions_list.page)


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


class AddItemPage:
    def __init__(self, page: Page):
        self._page = page
        self.form = AddItemFormComponent(page.get_by_role("form"))

    @property
    def is_visible(self) -> bool:
        return self._page.get_by_role("heading", name="Add item", exact=True).is_visible()


class AddItemFormComponent:
    def __init__(self, form: Locator):
        self._form = form
        self.name = TextComponent(form.get_by_label("name"))
        self._confirm = form.get_by_role("button", name="Confirm")

    def enter_name(self, name: str) -> AddItemFormComponent:
        self.name.value = name
        return AddItemFormComponent(self._form)

    def confirm(self) -> AddItemPage:
        self._confirm.click()
        return AddItemPage(self._form.page)


class TextComponent:
    def __init__(self, input_: Locator):
        self._input = input_

    @property
    def value(self) -> str:
        return self._input.input_value()

    @value.setter
    def value(self, value: str) -> None:
        self._input.fill(value)
