from collections.abc import Mapping
from typing import Any

from flask import Flask

from wroblewshop import start


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)

    app.register_blueprint(start.bp)

    return app
