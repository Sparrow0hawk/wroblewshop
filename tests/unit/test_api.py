from wroblewshop.views.api import CupboardRepr, UserRepr


class TestUserRepr:
    def test_create(self) -> None:
        user_repr = UserRepr(email="shopper@gmail.com", cupboard="Palace")

        assert user_repr.email == "shopper@gmail.com" and user_repr.cupboard == "Palace"

    def test_to_domain(self) -> None:
        user_repr = UserRepr(email="shopper@gmail.com", cupboard="Palace")

        user = user_repr.to_domain()

        assert user.email == "shopper@gmail.com" and user.cupboard == "Palace"


class TestCupboardRepr:
    def test_create(self) -> None:
        cupboard_repr = CupboardRepr(id=1, name="Palace")

        assert cupboard_repr.id == 1 and cupboard_repr.name == "Palace"

    def test_to_domain(self) -> None:
        cupboard_repr = CupboardRepr(id=1, name="Palace")

        cupboard = cupboard_repr.to_domain()

        assert cupboard.id == 1 and cupboard.name == "Palace"
