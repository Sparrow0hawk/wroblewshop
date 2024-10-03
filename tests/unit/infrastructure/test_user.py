import pytest

from wroblewshop.domain.user import User
from wroblewshop.infrastructure.user import DatabaseUserRepository


class TestDatabaseUserRepository:
    @pytest.fixture(name="users")
    def users_fixture(self) -> DatabaseUserRepository:
        return DatabaseUserRepository()

    def test_add(self, users: DatabaseUserRepository) -> None:
        users.add(User(email="shopper@gmail.com"))

        user: User
        (user,) = users._users
        assert user.email == "shopper@gmail.com"

    def test_get_by_email(self, users: DatabaseUserRepository) -> None:
        users._users.append(User(email="shopper@gmail.com"))

        user = users.get_by_email(email="shopper@gmail.com")
        assert user and user.email == "shopper@gmail.com"

    def test_clear(self, users: DatabaseUserRepository) -> None:
        users._users.extend([User(email="shopper@gmail.com"), User(email="recipemaker@gmail.com")])

        users.clear()

        assert not users._users
