from dataclasses import dataclass

from flask import Blueprint, Response, current_app, request

from wroblewshop.domain.user import User, UserRepository

bp = Blueprint("api", __name__)


@bp.post("/user")
def add_user() -> Response:
    users: UserRepository = current_app.extensions["users"]
    user_repr = UserRepr(request.get_json()["email"])
    users.add(user_repr.to_domain())
    return Response(status=201)


@bp.delete("/user")
def delete_user() -> Response:
    current_app.extensions["users"].clear()
    return Response(status=204)


@dataclass
class UserRepr:
    email: str

    def to_domain(self) -> User:
        return User(email=self.email)
