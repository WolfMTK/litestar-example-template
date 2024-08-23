from collections.abc import Iterator
from typing import cast

from ulid import ULID

from app.domain.model.id import Id
from app.domain.model.task import Task


class TaskGatewayMock:
    def __init__(self) -> None:
        self.is_check = True
        self._limit = 10
        self._offset = 0
        self._total = 2
        self._task_id = ULID()

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def task_id(self) -> Id:
        return cast(Id, self._task_id)

    @property
    def total(self) -> int:
        return self._total

    async def insert(self, source: Task) -> Task:
        self._task_id = source.id
        return Task(
            id=self.task_id,
            name=source.name,
            description=source.description
        )

    async def update(self, source: Task) -> Task:
        return Task(
            id=self.task_id,
            name=source.name,
            description=source.description
        )

    async def get(self, source: Id) -> Task | None:
        if not self.is_check:
            return None
        return Task(
            id=source,
            name="Cooking",
            description="Task Description"
        )

    async def get_list(
            self,
            limit: int,
            offset: int
    ) -> Iterator[Task]:
        return (Task(
            id=cast(Id, ULID()),
            name="Cooking",
            description="Task Description"
        ) for _ in range(self.total))

    async def get_total(self) -> int:
        return self.total

    async def check_task(self, source: Id) -> bool:
        return self.is_check

    async def delete(self, source: Id) -> Task:
        return Task(
            id=self.task_id,
            name="Cooking",
            description="Task Description"
        )
