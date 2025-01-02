import inject
from sqlalchemy import Engine, delete, select
from sqlalchemy.orm import Session

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.item import Item
from wroblewshop.infrastructure import CupboardEntity, ItemEntity


class DatabaseCupboardRepository(CupboardRepository):
    @inject.autoparams()
    def __init__(self, engine: Engine):
        self._engine = engine

    def add(self, *cupboards: Cupboard) -> None:
        with Session(self._engine) as session:
            for cupboard in cupboards:
                cupboard_entity = self._cupboard_to_entity(cupboard)
                session.add(cupboard_entity)
            session.commit()

    def get(self, id_: int) -> Cupboard | None:
        with Session(self._engine) as session:
            result = session.scalars(select(CupboardEntity).where(CupboardEntity.id == id_))
            row = result.one_or_none()
            return self._cupboard_from_entity(row) if row else None

    def get_by_name(self, name: str) -> Cupboard | None:
        with Session(self._engine) as session:
            result = session.scalars(select(CupboardEntity).where(CupboardEntity.name == name))
            row = result.one_or_none()
            return self._cupboard_from_entity(row) if row else None

    def update(self, cupboard: Cupboard) -> None:
        with Session(self._engine) as session:
            session.merge(self._cupboard_to_entity(cupboard))
            session.commit()

    def clear(self) -> None:
        with Session(self._engine) as session:
            session.execute(delete(ItemEntity))
            session.execute(delete(CupboardEntity))
            session.commit()

    def _cupboard_from_entity(self, cupboard_entity: CupboardEntity) -> Cupboard:
        cupboard = Cupboard(id_=cupboard_entity.id, name=cupboard_entity.name)
        for item in cupboard_entity.items:
            cupboard.items.add_item(Item(id=item.id, name=item.name))
        return cupboard

    def _cupboard_to_entity(self, cupboard: Cupboard) -> CupboardEntity:
        cupboard_entity = CupboardEntity(id=cupboard.id, name=cupboard.name)
        for item in cupboard.items.item_entries:
            cupboard_entity.items.append(ItemEntity(id=item.id, name=item.name, cupboard_id=cupboard.id))
        return cupboard_entity
