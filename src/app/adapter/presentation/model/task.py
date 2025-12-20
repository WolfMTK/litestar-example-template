from pydantic import Field

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
