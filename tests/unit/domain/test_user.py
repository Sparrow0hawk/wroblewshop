from wroblewshop.domain.user import User


def test_user_create() -> None:
    user = User(email="shopper@gmail.com", cupboard="Palace")

    assert user.email == "shopper@gmail.com" and user.cupboard == "Palace"
