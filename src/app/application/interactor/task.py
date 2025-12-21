from dataclasses import asdict

from app.application.dto.id import IdDTO
from app.application.dto.page import PaginationDTO
from app.application.dto.task import (
    CreateTaskDTO,
    TaskDTO,
    TaskListDTO,
    UpdateTaskDTO,
)
from app.application.exceptions.task import TaskNotFoundException
from app.application.interface.db import DBSession
from app.application.interface.gateway import ITaskWrite, ITaskRead
from app.application.interface.ulid_generator import ULIDGenerator
from app.domain.model.task import Task


class RegisterTaskInteractor:
    def __init__(
            self,
            db_session: DBSession,
            task_write: ITaskWrite,
            ulid_generator: ULIDGenerator
    ) -> None:
        self.db_session = db_session
        self.task_write = task_write
        self.ulid_generator = ulid_generator

    async def execute(self, source: CreateTaskDTO) -> IdDTO:
        task = Task(
            id=self.ulid_generator(),
            name=source.name,
            description=source.description,
        )
        task = await self.task_write.insert(task)
        await self.db_session.commit()
        return IdDTO(
            id=task.id,
        )


class GetTaskInteractor:
    def __init__(
            self,
            task_read: ITaskRead,
    ) -> None:
        self.task_read = task_read

    async def execute(self, dto: IdDTO) -> TaskDTO:
        task = await self.task_read.get(dto.id)
        if task is None:
            raise TaskNotFoundException()
        return TaskDTO(
            id=task.id,
            name=task.name,
            description=task.description,
        )


class GetTaskListInteractor:
    def __init__(
            self,
            task_read: ITaskRead,
    ) -> None:
        self.task_read = task_read

    async def execute(self, dto: PaginationDTO) -> TaskListDTO:
        tasks = await self.task_read.get_list(
            limit=dto.limit,
            offset=dto.offset,
        )
        return TaskListDTO(
            total=tasks.total,
            limit=tasks.limit,
            offset=tasks.offset,
            values=[TaskDTO(
                id=task.id,
                name=task.name,
                description=task.description,
            ) for task in tasks.values]
        )


class UpdateTaskInteractor:
    def __init__(
            self,
            db_session: DBSession,
            task_write: ITaskWrite,
            task_read: ITaskRead,
    ) -> None:
        self.db_session = db_session
        self.task_write = task_write
        self.task_read = task_read

    async def execute(self, dto: UpdateTaskDTO) -> TaskDTO:
        task = await self.task_read.get(dto.id)
        if task is None:
            raise TaskNotFoundException()
        for key, val in asdict(dto).items():
            if val is not None:
                setattr(task, key, val)
        task = await self.task_write.update(task)
        await self.db_session.commit()
        return TaskDTO(
            id=task.id,
            name=task.name,
            description=task.description,
        )


class DeleteTaskInteractor:
    def __init__(
            self,
            db_session: DBSession,
            task_write: ITaskWrite,
            task_read: ITaskRead,
    ) -> None:
        self.db_session = db_session
        self.task_write = task_write
        self.task_read = task_read

    async def execute(self, dto: IdDTO) -> None:
        task = await self.task_read.get(dto.id)
        if task is None:
            raise TaskNotFoundException()
        await self.task_write.delete(dto.id)
        await self.db_session.commit()
