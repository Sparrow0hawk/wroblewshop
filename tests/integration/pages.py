from __future__ import annotations

from typing import Any, Iterator

from bs4 import BeautifulSoup, Tag
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


class StartPage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        navbar = self._soup.select_one("header.navbar")
        assert navbar
        self.navbar = NavbarComponent(navbar)
        heading = self._soup.select_one("h2")
        assert heading
        self.is_visible = heading.string == "Welcome to Wroblewshop" if heading.string else False

    @classmethod
    def open(cls, client: FlaskClient) -> StartPage:
        response = client.get("/")
        return StartPage(response)


class NavbarComponent:
    def __init__(self, navbar: Tag):
        navbar_link = navbar.select_one("a")
        assert navbar_link
        self.link = navbar_link["href"]


class HomePage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        navbar = self._soup.select_one("header.navbar")
        assert navbar
        self.navbar = SignedInNavBarComponent(navbar)
        heading = self._soup.select_one("h2")
        assert heading
        self.heading = heading.string if heading.string else False
        actions_list = self._soup.select_one("main ul")
        assert actions_list
        self.items = ActionsListComponent(actions_list)

    @classmethod
    def open(cls, client: FlaskClient) -> HomePage:
        response = client.get("/home")
        return HomePage(response)


class SignedInNavBarComponent:
    def __init__(self, navbar: Tag):
        navbar_links = navbar.select("a")
        assert navbar_links
        sign_out_link = navbar_links[1]
        self.sign_out = sign_out_link["href"]


class ActionsListComponent:
    def __init__(self, actions_list: Tag):
        add_item_link = actions_list.select_one("a")
        assert add_item_link
        self.add_item = add_item_link["href"]


class AddItemPage:
    def __init__(self, response: TestResponse):
        self._soup = BeautifulSoup(response.text, "html.parser")
        heading = self._soup.select_one("h2")
        assert heading
        form = self._soup.select_one("form")
        assert form
        self.form = AddItemFormComponent(form)
        self.is_visible = heading.string == "Add item" if heading.string else False
        delete_items = self._soup.select_one("hr ~ section")
        assert delete_items
        self.delete_items = DeleteItemSectionComponent(delete_items)

    @classmethod
    def open(cls, client: FlaskClient) -> AddItemPage:
        response = client.get("/item")
        return AddItemPage(response)


class AddItemFormComponent:
    def __init__(self, form: Tag):
        alert = form.select_one(".alert-danger")
        self.alert = alert.text.strip() if alert else None
        input_ = form.select_one("input[name='name']")
        assert input_
        self.name = TextComponent(input_)
        self.confirm_url = form["action"]


class DeleteItemSectionComponent:
    def __init__(self, section: Tag):
        self._forms = section.select("form")

    def __iter__(self) -> Iterator[DeleteItemFormComponent]:
        return (DeleteItemFormComponent(row) for row in self._forms)

    def __call__(self, *args: Any, **kwargs: Any) -> list[dict[str, str | int]]:
        return [{"name": (cell.name or "")} for cell in self]


class DeleteItemFormComponent:
    def __init__(self, form: Tag):
        label = form.select_one("label")
        self.name = label.string if label else None


class TextComponent:
    def __init__(self, input_: Tag):
        fieldset = input_.find_parent("fieldset")
        assert fieldset
        self.name = input_["name"]
        self.value = input_["value"]
        self.is_errored = "is-invalid" in input_.get_attribute_list("class")
        error_message = fieldset.select_one(".invalid-feedback")
        self.error = error_message.text.strip() if error_message else None
