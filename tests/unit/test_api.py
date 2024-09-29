from wroblewshop.views.api import UserRepr


class TestUserRepr:
    def test_create(self) -> None:
        user_repr = UserRepr(email="shopper@gmail.com")

        assert user_repr.email == "shopper@gmail.com"

    def test_to_domain(self) -> None:
        user_repr = UserRepr(email="shopper@gmail.com")

        user = user_repr.to_domain()

        assert user.email == "shopper@gmail.com"
