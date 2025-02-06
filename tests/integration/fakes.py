from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.item import Item
from wroblewshop.domain.user import User, UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: list[User] = []

    def add(self, *users: User) -> None:
        for user in users:
            self._users.append(user)

    def get_by_email(self, email: str) -> User | None:
        return next((user for user in self._users if user.email == email), None)

    def get_all(self) -> list[User]:
        return [user for user in self._users]

    def clear(self) -> None:
        self._users.clear()


class InMemoryCupboardRepository(CupboardRepository):
    def __init__(self) -> None:
        self._cupboards: dict[int, Cupboard] = {}

    def add(self, cupboard: Cupboard) -> None:
        self._cupboards[cupboard.id] = cupboard

    def get(self, id_: int) -> Cupboard | None:
        return self._cupboards.get(id_)

    def get_by_name(self, name: str) -> Cupboard | None:
        cupboard_by_name = (cupboard for cupboard in self._cupboards.values() if cupboard.name == name)
        return next(cupboard_by_name, None)

    def get_all(self) -> list[Cupboard]:
        return [cupboard for cupboard in self._cupboards.values()]

    def update(self, cupboard: Cupboard) -> None:
        self._enforce_item_ids(cupboard)
        self._cupboards[cupboard.id] = cupboard

    def clear(self) -> None:
        self._cupboards.clear()

    @staticmethod
    def _enforce_item_ids(cupboard: Cupboard) -> None:
        def _get_next_id(item_ids: list[int | None]) -> int:
            return max([id_ for id_ in item_ids if id_ is not None]) + 1

        item_ids = [item.id for item in cupboard.items.item_entries]
        if None in item_ids:
            item_with_no_id = next(item for item in cupboard.items.item_entries if not item.id)
            replacement_item = Item(id=_get_next_id(item_ids), name=item_with_no_id.name)

            cupboard.items._items = [item for item in cupboard.items.item_entries if item.id is not None] + [
                replacement_item
            ]
