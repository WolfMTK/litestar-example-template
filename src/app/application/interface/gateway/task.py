from abc import abstractmethod
from typing import Protocol

from app.domain.model.id import Id
from app.domain.model.task import Task, TaskList


class ITaskWrite(Protocol):
    @abstractmethod
    async def insert(self, task: Task) -> Task: ...

    @abstractmethod
    async def update(self, task: Task) -> Task: ...

    @abstractmethod
    async def delete(self, task_id: Id) -> None: ...


class ITaskRead(Protocol):
    @abstractmethod
    async def get(self, task_id: Id) -> Task | None: ...

    @abstractmethod
    async def get_list(self, limit: int, offset: int) -> TaskList: ...
