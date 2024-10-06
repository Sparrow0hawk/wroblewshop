import inject
from sqlalchemy import Engine, delete, select
from sqlalchemy.orm import Session

from wroblewshop.domain.user import User, UserRepository
from wroblewshop.infrastructure import UserEntity


class DatabaseUserRepository(UserRepository):
    @inject.autoparams()
    def __init__(self, engine: Engine):
        self._engine = engine

    def add(self, *users: User) -> None:
        with Session(self._engine) as session:
            for user in users:
                session.add(UserEntity(email=user.email))
            session.commit()

    def get_by_email(self, email: str) -> User | None:
        with Session(self._engine) as session:
            result = session.scalars(select(UserEntity).where(UserEntity.email == email))
            row = result.one_or_none()
            return User(email=row.email) if row else None

    def clear(self) -> None:
        with Session(self._engine) as session:
            session.execute(delete(UserEntity))
            session.commit()
