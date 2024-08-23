from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self, cast

from ulid import ULID

from app.domain.model.id import Id
from app.domain.model.task import Task


@dataclass(slots=True)
class TaskView:
    id: str
    name: str
    description: str

    @classmethod
    def from_into(cls, value: Task) -> Self:
        return cls(
            id=str(value.id),
            name=value.name,
            description=value.description
        )


@dataclass(slots=True)
class TaskListView:
    total: int
    tasks: Iterator[TaskView]


@dataclass(slots=True)
class CreateTaskView:
    name: str
    description: str

    def into(self) -> Task:
        return Task(
            id=cast(Id, str(ULID())),
            name=self.name,
            description=self.description
        )


@dataclass(slots=True)
class UpdateTaskView:
    id: str
    name: str | None
    description: str | None

    def into(self) -> Task:
        return Task(
            id=cast(id, self.id),
            name=self.name,
            description=self.description
        )
