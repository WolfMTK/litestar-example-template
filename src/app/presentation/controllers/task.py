from typing import Annotated

from litestar import post, get, delete, patch, status_codes
from litestar.controller import Controller
from litestar.params import Dependency, Parameter

from app.application.exceptions.task import TaskNotFoundException
from app.presentation.constants import OFFSET, LIMIT
from app.presentation.exception_handlers import not_found
from app.presentation.interactor import InteractorFactory
from app.presentation.model.task import (
    JsonCreateTask,
    JsonTask,
    JsonTaskList,
    JsonUpdateTask,
)
from app.presentation.openapi import (
    CreateTaskOperation,
    GetTaskOperation,
    GetTasksOperation,
    UpdateTaskOperation,
    DeleteTaskOperation,
)

LENGTH_ID = 26


class TaskController(Controller):
    path = "/tasks"
    exception_handlers = {
        TaskNotFoundException: not_found
    }

    @post(
        operation_class=CreateTaskOperation
    )
    async def create_task(
            self,
            data: JsonCreateTask,
            ioc: Annotated[
                InteractorFactory,
                Dependency(skip_validation=True)
            ]
    ) -> JsonTask:
        async with ioc.task_usecase() as usecase:
            task = await usecase.create_task(data.into())
            return JsonTask.from_into(task)

    @get(
        "/{task_id:str}",
        operation_class=GetTaskOperation
    )
    async def get_task(
            self,
            task_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            ioc: Annotated[
                InteractorFactory,
                Dependency(skip_validation=True)
            ]
    ) -> JsonTask:
        async with ioc.task_usecase() as usecase:
            task = await usecase.get_task(task_id)
            return JsonTask.from_into(task)

    @get(
        operation_class=GetTasksOperation
    )
    async def get_tasks(
            self,
            ioc: Annotated[
                InteractorFactory,
                Dependency(skip_validation=True)
            ],
            limit: int = LIMIT,
            offset: int = OFFSET
    ) -> JsonTaskList:
        async with ioc.task_usecase() as usecase:
            tasks = await usecase.get_tasks(limit, offset)
            return JsonTaskList.from_into(limit, offset, tasks)

    @patch(
        "/{task_id:str}",
        operation_class=UpdateTaskOperation
    )
    async def update_task(
            self,
            task_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            data: JsonUpdateTask,
            ioc: Annotated[
                InteractorFactory,
                Dependency(skip_validation=True)
            ]
    ) -> JsonTask:
        async with ioc.task_usecase() as usecase:
            task = await usecase.update_task(data.into(task_id))
            return JsonTask.from_into(task)

    @delete(
        "/{task_id:str}",
        status_code=status_codes.HTTP_204_NO_CONTENT,
        operation_class=DeleteTaskOperation
    )
    async def delete_task(
            self,
            task_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            ioc: Annotated[
                InteractorFactory,
                Dependency(skip_validation=True)
            ]
    ) -> None:
        async with ioc.task_usecase() as usecase:
            await usecase.delete_task(task_id)
