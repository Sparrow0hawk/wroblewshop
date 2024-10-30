from flask import Blueprint, render_template

from wroblewshop.views.auth import secure

bp = Blueprint("add_item", __name__)


@bp.get("")
@secure
def index() -> str:
    return render_template("add-item.html")
