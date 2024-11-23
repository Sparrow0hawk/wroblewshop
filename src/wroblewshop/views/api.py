from dataclasses import dataclass

import inject
from flask import Blueprint, Response, request

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.user import User, UserRepository

bp = Blueprint("api", __name__)


@bp.post("/user")
@inject.autoparams()
def add_user(users: UserRepository) -> Response:
    user_repr = UserRepr(email=request.get_json()["email"], cupboard=request.get_json()["cupboard"])
    users.add(user_repr.to_domain())
    return Response(status=201)


@bp.delete("/user")
@inject.autoparams()
def delete_user(users: UserRepository) -> Response:
    users.clear()
    return Response(status=204)


@bp.post("/cupboard")
@inject.autoparams()
def add_cupboard(cupboards: CupboardRepository) -> Response:
    cupboard_repr = CupboardRepr(id=request.get_json()["id"], name=request.get_json()["name"])
    cupboards.add(cupboard_repr.to_domain())
    return Response(status=201)


@bp.delete("/cupboard")
@inject.autoparams()
def delete_cupboard(cupboards: CupboardRepository) -> Response:
    cupboards.clear()
    return Response(status=204)


@dataclass
class UserRepr:
    email: str
    cupboard: str

    def to_domain(self) -> User:
        return User(email=self.email, cupboard=self.cupboard)


@dataclass
class CupboardRepr:
    id: int
    name: str

    def to_domain(self) -> Cupboard:
        return Cupboard(id_=self.id, name=self.name)
