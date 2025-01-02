import pytest
from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.domain.item import Item
from wroblewshop.infrastructure import CupboardEntity, ItemEntity
from wroblewshop.infrastructure.cupboard import DatabaseCupboardRepository


class TestDatabaseCupboardRepository:
    @pytest.fixture(name="cupboards")
    def cupboards_fixture(self, engine: Engine) -> DatabaseCupboardRepository:
        repository: DatabaseCupboardRepository = DatabaseCupboardRepository(engine=engine)
        return repository

    def test_add(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        cupboard = Cupboard(id_=1, name="Palace")
        cupboard.items.add_item(Item(id=2, name="Beans"))

        cupboards.add(cupboard)

        cupboard_entity: CupboardEntity
        with Session(engine) as session:
            (cupboard_entity,) = session.scalars(select(CupboardEntity))

            assert cupboard_entity.id == 1 and cupboard_entity.name == "Palace"
            item_entity: ItemEntity
            (item_entity,) = cupboard_entity.items
            assert item_entity.id == 2 and item_entity.name == "Beans" and item_entity.cupboard_id == 1

    def test_get(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        with Session(engine) as session:
            session.add_all(
                [
                    CupboardEntity(id=1, name="Palace"),
                    ItemEntity(id=2, name="Beans", cupboard_id=1),
                    ItemEntity(id=3, name="Rice", cupboard_id=1),
                ]
            )
            session.commit()

        cupboard = cupboards.get(1)

        assert cupboard and cupboard.id == 1 and cupboard.name == "Palace"
        item1: Item
        item2: Item
        item1, item2 = cupboard.items.item_entries
        assert item1.id == 2 and item1.name == "Beans" and item2.id == 3 and item2.name == "Rice"

    def test_get_by_name(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        with Session(engine) as session:
            session.add(CupboardEntity(id=1, name="Palace"))
            session.add(ItemEntity(id=2, name="Beans", cupboard_id=1))
            session.add(ItemEntity(id=3, name="Rice", cupboard_id=1))
            session.commit()

        cupboard = cupboards.get_by_name("Palace")

        assert cupboard and cupboard.id == 1 and cupboard.name == "Palace"
        item1: Item
        item2: Item
        item1, item2 = cupboard.items.item_entries
        assert item1.id == 2 and item1.name == "Beans" and item2.id == 3 and item2.name == "Rice"

    def test_update(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        with Session(engine) as session:
            session.add(CupboardEntity(id=1, name="Palace"))
            session.add(ItemEntity(id=2, name="Beans", cupboard_id=1))
            session.commit()

        cupboard = cupboards.get(1)
        assert cupboard
        cupboard.items.add_item(Item(id=3, name="Rice"))

        cupboards.update(cupboard)

        with Session(engine) as session:
            cupboard_entity: CupboardEntity
            (cupboard_entity,) = session.scalars(select(CupboardEntity))

            assert cupboard_entity.id == 1 and cupboard_entity.name == "Palace"
            item_entity1: ItemEntity
            item_entity2: ItemEntity
            item_entity1, item_entity2 = cupboard_entity.items
            assert item_entity1.id == 2 and item_entity1.name == "Beans" and item_entity1.cupboard_id == 1
            assert item_entity2.id == 3 and item_entity2.name == "Rice" and item_entity2.cupboard_id == 1

    def test_clear(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        with Session(engine) as session:
            session.add_all([CupboardEntity(id=1, name="Palace"), CupboardEntity(id=2, name="Castle")])
            session.add_all(
                [ItemEntity(id=3, name="Beans", cupboard_id=1), ItemEntity(id=4, name="Rice", cupboard_id=2)]
            )
            session.commit()

        cupboards.clear()

        with Session(engine) as session:
            assert session.execute(select(func.count()).select_from(CupboardEntity)).scalar_one() == 0
            assert session.execute(select(func.count()).select_from(ItemEntity)).scalar_one() == 0
