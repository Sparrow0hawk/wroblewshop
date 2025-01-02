from __future__ import annotations

from dataclasses import dataclass, field

import requests
from dacite import from_dict


class AppClient:
    def __init__(self, url: str):
        self.url = url

    def add_user(self, user: UserRepr) -> None:
        response = requests.post(f"{self.url}/user", json={"email": user.email, "cupboard": user.cupboard})
        response.raise_for_status()

    def clear_users(self) -> None:
        response = requests.delete(f"{self.url}/user")
        response.raise_for_status()

    def add_cupboard(self, cupboard: CupboardRepr) -> None:
        response = requests.post(f"{self.url}/cupboard", json={"id": cupboard.id, "name": cupboard.name})
        response.raise_for_status()

    def get_cupboard(self, id_: int) -> CupboardRepr:
        response = requests.get(f"{self.url}/cupboard/{id_}")
        cupboard_repr = from_dict(data_class=CupboardRepr, data=response.json())
        return cupboard_repr

    def clear_cupboards(self) -> None:
        response = requests.delete(f"{self.url}/cupboard")
        response.raise_for_status()


@dataclass
class UserRepr:
    email: str
    cupboard: str


@dataclass
class CupboardRepr:
    id: int
    name: str
    items: list[ItemRepr] = field(default_factory=list)


@dataclass
class ItemRepr:
    name: str
