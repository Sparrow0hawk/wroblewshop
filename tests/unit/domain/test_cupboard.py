from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.domain.item import CupboardItems


class TestCupboard:
    def test_cupboard_create(self) -> None:
        cupboard = Cupboard(id_=1, name="Palace")

        assert cupboard.id == 1 and cupboard.name == "Palace" and isinstance(cupboard.items, CupboardItems)
