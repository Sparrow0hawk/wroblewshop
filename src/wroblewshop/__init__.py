import os
from collections.abc import Mapping
from typing import Any, Callable

import alembic.config
import flask_session
import inject
from alembic import command
from authlib.integrations.flask_client import OAuth
from flask import Flask, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from inject import Binder
from sqlalchemy import Engine, event
from sqlalchemy.dialects.sqlite.base import SQLiteDialect
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.pool import ConnectionPoolEntry
from werkzeug import Response as BaseResponse
from werkzeug.middleware.proxy_fix import ProxyFix

from wroblewshop.config import LocalConfig
from wroblewshop.domain.cupboard import CupboardRepository
from wroblewshop.domain.user import UserRepository
from wroblewshop.infrastructure.cupboard import DatabaseCupboardRepository
from wroblewshop.infrastructure.user import DatabaseUserRepository
from wroblewshop.views import api, auth, home, item, start


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    env = os.getenv("FLASK_ENV", LocalConfig.NAME)

    app = Flask(__name__, static_folder="views/static", template_folder="views/templates")
    app.config.from_object(f"wroblewshop.config.{env.title()}Config")
    app.config.from_prefixed_env()

    if test_config:
        app.config.from_mapping(test_config)

    inject.configure(bindings(app), bind_in_runtime=False)

    app.config["SESSION_SQLALCHEMY"] = SQLAlchemy(app)
    flask_session.Session(app)
    csrf = CSRFProtect(app)

    _create_database()
    _configure_error_pages(app)

    _configure_oidc(app)

    app.register_blueprint(start.bp)
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(home.bp, url_prefix="/home")
    app.register_blueprint(item.bp, url_prefix="/item")
    if app.testing:
        app.register_blueprint(api.bp)
        csrf.exempt(api.bp)

    app.wsgi_app = ProxyFix(app.wsgi_app)  # type: ignore

    return app


def bindings(app: Flask) -> Callable[[Binder], None]:
    def _bindings(binder: Binder) -> None:
        binder.bind(Flask, app)
        binder.bind_to_constructor(Engine, _create_engine)
        binder.bind_to_constructor(UserRepository, DatabaseUserRepository)
        binder.bind_to_constructor(CupboardRepository, DatabaseCupboardRepository)

    return _bindings


@inject.autoparams()
def _create_engine(app: Flask) -> Engine:
    flask_sqlalchemy_extension: SQLAlchemy = app.extensions["sqlalchemy"]
    with app.app_context():
        engine = flask_sqlalchemy_extension.engine

    if engine.dialect.name == SQLiteDialect.name:
        event.listen(engine, "connect", _enforce_sqlite_foreign_keys)

    return engine


def _enforce_sqlite_foreign_keys(dbapi_connection: DBAPIConnection, _connection_record: ConnectionPoolEntry) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@inject.autoparams()
def _create_database(engine: Engine) -> None:
    alembic_config = alembic.config.Config()

    alembic_config.set_main_option("script_location", "wroblewshop:infrastructure:migrations")

    with engine.connect() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")


def _configure_error_pages(app: Flask) -> None:
    @app.errorhandler(CSRFError)
    def csrf_error(_error: CSRFError) -> BaseResponse:
        flash("The form you were submitting has expired. Please try again.")
        return redirect(request.referrer)


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
