from functools import wraps
from typing import Callable

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, Response, current_app, redirect, session, url_for
from typing_extensions import ParamSpec, TypeVar
from werkzeug import Response as BaseResponse

bp = Blueprint("auth", __name__)


@bp.get("")
def callback() -> BaseResponse:
    oauth = _get_oauth()
    # TODO: flask test for checking iss and aud
    server_metadata = oauth.google.load_server_metadata()
    token = oauth.google.authorize_access_token(
        claims_options={
            "iss": {"value": server_metadata.get("issuer")},
            "aud": {"value": oauth.google.client_id},
        }
    )
    session["user"] = oauth.google.userinfo(token=token)
    return redirect(url_for("home.index"))


@bp.get("/logout")
def logout() -> BaseResponse:
    session.pop("user", None)
    return redirect(url_for("start.index"))


T = TypeVar("T")
P = ParamSpec("P")


def secure(func: Callable[P, T]) -> Callable[P, T | Response]:
    @wraps(func)
    def decorated_function(*args: P.args, **kwargs: P.kwargs) -> T | Response:
        if "user" not in session:
            oauth = _get_oauth()
            callback_url = url_for("auth.callback", _external=True)
            response: Response = oauth.google.authorize_redirect(callback_url)
            return response
        return func(*args, **kwargs)

    return decorated_function


def _get_oauth() -> OAuth:
    return current_app.extensions["authlib.integrations.flask_client"]
