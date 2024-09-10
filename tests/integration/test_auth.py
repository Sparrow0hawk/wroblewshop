from authlib.oidc.core import UserInfo
from flask.testing import FlaskClient


def test_logout_logs_out_from_oidc(client: FlaskClient) -> None:
    with client.session_transaction() as setup_session:
        setup_session["user"] = UserInfo({"email": "boardman@example.com"})
        setup_session["id_token"] = "jwt"

    response = client.get("/auth/logout")

    assert (
            response.status_code == 302 and
            response.location == "/"
    )
