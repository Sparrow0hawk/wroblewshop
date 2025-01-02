from flask.testing import FlaskClient

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.item import Item
from wroblewshop.domain.user import User, UserRepository


def test_add_users(client: FlaskClient, users: UserRepository) -> None:
    response = client.post("/user", json={"email": "foo@example.com", "cupboard": "Palace"})

    assert response.status_code == 201
    user = users.get_by_email("foo@example.com")
    assert user and user.cupboard == "Palace"


def test_delete_users(client: FlaskClient, users: UserRepository) -> None:
    users.add(User(email="foo@example.com", cupboard="Palace"))
    response = client.delete("/user")

    assert response.status_code == 204
    assert not users.get_all()


def test_add_cupboard(client: FlaskClient, cupboards: CupboardRepository) -> None:
    response = client.post("/cupboard", json={"id": 1, "name": "Palace", "items": [{"id": 2, "name": "Beans"}]})

    assert response.status_code == 201
    (cupboard,) = cupboards.get_all()
    assert cupboard and cupboard.id == 1 and cupboard.name == "Palace"
    (item,) = cupboard.items.item_entries
    assert item.id == 2 and item.name == "Beans"


def test_get_cupboard(client: FlaskClient, cupboards: CupboardRepository) -> None:
    cupboard = Cupboard(id_=1, name="Palace")
    cupboard.items.add_item(Item(id=2, name="Beans"))
    cupboards.add(cupboard)
    response = client.get("/cupboard/1")

    assert response.json == {"id": 1, "name": "Palace", "items": [{"id": 2, "name": "Beans"}]}


def test_delete_cupboards(client: FlaskClient, cupboards: CupboardRepository) -> None:
    response = client.delete("/cupboard")

    assert response.status_code == 204
    assert not cupboards.get_all()
