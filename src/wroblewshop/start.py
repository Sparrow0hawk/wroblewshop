from flask import Blueprint, render_template

bp = Blueprint("start", __name__)


@bp.get("/")
def index() -> str:
    return render_template("start.html")
