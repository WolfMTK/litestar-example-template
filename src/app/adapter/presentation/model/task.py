from typing import Self

from pydantic import Field

from app.application.model.task import (
    TaskView,
    TaskListView,
    CreateTaskView,
    UpdateTaskView,
)
from app.adapter.presentation.constants import TOTAL, LIMIT, OFFSET
from app.adapter.presentation.model.base import Base


class JsonTask(Base):
    id: str = Field(
        ...,
        json_schema_extra={
            "title": "id",
            "description": "Unique identifier",
            "example": "01J4HC5WQB3FK3FA1FMXYVYJ6Y"
        }
    )
    name: str = Field(
        ...,
        json_schema_extra={
            "title": "name",
            "description": "Task name",
            "example": "Cooking"
        }
    )
    description: str = Field(
        ...,
        json_schema_extra={
            "title": "description",
            "description": "Task Description",
            "example": "Make a meal"
        }
    )

    @classmethod
    def from_into(cls, value: TaskView) -> Self:
        return cls(
            id=value.id,
            name=value.name,
            description=value.description
        )


class JsonTaskList(Base):
    total: int = Field(
        ...,
        json_schema_extra={
            "title": "total",
            "description": "Number of records",
            "example": TOTAL
        }
    )
    limit: int = Field(
        ...,
        json_schema_extra={
            "title": "limit",
            "description": "Record limit",
            "example": LIMIT
        }
    )
    offset: int = Field(
        ...,
        json_schema_extra={
            "title": "offset",
            "description": "Current page",
            "example": OFFSET
        }
    )
    values: list[JsonTask] = Field(
        ...,
        description="Tasks"
    )

    @classmethod
    def from_into(cls, limit: int, offset: int, value: TaskListView) -> Self:
        return cls(
            total=value.total,
            limit=limit,
            offset=offset,
            values=[JsonTask.from_into(task) for task in value.tasks]
        )


class JsonCreateTask(Base):
    name: str = Field(
        ...,
        json_schema_extra={
            "title": "name",
            "description": "Task name",
            "example": "Cooking"
        }
    )
    description: str = Field(
        ...,
        json_schema_extra={
            "title": "description",
            "description": "Task Description",
            "example": "Make a meal"
        }
    )

    def into(self) -> CreateTaskView:
        return CreateTaskView(
            name=self.name,
            description=self.description
        )


class JsonUpdateTask(Base):
    name: str | None = Field(
        None,
        json_schema_extra={
            "title": "name",
            "description": "Task name",
        }
    )
    description: str | None = Field(
        None,
        json_schema_extra={
            "title": "description",
            "description": "Task Description",
        }
    )

    def into(self, task_id: str) -> UpdateTaskView:
        return UpdateTaskView(
            id=task_id,
            name=self.name,
            description=self.description
        )
