import pytest
from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.infrastructure import CupboardEntity
from wroblewshop.infrastructure.cupboard import DatabaseCupboardRepository


class TestDatabaseCupboardRepository:
    @pytest.fixture(name="cupboards")
    def cupboards_fixture(self, engine: Engine) -> DatabaseCupboardRepository:
        repository: DatabaseCupboardRepository = DatabaseCupboardRepository(engine=engine)
        return repository

    def test_add(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        cupboard = Cupboard(id_=1, name="Palace")

        cupboards.add(cupboard)

        cupboard_entity: CupboardEntity
        with Session(engine) as session:
            (cupboard_entity,) = session.scalars(select(CupboardEntity))

        assert cupboard_entity.id == 1 and cupboard_entity.name == "Palace"

    def test_get_by_name(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        with Session(engine) as session:
            session.add(CupboardEntity(id=1, name="Palace"))
            session.commit()

        cupboard = cupboards.get_by_name("Palace")

        assert cupboard and cupboard.id == 1 and cupboard.name == "Palace"

    def test_clear(self, engine: Engine, cupboards: DatabaseCupboardRepository) -> None:
        with Session(engine) as session:
            session.add_all([CupboardEntity(id=1, name="Palace"), CupboardEntity(id=2, name="Castle")])
            session.commit()

        cupboards.clear()

        with Session(engine) as session:
            assert session.execute(select(func.count()).select_from(CupboardEntity)).scalar_one() == 0
