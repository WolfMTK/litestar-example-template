from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter.db.connect import get_transaction
from app.adapter.db.gateway.task import TaskGateway
from app.application.usecase.task import TaskUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            session: AsyncSession,
    ) -> None:
        self.transaction = get_transaction(session)
        self.task_gateway = TaskGateway(session)

    @asynccontextmanager
    async def task_usecase(self) -> AsyncIterator[TaskUseCase]:
        yield TaskUseCase(
            transaction=self.transaction,
            task_gateway=self.task_gateway
        )
