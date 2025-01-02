from __future__ import annotations

from dataclasses import asdict, dataclass

import inject
from flask import Blueprint, Response, make_response, request

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.item import Item
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
    request_json = request.get_json()
    items = request_json.get("items")
    cupboard_repr = CupboardRepr(
        id=request_json.get("id"),
        name=request_json.get("name"),
        items=[ItemRepr(id=item["id"], name=item["name"]) for item in items] if items else None,
    )
    cupboards.add(cupboard_repr.to_domain())
    return Response(status=201)


@bp.get("/cupboard/<int:cupboard_id>")
@inject.autoparams()
def get_cupboard(cupboard_id: int, cupboards: CupboardRepository) -> Response:
    cupboard = cupboards.get(cupboard_id)
    assert cupboard
    cupboard_repr = CupboardRepr.from_domain(cupboard)
    response = make_response(asdict(cupboard_repr))
    response.content_type = "application/json"
    return response


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
    items: list[ItemRepr] | None

    def to_domain(self) -> Cupboard:
        cupboard = Cupboard(id_=self.id, name=self.name)
        if self.items:
            cupboard.items.add_items(*[item_repr.to_domain() for item_repr in self.items])
        return cupboard

    @classmethod
    def from_domain(cls, cupboard: Cupboard) -> CupboardRepr:
        return CupboardRepr(
            id=cupboard.id,
            name=cupboard.name,
            items=[ItemRepr.from_domain(item) for item in cupboard.items.item_entries],
        )


@dataclass
class ItemRepr:
    id: int | None
    name: str

    def to_domain(self) -> Item:
        return Item(id=self.id, name=self.name)

    @classmethod
    def from_domain(cls, item: Item) -> ItemRepr:
        return ItemRepr(id=item.id, name=item.name)
