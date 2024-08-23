from abc import abstractmethod
from typing import Protocol


class Transaction(Protocol):
    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
