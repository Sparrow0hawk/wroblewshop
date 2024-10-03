from collections.abc import Mapping
from typing import Any

import flask_session
import inject
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inject import Binder
from werkzeug.middleware.proxy_fix import ProxyFix

from wroblewshop.domain.user import User, UserRepository
from wroblewshop.infrastructure.user import DatabaseUserRepository
from wroblewshop.views import api, auth, home, start


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, static_folder="views/static", template_folder="views/templates")
    app.config.from_object("wroblewshop.config.Config")
    app.config.from_prefixed_env()

    if test_config:
        app.config.from_mapping(test_config)

    inject.configure(_bindings, bind_in_runtime=False)

    app.config["SESSION_SQLALCHEMY"] = SQLAlchemy(app)
    flask_session.Session(app)

    _configure_oidc(app)
    _configure_users(app)

    app.register_blueprint(start.bp)
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(home.bp, url_prefix="/home")
    if app.testing:
        app.register_blueprint(api.bp)

    app.wsgi_app = ProxyFix(app.wsgi_app)  # type: ignore

    return app


def _bindings(binder: Binder) -> None:
    binder.bind_to_constructor(UserRepository, DatabaseUserRepository)


def _configure_oidc(app: Flask) -> None:
    oauth = OAuth(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
        client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
        server_metadata_url=app.config["GOOGLE_SERVER_METADATA_URL"],
        client_kwargs={
            "scope": "openid email",
        },
    )


@inject.autoparams("users")
def _configure_users(app: Flask, users: UserRepository) -> None:
    if app.config.get("USERS"):
        users.add(*[User(email=email) for email in app.config["USERS"].split(",")])
