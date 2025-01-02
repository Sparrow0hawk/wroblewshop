from __future__ import annotations

from dataclasses import dataclass


class CupboardItems:
    def __init__(self) -> None:
        self._items: list[Item] = []

    @property
    def item_entries(self) -> list[Item]:
        return self._items.copy()

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def add_items(self, *items: Item) -> None:
        for item in items:
            self.add_item(item)


@dataclass(frozen=True)
class Item:
    id: int | None
    name: str
