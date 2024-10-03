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
