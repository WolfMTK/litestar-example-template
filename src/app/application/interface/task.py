from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.domain.model.id import Id
from app.domain.model.task import Task


class TaskGateway(Protocol):
    @abstractmethod
    async def insert(self, source: Task) -> Task: ...

    @abstractmethod
    async def update(self, source: Task) -> Task: ...

    @abstractmethod
    async def get(self, source: Id) -> Task | None: ...

    @abstractmethod
    async def get_list(
            self,
            limit: int,
            offset: int
    ) -> Iterator[Task]: ...

    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def check_task(self, source: Id) -> bool: ...

    @abstractmethod
    async def delete(self, source: Id) -> Task: ...
