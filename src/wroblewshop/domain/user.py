class User:
    def __init__(self, email: str, cupboard: str):
        self.email = email
        self.cupboard = cupboard


class UserRepository:
    def add(self, *users: User) -> None:
        raise NotImplementedError()

    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError()

    def get_all(self) -> list[User]:
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()
