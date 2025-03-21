from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any

import inject
from flask import Blueprint, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from werkzeug import Response as BaseResponse
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from wroblewshop.domain.cupboard import Cupboard, CupboardRepository
from wroblewshop.domain.item import CupboardItems, Item
from wroblewshop.domain.user import UserRepository
from wroblewshop.views.auth import secure

bp = Blueprint("item", __name__)


@bp.get("")
@secure
@inject.autoparams()
def index(cupboards: CupboardRepository, users: UserRepository) -> str:
    user_info = session["user"]
    user = users.get_by_email(user_info["email"])
    assert user
    cupboard = cupboards.get_by_name(user.cupboard)
    assert cupboard

    context = AddItemContext.from_domain(cupboard)

    context.form.validate_on_submit()
    return render_template("add-item.html", **_as_shallow_dict(context))


@bp.post("")
@secure
@inject.autoparams()
def add_item(cupboards: CupboardRepository, users: UserRepository) -> BaseResponse:
    user_info = session["user"]
    user = users.get_by_email(user_info["email"])
    assert user
    cupboard = cupboards.get_by_name(user.cupboard)
    assert cupboard

    form = AddItemForm.from_domain(cupboard.items)

    if not form.validate():
        return index()

    if form.name.data:
        cupboard.items.add_item(Item(id=None, name=form.name.data))
        cupboards.update(cupboard)

    return redirect(url_for("item.index"))


@dataclass
class AddItemContext:
    items: list[DeleteItemRowContext]
    form: AddItemForm

    @classmethod
    def from_domain(cls, cupboard: Cupboard) -> AddItemContext:
        return AddItemContext(
            items=[DeleteItemRowContext.from_domain(item) for item in cupboard.items.item_entries],
            form=AddItemForm.from_domain(cupboard.items),
        )


@dataclass
class DeleteItemRowContext:
    id: int
    form: DeleteItemForm

    @classmethod
    def from_domain(cls, item: Item) -> DeleteItemRowContext:
        assert item.id
        return DeleteItemRowContext(id=item.id, form=DeleteItemForm.from_domain(item))


class AddItemForm(FlaskForm):  # type: ignore
    name = StringField("Name", validators=[InputRequired(message="Please enter item name")])

    def __init__(self, existing_items: list[Item], **kwargs: object):
        super().__init__(**kwargs)
        self.existing_items = existing_items

    @classmethod
    def from_domain(cls, cupboard_items: CupboardItems) -> AddItemForm:
        return AddItemForm(existing_items=cupboard_items.item_entries)

    @staticmethod
    def validate_name(form: AddItemForm, field: StringField) -> None:
        if field.data is not None and field.data.lower() in [item.name.lower() for item in form.existing_items]:
            raise ValidationError("Please specify an item that doesn't already exist in the cupboard")


@bp.post("/delete/<int:item_id>")
@inject.autoparams()
def delete_item(item_id: int, users: UserRepository, cupboards: CupboardRepository) -> BaseResponse:
    user_info = session["user"]
    user = users.get_by_email(user_info["email"])
    assert user
    cupboard = cupboards.get_by_name(user.cupboard)
    assert cupboard

    # TODO: should domain allow for item getter
    item = next(item for item in cupboard.items.item_entries if item.id == item_id)
    form = DeleteItemForm.from_domain(item)

    if not form.validate():
        return index()

    cupboard.items.delete_item(item_id=item_id)
    cupboards.update(cupboard)

    return redirect(url_for("item.index"))


class DeleteItemForm(FlaskForm):  # type: ignore
    @staticmethod
    def create_class(item: Item) -> type[DeleteItemForm]:
        class DynamicDeleteItemForm(DeleteItemForm):
            pass

        field = SubmitField(label=item.name)
        setattr(DynamicDeleteItemForm, f"delete_{item.name.lower()}", field)

        return DynamicDeleteItemForm

    @classmethod
    def from_domain(cls, item: Item) -> DeleteItemForm:
        form_class = DeleteItemForm.create_class(item)
        return form_class()


def _as_shallow_dict(obj: Any) -> dict[str, Any]:
    return {field_.name: getattr(obj, field_.name) for field_ in fields(obj)}
