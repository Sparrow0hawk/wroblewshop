from flask.testing import FlaskClient

from tests.integration.pages import AddItemPage


def test_add_item_shows_heading(client: FlaskClient) -> None:
    with client.session_transaction() as session:
        session["user"] = {"email": "shopper@gmail.com"}

    add_item_page = AddItemPage.open(client)

    assert add_item_page.is_visible
