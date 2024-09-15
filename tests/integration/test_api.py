from flask import current_app
from flask.testing import FlaskClient


def test_add_users(client: FlaskClient) -> None:
    response = client.post("/user", json={"email": "foo@example.com"})

    assert response.status_code == 201
    assert "foo@example.com" in current_app.extensions["users"]


def test_delete_users(client: FlaskClient) -> None:
    current_app.extensions["users"].append("foo@example.com")
    response = client.delete("/user")

    assert response.status_code == 204
    assert not current_app.extensions["users"]
