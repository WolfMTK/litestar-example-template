from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from litestar.params import Dependency

from app.adapter.db.gateway.task import TaskGateway
from app.application.interface.transaction import Transaction
from app.application.usecase.task import TaskUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            transaction: Annotated[Transaction, Dependency(skip_validation=True)],
            task_gateway: TaskGateway
    ) -> None:
        self.transaction = transaction
        self.task_gateway = task_gateway

    @asynccontextmanager
    async def task_usecase(self) -> AsyncIterator[TaskUseCase]:
        yield TaskUseCase(
            transaction=self.transaction,
            task_gateway=self.task_gateway
        )
