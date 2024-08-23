from typing import cast

from app.application.exceptions.task import TaskNotFoundException
from app.application.interface.task import TaskGateway
from app.application.interface.transaction import Transaction
from app.application.model.task import (
    CreateTaskView,
    TaskView,
    UpdateTaskView,
    TaskListView,
)
from app.domain.model.id import Id


class TaskUseCase:
    def __init__(
            self,
            transaction: Transaction,
            task_gateway: TaskGateway,
    ) -> None:
        self.transaction = transaction
        self.task_gateway = task_gateway

    async def create_task(self, source: CreateTaskView) -> TaskView:
        task = await self.task_gateway.insert(source.into())
        await self.transaction.commit()
        return TaskView.from_into(task)

    async def update_task(self, source: UpdateTaskView) -> TaskView:
        if not await self.task_gateway.check_task(cast(Id, source.id)):
            raise TaskNotFoundException()

        task = await self.task_gateway.update(source.into())
        await self.transaction.commit()
        return TaskView.from_into(task)

    async def get_task(self, task_id: str) -> TaskView:
        task = await self.task_gateway.get(cast(Id, task_id))

        if task is None:
            raise TaskNotFoundException()

        return TaskView.from_into(task)

    async def get_tasks(self, limit: int, offset: int) -> TaskListView:
        tasks = await self.task_gateway.get_list(limit, offset)
        total = await self.task_gateway.get_total()
        return TaskListView(
            total=total,
            tasks=(TaskView.from_into(task) for task in tasks)
        )

    async def delete_task(self, task_id: str) -> TaskView:
        if not await self.task_gateway.check_task(cast(Id, task_id)):
            raise TaskNotFoundException()

        task = await self.task_gateway.delete(cast(Id, task_id))
        await self.transaction.commit()
        return TaskView.from_into(task)
