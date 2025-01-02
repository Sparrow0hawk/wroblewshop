import inject
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug import Response as BaseResponse

from wroblewshop.domain.cupboard import CupboardRepository
from wroblewshop.domain.item import Item
from wroblewshop.domain.user import UserRepository
from wroblewshop.views.auth import secure

bp = Blueprint("add_item", __name__)


@bp.get("")
@secure
@inject.autoparams()
def index(cupboards: CupboardRepository, users: UserRepository) -> str:
    user_info = session["user"]
    user = users.get_by_email(user_info["email"])
    assert user
    cupboard = cupboards.get_by_name(user.cupboard)
    assert cupboard

    return render_template("add-item.html")


@bp.post("")
@secure
@inject.autoparams()
def add_item(cupboards: CupboardRepository, users: UserRepository) -> BaseResponse:
    user_info = session["user"]
    user = users.get_by_email(user_info["email"])
    assert user
    cupboard = cupboards.get_by_name(user.cupboard)
    assert cupboard

    cupboard.items.add_item(Item(id=None, name=request.form["name"]))

    cupboards.update(cupboard)
    return redirect(url_for("add_item.index"))
