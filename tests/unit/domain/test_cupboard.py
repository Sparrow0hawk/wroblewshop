from wroblewshop.domain.cupboard import Cupboard


class TestCupboard:
    def test_cupboard_create(self) -> None:
        cupboard = Cupboard(id_=1, name="Palace")

        assert cupboard.id == 1 and cupboard.name == "Palace"
