import pytest
from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session, selectinload

from wroblewshop.domain.user import User
from wroblewshop.infrastructure import CupboardEntity, UserEntity
from wroblewshop.infrastructure.user import DatabaseUserRepository


class TestDatabaseUserRepository:
    @pytest.fixture(name="users")
    def users_fixture(self, engine: Engine) -> DatabaseUserRepository:
        repository: DatabaseUserRepository = DatabaseUserRepository(engine=engine)
        return repository

    def test_add(self, engine: Engine, users: DatabaseUserRepository) -> None:
        with Session(engine) as session:
            session.add(CupboardEntity(id=1, name="Palace"))
            session.commit()

        users.add(
            User(email="shopper@gmail.com", cupboard="Palace"), User(email="recipemaker@gmail.com", cupboard="Palace")
        )

        user1: UserEntity
        user2: UserEntity
        with Session(engine) as session:
            user1, user2 = session.scalars(select(UserEntity).options(selectinload("*")))

        assert (
            user1.email == "shopper@gmail.com"
            and user1.cupboard_id == 1
            and user2.email == "recipemaker@gmail.com"
            and user2.cupboard_id == 1
        )

    def test_get_by_email(self, engine: Engine, users: DatabaseUserRepository) -> None:
        with Session(engine) as session:
            session.add(CupboardEntity(id=1, name="Palace"))
            session.add(UserEntity(email="shopper@gmail.com", cupboard_id=1))
            session.commit()

        user = users.get_by_email(email="shopper@gmail.com")

        assert user and user.email == "shopper@gmail.com" and user.cupboard == "Palace"

    def test_clear(self, engine: Engine, users: DatabaseUserRepository) -> None:
        with Session(engine) as session:
            session.add(CupboardEntity(id=1, name="Palace"))
            session.add(UserEntity(email="shopper@gmail.com", cupboard_id=1))
            session.add(UserEntity(email="recipemaker@gmail.com", cupboard_id=1))
            session.commit()

        users.clear()

        with Session(engine) as session:
            assert session.execute(select(func.count()).select_from(UserEntity)).scalar_one() == 0
