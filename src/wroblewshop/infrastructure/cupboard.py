import inject
from sqlalchemy import Engine, delete, select
from sqlalchemy.orm import Session

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.infrastructure import CupboardEntity


class DatabaseCupboardRepository(CupboardRepository):
    @inject.autoparams()
    def __init__(self, engine: Engine):
        self._engine = engine

    def add(self, *cupboards: Cupboard) -> None:
        with Session(self._engine) as session:
            for cupboard in cupboards:
                cupboard_entity = CupboardEntity(id=cupboard.id, name=cupboard.name)
                session.add(cupboard_entity)
            session.commit()

    def get(self, name: str) -> Cupboard | None:
        with Session(self._engine) as session:
            result = session.scalars(select(CupboardEntity).where(CupboardEntity.name.is_(name)))
            row = result.one_or_none()
            return Cupboard(id_=row.id, name=row.name) if row else None

    def clear(self) -> None:
        with Session(self._engine) as session:
            session.execute(delete(CupboardEntity))
            session.commit()
