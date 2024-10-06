from collections.abc import Mapping
from typing import Any, Callable

import flask_session
import inject
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inject import Binder
from sqlalchemy import Engine
from werkzeug.middleware.proxy_fix import ProxyFix

from wroblewshop.domain.user import User, UserRepository
from wroblewshop.infrastructure import Base
from wroblewshop.infrastructure.user import DatabaseUserRepository
from wroblewshop.views import api, auth, home, start


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, static_folder="views/static", template_folder="views/templates")
    app.config.from_object("wroblewshop.config.Config")
    app.config.from_prefixed_env()

    if test_config:
        app.config.from_mapping(test_config)

    inject.configure(bindings(app), bind_in_runtime=False)

    app.config["SESSION_SQLALCHEMY"] = SQLAlchemy(app)
    flask_session.Session(app)

    _create_database()

    _configure_oidc(app)
    _configure_users(app)

    app.register_blueprint(start.bp)
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(home.bp, url_prefix="/home")
    if app.testing:
        app.register_blueprint(api.bp)

    app.wsgi_app = ProxyFix(app.wsgi_app)  # type: ignore

    return app


def bindings(app: Flask) -> Callable[[Binder], None]:
    def _bindings(binder: Binder) -> None:
        binder.bind(Flask, app)
        binder.bind_to_constructor(Engine, _create_engine)
        binder.bind_to_constructor(UserRepository, DatabaseUserRepository)

    return _bindings


@inject.autoparams()
def _create_engine(app: Flask) -> Engine:
    flask_sqlalchemy_extension: SQLAlchemy = app.extensions["sqlalchemy"]
    with app.app_context():
        engine = flask_sqlalchemy_extension.engine
    return engine


@inject.autoparams()
def _create_database(engine: Engine) -> None:
    Base.metadata.create_all(engine)


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
