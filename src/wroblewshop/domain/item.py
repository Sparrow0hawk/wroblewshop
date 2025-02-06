from __future__ import annotations

from dataclasses import dataclass


class CupboardItems:
    def __init__(self) -> None:
        self._items: list[Item] = []

    @property
    def item_entries(self) -> list[Item]:
        return self._items.copy()

    def add_item(self, item: Item) -> None:
        self._ensure_unique_item(item)
        self._items.append(item)

    def add_items(self, *items: Item) -> None:
        for item in items:
            self.add_item(item)

    def delete_item(self, item_id: int) -> None:
        self._items = [item for item in self._items if item.id != item_id]

    def _ensure_unique_item(self, item: Item) -> None:
        if item.name.lower() in [cupboard_item.name.lower() for cupboard_item in self._items]:
            raise ValueError(f"Cupboard already contains item: {item.name}")


@dataclass(frozen=True)
class Item:
    id: int | None
    name: str
