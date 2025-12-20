from typing import Protocol

from app.domain.model.id import Id


class ULIDGenerator(Protocol):
    def __call__(self) -> Id: ...
