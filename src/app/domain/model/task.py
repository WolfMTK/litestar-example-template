from dataclasses import dataclass

from app.domain.model.id import Id


@dataclass(slots=True)
class Task:
    id: Id
    name: str | None
    description: str | None
