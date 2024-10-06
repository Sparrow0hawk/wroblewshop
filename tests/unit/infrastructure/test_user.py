import pytest
from sqlalchemy import Engine, create_engine, func, select
from sqlalchemy.orm import Session

from wroblewshop.domain.user import User
from wroblewshop.infrastructure import Base, UserEntity
from wroblewshop.infrastructure.user import DatabaseUserRepository


class TestDatabaseUserRepository:
    @pytest.fixture(name="engine")
    def engine_fixture(self) -> Engine:
        engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    @pytest.fixture(name="users")
    def users_fixture(self, engine: Engine) -> DatabaseUserRepository:
        repository: DatabaseUserRepository = DatabaseUserRepository(engine=engine)
        return repository

    def test_add(self, engine: Engine, users: DatabaseUserRepository) -> None:
        users.add(User(email="shopper@gmail.com"), User("recipemaker@gmail.com"))

        user1: UserEntity
        user2: UserEntity
        with Session(engine) as session:
            user1, user2 = session.scalars(select(UserEntity))

        assert user1.email == "shopper@gmail.com" and user2.email == "recipemaker@gmail.com"

    def test_get_by_email(self, engine: Engine, users: DatabaseUserRepository) -> None:
        with Session(engine) as session:
            session.add(UserEntity(email="shopper@gmail.com"))
            session.commit()

        user = users.get_by_email(email="shopper@gmail.com")
        assert user and user.email == "shopper@gmail.com"

    def test_clear(self, engine: Engine, users: DatabaseUserRepository) -> None:
        with Session(engine) as session:
            session.add(UserEntity(email="shopper@gmail.com"))
            session.add(UserEntity(email="recipemaker@gmail.com"))
            session.commit()

        users.clear()

        with Session(engine) as session:
            assert session.execute(select(func.count()).select_from(UserEntity)).scalar_one() == 0
