from wroblewshop.domain.item import CupboardItems, Item


class TestCupboardItems:
    def test_create(self) -> None:
        cupboard_items = CupboardItems()

        assert not cupboard_items._items

    def test_item_entries_is_copy(self) -> None:
        cupboard_items = CupboardItems()
        cupboard_items.add_item(Item(id=1, name="Beans"))

        cupboard_items.item_entries.clear()

        assert cupboard_items.item_entries

    def test_add_item(self) -> None:
        cupboard_items = CupboardItems()

        cupboard_items.add_item(Item(id=1, name="Beans"))

        assert cupboard_items._items == [Item(id=1, name="Beans")]

    def test_add_items(self) -> None:
        cupboard_items = CupboardItems()

        cupboard_items.add_items(*[Item(id=1, name="Beans"), Item(id=2, name="Rice")])

        assert cupboard_items._items == [Item(id=1, name="Beans"), Item(id=2, name="Rice")]


class TestItem:
    def test_create(self) -> None:
        item = Item(id=1, name="Beans")

        assert item.id == 1 and item.name == "Beans"
