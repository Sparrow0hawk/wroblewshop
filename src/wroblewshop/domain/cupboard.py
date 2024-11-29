class Cupboard:
    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name


class CupboardRepository:
    def add(self, cupboard: Cupboard) -> None:
        raise NotImplementedError()

    def get_by_name(self, name: str) -> Cupboard | None:
        raise NotImplementedError()

    def get_all(self) -> list[Cupboard]:
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()
