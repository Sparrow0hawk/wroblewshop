import pytest

from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.domain.item import Item
from wroblewshop.views.items import AddItemContext, AddItemForm, ItemRowContext


@pytest.mark.usefixtures("app")
class TestAddItemContext:
    def test_create(self) -> None:
        context = AddItemContext(items=[ItemRowContext(name="Beans")], form=AddItemForm())

        assert context.items == [ItemRowContext(name="Beans")] and context.form.name.data is None

    def test_from_domain(self) -> None:
        cupboard = Cupboard(id_=0, name="")
        cupboard.items.add_items(*[Item(id=1, name="Beans"), Item(id=2, name="Rice")])

        context = AddItemContext.from_domain(cupboard)

        assert context.form.name.data is None
        item1: ItemRowContext
        item2: ItemRowContext
        (item1, item2) = context.items
        assert item1.name == "Beans" and item2.name == "Rice"


class TestItemRowContext:
    def test_create(self) -> None:
        context = ItemRowContext(name="Beans")

        assert context.name == "Beans"

    def test_from_domain(self) -> None:
        item = Item(id=1, name="Beans")

        context = ItemRowContext.from_domain(item)

        assert context.name == "Beans"
