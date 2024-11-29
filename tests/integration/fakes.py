from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
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

    def get_by_name(self, name: str) -> Cupboard | None:
        cupboard_by_name = (cupboard for cupboard in self._cupboards.values() if cupboard.name == name)
        return next(cupboard_by_name, None)

    def get_all(self) -> list[Cupboard]:
        return [cupboard for cupboard in self._cupboards.values()]

    def clear(self) -> None:
        self._cupboards.clear()
