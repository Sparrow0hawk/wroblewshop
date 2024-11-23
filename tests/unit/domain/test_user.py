from wroblewshop.domain.user import User


class TestUser:
    def test_create(self) -> None:
        user = User(email="shopper@gmail.com", cupboard="Palace")

        assert user.email == "shopper@gmail.com" and user.cupboard == "Palace"
