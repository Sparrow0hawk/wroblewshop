from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.domain.item import Item
from wroblewshop.views.api import CupboardRepr, ItemRepr, UserRepr


class TestUserRepr:
    def test_create(self) -> None:
        user_repr = UserRepr(email="shopper@gmail.com", cupboard="Palace")

        assert user_repr.email == "shopper@gmail.com" and user_repr.cupboard == "Palace"

    def test_to_domain(self) -> None:
        user_repr = UserRepr(email="shopper@gmail.com", cupboard="Palace")

        user = user_repr.to_domain()

        assert user.email == "shopper@gmail.com" and user.cupboard == "Palace"


class TestCupboardRepr:
    def test_create(self) -> None:
        cupboard_repr = CupboardRepr(id=1, name="Palace", items=[ItemRepr(id=2, name="Beans")])

        assert (
            cupboard_repr.id == 1
            and cupboard_repr.name == "Palace"
            and cupboard_repr.items
            and cupboard_repr.items[0] == ItemRepr(id=2, name="Beans")
        )

    def test_to_domain(self) -> None:
        cupboard_repr = CupboardRepr(id=1, name="Palace", items=[ItemRepr(id=2, name="Beans")])

        cupboard = cupboard_repr.to_domain()

        assert cupboard.id == 1 and cupboard.name == "Palace"
        item: Item
        (item,) = cupboard.items.item_entries
        assert item.id == 2 and item.name == "Beans"

    def test_to_domain_when_no_items(self) -> None:
        cupboard_repr = CupboardRepr(id=1, name="Palace", items=None)

        cupboard = cupboard_repr.to_domain()

        assert cupboard.id == 1 and cupboard.name == "Palace" and cupboard.items.item_entries == []

    def test_from_domain(self) -> None:
        cupboard = Cupboard(id_=1, name="Palace")
        cupboard.items.add_items(*[Item(id=2, name="Beans"), Item(id=3, name="Rice")])

        cupboard_repr = CupboardRepr.from_domain(cupboard)

        assert cupboard_repr.id == 1 and cupboard_repr.name == "Palace" and cupboard_repr.items
        item_repr1: ItemRepr
        item_repr2: ItemRepr
        item_repr1, item_repr2 = cupboard_repr.items
        assert item_repr1.id == 2 and item_repr1.name == "Beans" and item_repr2.id == 3 and item_repr2.name == "Rice"


class TestItemRepr:
    def test_create(self) -> None:
        item_repr = ItemRepr(id=1, name="Beans")

        assert item_repr.id == 1 and item_repr.name == "Beans"

    def test_to_domain(self) -> None:
        item_repr = ItemRepr(id=1, name="Beans")

        item = item_repr.to_domain()

        assert item.id == 1 and item.name == "Beans"

    def test_from_domain(self) -> None:
        item = Item(id=1, name="Beans")

        item_repr = ItemRepr.from_domain(item)

        assert item_repr.id == 1 and item_repr.name == "Beans"
