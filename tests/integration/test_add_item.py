from flask.testing import FlaskClient

from tests.integration.pages import AddItemPage
from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.item import Item
from wroblewshop.domain.user import User, UserRepository


def test_add_item_page_shows_heading(users: UserRepository, cupboards: CupboardRepository, client: FlaskClient) -> None:
    cupboards.add(Cupboard(id_=1, name="Palace"))
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    add_item_page = AddItemPage.open(client)

    assert add_item_page.is_visible and add_item_page.table() == []


def test_add_item_page_shows_items(users: UserRepository, cupboards: CupboardRepository, client: FlaskClient) -> None:
    cupboard = Cupboard(id_=1, name="Palace")
    cupboard.items.add_items(*[Item(id=2, name="Beans"), Item(id=3, name="Rice")])
    cupboards.add(cupboard)
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    add_item_page = AddItemPage.open(client)

    assert add_item_page.is_visible and add_item_page.table() == [{"name": "Beans"}, {"name": "Rice"}]


def test_add_item_page_shows_confirm(users: UserRepository, cupboards: CupboardRepository, client: FlaskClient) -> None:
    cupboards.add(Cupboard(id_=1, name="Palace"))
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    add_item_page = AddItemPage.open(client)

    assert add_item_page.form.confirm_url == "/add-item"


def test_add_item_form_adds_item(
    csrf_token: str, users: UserRepository, cupboards: CupboardRepository, client: FlaskClient
) -> None:
    cupboard = Cupboard(id_=1, name="Palace")
    cupboard.items.add_item(Item(id=1, name="Sausages"))
    cupboards.add(cupboard)
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    response = client.post("/add-item", data={"csrf_token": csrf_token, "name": "Beans"})

    assert response.status_code == 302
    actual_cupboard = cupboards.get(1)
    assert actual_cupboard
    item1: Item
    item2: Item
    item1, item2 = actual_cupboard.items.item_entries
    assert item1.id == 1 and item1.name == "Sausages" and item2.name == "Beans"


def test_add_item_form_shows_items(
    csrf_token: str, users: UserRepository, cupboards: CupboardRepository, client: FlaskClient
) -> None:
    cupboard = Cupboard(id_=1, name="Palace")
    cupboard.items.add_item(Item(id=1, name="Sausages"))
    cupboards.add(cupboard)
    users.add(User(email="shopper@gmail.com", cupboard="Palace"))
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    add_item_page = AddItemPage(
        client.post("/add-item", data={"csrf_token": csrf_token, "name": "Beans"}, follow_redirects=True)
    )

    assert add_item_page.is_visible and add_item_page.table() == [{"name": "Sausages"}, {"name": "Beans"}]
