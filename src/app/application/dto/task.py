from dataclasses import dataclass, field


@dataclass(slots=True)
class CreateTaskDTO:
    name: str
    description: str


@dataclass(slots=True)
class TaskDTO:
    id: str
    name: str
    description: str


@dataclass(slots=True)
class TaskListDTO:
    total: int
    limit: int
    offset: int
    values: list[TaskDTO]


@dataclass(slots=True, kw_only=True)
class UpdateTaskDTO:
    id: str
    name: str | None = field(default=None)
    description: str | None = field(default=None)
