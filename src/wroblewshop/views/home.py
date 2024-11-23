from __future__ import annotations

from dataclasses import asdict, dataclass

import inject
from flask import Blueprint, render_template, session

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.user import UserRepository
from wroblewshop.views.auth import secure

bp = Blueprint("home", __name__)


@bp.get("")
@secure
@inject.autoparams()
def index(cupboards: CupboardRepository, users: UserRepository) -> str:
    user_info = session["user"]
    user = users.get_by_email(user_info["email"])
    assert user
    cupboard = cupboards.get(user.cupboard)
    assert cupboard

    context = HomeContext.from_domain(cupboard)
    return render_template("home.html", **asdict(context))


@dataclass
class HomeContext:
    cupboard_name: str

    @classmethod
    def from_domain(cls, cupboard: Cupboard) -> HomeContext:
        return HomeContext(cupboard_name=cupboard.name)
