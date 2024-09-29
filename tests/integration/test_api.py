from flask import current_app
from flask.testing import FlaskClient

from wroblewshop.domain.user import User, UserRepository


def test_add_users(client: FlaskClient) -> None:
    response = client.post("/user", json={"email": "foo@example.com"})

    assert response.status_code == 201
    users: UserRepository = current_app.extensions["users"]
    assert users.get_by_email("foo@example.com")


def test_delete_users(client: FlaskClient) -> None:
    users: UserRepository = current_app.extensions["users"]
    users.add(User(email="foo@example.com"))
    response = client.delete("/user")

    assert response.status_code == 204
    assert not users.get_all()
