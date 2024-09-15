from flask import Blueprint, Response, current_app, request

bp = Blueprint("api", __name__)


@bp.post("/user")
def add_user() -> Response:
    email = request.get_json()["email"]
    current_app.extensions["users"].append(email)
    return Response(status=201)


@bp.delete("/user")
def delete_user() -> Response:
    current_app.extensions["users"].clear()
    return Response(status=204)
