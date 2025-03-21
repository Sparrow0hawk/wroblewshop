from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import inject
from authlib.integrations.flask_client import OAuth
from authlib.oidc.core import UserInfo
from flask import (
    Blueprint,
    Response,
    current_app,
    redirect,
    render_template,
    session,
    url_for,
)
from werkzeug import Response as BaseResponse

from wroblewshop.domain.user import UserRepository

bp = Blueprint("auth", __name__)


@bp.get("")
@inject.autoparams()
def callback(users: UserRepository) -> BaseResponse:
    oauth = _get_oauth()
    # TODO: flask test for checking iss and aud
    server_metadata = oauth.google.load_server_metadata()
    token = oauth.google.authorize_access_token(
        claims_options={
            "iss": {"value": server_metadata.get("issuer")},
            "aud": {"value": oauth.google.client_id},
        }
    )
    user = oauth.google.userinfo(token=token)

    if not _is_authorised(user, users):
        return redirect(url_for("auth.forbidden"))

    session["user"] = user

    return redirect(url_for("home.index"))


def _is_authorised(user: UserInfo, users: UserRepository) -> bool:
    return users.get_by_email(user["email"]) is not None


@bp.get("/forbidden")
def forbidden() -> Response:
    return Response(render_template("forbidden.html"), status=403)


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
