from dataclasses import dataclass

import inject
from flask import Blueprint, Response, request

from wroblewshop.domain.user import User, UserRepository

bp = Blueprint("api", __name__)


@bp.post("/user")
@inject.autoparams()
def add_user(users: UserRepository) -> Response:
    user_repr = UserRepr(request.get_json()["email"])
    users.add(user_repr.to_domain())
    return Response(status=201)


@bp.delete("/user")
@inject.autoparams()
def delete_user(users: UserRepository) -> Response:
    users.clear()
    return Response(status=204)


@dataclass
class UserRepr:
    email: str

    def to_domain(self) -> User:
        return User(email=self.email)
