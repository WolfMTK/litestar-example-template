from typing import Annotated

from dishka.integrations.litestar import inject, FromDishka
from litestar import post, get, patch, delete, status_codes
from litestar.controller import Controller
from litestar.params import Parameter

from app.adapter.presentation.constants import OFFSET, LIMIT
from app.adapter.presentation.exception_handlers import not_found
from app.adapter.presentation.model.id import JsonId
from app.adapter.presentation.model.task import (
    JsonCreateTask,
    JsonTask,
    JsonTaskList,
    JsonUpdateTask,
)
from app.adapter.presentation.openapi import (
    CreateTaskOperation,
    GetTaskOperation,
    GetTasksOperation,
    UpdateTaskOperation,
    DeleteTaskOperation,
)
from app.application.dto.id import IdDTO
from app.application.dto.page import PaginationDTO
from app.application.dto.task import CreateTaskDTO, UpdateTaskDTO
from app.application.exceptions.task import TaskNotFoundException
from app.application.interactor.task import (
    RegisterTaskInteractor,
    GetTaskInteractor,
    GetTaskListInteractor,
    UpdateTaskInteractor,
    DeleteTaskInteractor,
)

LENGTH_ID = 26


class TaskController(Controller):
    path = "/tasks"
    exception_handlers = {
        TaskNotFoundException: not_found,
    }

    @post(
        operation_class=CreateTaskOperation,
    )
    @inject
    async def create_task(
            self,
            data: JsonCreateTask,
            interactor: FromDishka[RegisterTaskInteractor],
    ) -> JsonId:
        dto = CreateTaskDTO(
            name=data.name,
            description=data.description,
        )
        task_id = await interactor.execute(dto)
        return JsonId(
            id=task_id.id,
        )

    @get(
        "/{task_id:str}",
        operation_class=GetTaskOperation,
    )
    @inject
    async def get_task(
            self,
            task_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            interactor: FromDishka[GetTaskInteractor],
    ) -> JsonTask:
        dto = IdDTO(id=task_id)
        task = await interactor.execute(dto)
        return JsonTask(
            id=task.id,
            name=task.name,
            description=task.description,
        )

    @get(
        operation_class=GetTasksOperation,
    )
    @inject
    async def get_tasks(
            self,
            interactor: FromDishka[GetTaskListInteractor],
            limit: int = LIMIT,
            offset: int = OFFSET,
    ) -> JsonTaskList:
        dto = PaginationDTO(
            limit=limit,
            offset=offset,
        )
        tasks = await interactor.execute(dto)
        return JsonTaskList(
            limit=limit,
            offset=offset,
            total=tasks.total,
            values=[JsonTask(
                id=task.id,
                name=task.name,
                description=task.description,
            ) for task in tasks.values]
        )

    @patch(
        "/{task_id:str}",
        operation_class=UpdateTaskOperation,
    )
    @inject
    async def update_task(
            self,
            task_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            data: JsonUpdateTask,
            interactor: FromDishka[UpdateTaskInteractor],
    ) -> JsonTask:
        dto = UpdateTaskDTO(
            id=task_id,
            name=data.name,
            description=data.description,
        )
        task = await interactor.execute(dto)
        return JsonTask(
            id=task.id,
            name=task.name,
            description=task.description,
        )

    @delete(
        "/{task_id:str}",
        status_code=status_codes.HTTP_204_NO_CONTENT,
        operation_class=DeleteTaskOperation,
    )
    @inject
    async def delete_task(
            self,
            task_id: Annotated[str, Parameter(
                max_length=LENGTH_ID,
                min_length=LENGTH_ID
            )],
            interactor: FromDishka[DeleteTaskInteractor],
    ) -> None:
        dto = IdDTO(id=task_id)
        await interactor.execute(dto)
