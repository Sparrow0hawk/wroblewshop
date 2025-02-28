import pytest
from flask_wtf.csrf import generate_csrf
from werkzeug.datastructures import MultiDict

from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.domain.item import CupboardItems, Item
from wroblewshop.views.item import (
    AddItemContext,
    AddItemForm,
    DeleteItemForm,
    DeleteItemRowContext,
)


@pytest.mark.usefixtures("app")
class TestAddItemContext:
    def test_create(self) -> None:
        item = Item(id=1, name="Beans")
        form = DeleteItemForm.create_class(item)()
        context = AddItemContext(
            items=[DeleteItemRowContext(id=1, form=form)],
            form=AddItemForm(existing_items=[item]),
        )

        assert context.form.name.data is None and context.form.existing_items == [Item(id=1, name="Beans")]
        delete_item_row: DeleteItemRowContext
        (delete_item_row,) = context.items
        assert delete_item_row.id == 1 and "delete_beans" in delete_item_row.form

    def test_from_domain(self) -> None:
        cupboard = Cupboard(id_=0, name="")
        cupboard.items.add_items(*[Item(id=1, name="Beans"), Item(id=2, name="Rice")])

        context = AddItemContext.from_domain(cupboard)

        assert context.form.name.data is None
        assert context.form.existing_items == [Item(id=1, name="Beans"), Item(id=2, name="Rice")]
        item1: DeleteItemRowContext
        item2: DeleteItemRowContext
        (item1, item2) = context.items
        assert "delete_beans" in item1.form
        assert "delete_rice" in item2.form


@pytest.mark.usefixtures("app")
class TestDeleteItemRowContext:
    def test_create(self) -> None:
        form = DeleteItemForm.create_class(Item(id=1, name="Beans"))()
        context = DeleteItemRowContext(id=1, form=form)

        assert context.id == 1 and "delete_beans" in context.form
        fields = [field for field in form if field.name != "csrf_token"]
        assert [field.data for field in fields] == [False]
        assert [field.label.text for field in fields] == ["Beans"]

    def test_from_domain(self) -> None:
        item = Item(id=1, name="Beans")

        context = DeleteItemRowContext.from_domain(item)

        assert context.id == 1
        fields = [field for field in context.form if field.name != "csrf_token"]
        assert [field.data for field in fields] == [False]
        assert [field.label.text for field in fields] == ["Beans"]


@pytest.mark.usefixtures("app")
class TestAddItemForm:
    def test_create(self) -> None:
        form = AddItemForm(existing_items=[Item(id=1, name="Beans")])

        assert form.name.data is None and form.existing_items == [Item(id=1, name="Beans")]

    def test_from_domain(self) -> None:
        cupboard_items = CupboardItems()
        cupboard_items.add_item(Item(id=1, name="Beans"))

        form = AddItemForm.from_domain(cupboard_items)

        assert form.name.data is None and form.existing_items == [Item(id=1, name="Beans")]

    def test_no_errors_when_valid(self) -> None:
        form = AddItemForm(formdata=MultiDict([("csrf_token", generate_csrf()), ("name", "Beans")]), existing_items=[])

        form.validate()

        assert not form.errors

    def test_name_is_required(self) -> None:
        form = AddItemForm(formdata=MultiDict([("csrf_token", generate_csrf()), ("name", "")]), existing_items=[])

        form.validate()

        assert form.errors and form.name.errors == ["Please enter item name"]

    def test_name_must_not_be_duplicate(self) -> None:
        form = AddItemForm(
            formdata=MultiDict([("csrf_token", generate_csrf()), ("name", "Beans")]),
            existing_items=[Item(id=1, name="Beans")],
        )

        form.validate()

        assert form.errors and form.name.errors == ["Please specify an item that doesn't already exist in the cupboard"]


@pytest.mark.usefixtures("app")
class TestDeleteItemForm:
    def test_create_class_sets_label(self) -> None:
        item = Item(id=1, name="Beans")

        form_class = DeleteItemForm.create_class(item)

        form = form_class()
        assert "delete_beans" in form
        fields = [field for field in form if field.name != "csrf_token"]
        assert [field.data for field in fields] == [False]
        assert [field.label.text for field in fields] == ["Beans"]

    def test_from_domain(self) -> None:
        item = Item(id=1, name="Beans")

        form = DeleteItemForm.from_domain(item)

        assert "delete_beans" in form
        fields = [field for field in form if field.name != "csrf_token"]
        assert [field.data for field in fields] == [False]
        assert [field.label.text for field in fields] == ["Beans"]
