from __future__ import annotations

from dataclasses import dataclass

import requests


class AppClient:
    def __init__(self, url: str):
        self.url = url

    def add_user(self, user: UserRepr) -> None:
        response = requests.post(f"{self.url}/user", json={"email": user.email})
        response.raise_for_status()

    def clear_users(self) -> None:
        response = requests.delete(f"{self.url}/user")
        response.raise_for_status()


@dataclass
class UserRepr:
    email: str
