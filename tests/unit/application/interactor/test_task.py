import pytest
import ulid
from faker.proxy import Faker

from app.application.dto.id import IdDTO
from app.application.dto.page import PaginationDTO
from app.application.dto.task import CreateTaskDTO, UpdateTaskDTO
from app.application.exceptions.task import TaskNotFoundException
from app.application.interactor.task import (
    GetTaskInteractor,
    RegisterTaskInteractor,
    GetTaskListInteractor,
    UpdateTaskInteractor,
    DeleteTaskInteractor,
)
from app.domain.model.task import Task, TaskList


@pytest.mark.parametrize(
    "dto", [
        IdDTO(id=str(ulid.ULID())),
        IdDTO(id=str(ulid.ULID())),
    ]
)
async def test_get_task_interactor(
        get_task_interactor: GetTaskInteractor,
        dto: IdDTO,
        faker: Faker,
) -> None:
    task = Task(
        id=dto.id,
        name=faker.pystr(),
        description=faker.pystr(),
    )
    get_task_interactor.task_read.get.return_value = task
    result = await get_task_interactor.execute(dto)
    get_task_interactor.task_read.get.assert_awaited_once_with(dto.id)
    assert result.id == task.id
    assert result.name == task.name
    assert result.description == task.description


async def test_invalid_get_task_interactor(
        get_task_interactor: GetTaskInteractor,
) -> None:
    dto = IdDTO(id=str(ulid.ULID()))
    get_task_interactor.task_read.get.return_value = None
    with pytest.raises(TaskNotFoundException) as err:
        await get_task_interactor.execute(dto)
    assert str(err.value) == "Task not found"


async def test_get_task_list_interactor(
        get_task_list_interactor: GetTaskListInteractor,
        faker: Faker,
) -> None:
    dto = PaginationDTO(
        limit=faker.pyint(),
        offset=faker.pyint(),
    )
    task_list = TaskList(
        total=10,
        offset=dto.offset,
        limit=dto.limit,
        values=[
            Task(
                id=str(faker.uuid4()),
                name=faker.pystr(),
                description=faker.pystr(),
            ),
            Task(
                id=str(faker.uuid4()),
                name=faker.pystr(),
                description=faker.pystr(),
            )
        ]
    )
    get_task_list_interactor.task_read.get_list.return_value = task_list
    result = await get_task_list_interactor.execute(dto)
    get_task_list_interactor.task_read.get_list.assert_awaited_once_with(dto.limit, dto.offset)
    assert result.total == task_list.total
    assert result.offset == task_list.offset
    assert result.limit == task_list.limit


async def test_register_task_interactor(
        register_task_interactor: RegisterTaskInteractor,
        faker: Faker,
) -> None:
    dto = CreateTaskDTO(
        name=faker.pystr(),
        description=faker.pystr(),
    )
    task = Task(
        id=str(register_task_interactor.ulid_generator()),
        name=dto.name,
        description=dto.description,
    )
    register_task_interactor.task_write.insert.return_value = task
    result = await register_task_interactor.execute(dto)
    register_task_interactor.task_write.insert.assert_awaited_with(task)
    register_task_interactor.db_session.commit.assert_awaited_once()
    assert result.id == task.id


@pytest.mark.parametrize(
    "dto", [
        UpdateTaskDTO(
            id=str(ulid.ULID()),
            name="test",
        ),
        UpdateTaskDTO(
            id=str(ulid.ULID()),
            description="test",
        ),
        UpdateTaskDTO(
            id=str(ulid.ULID()),
            name="test",
            description="test",
        )
    ]
)
async def test_update_task_interactor(
        update_task_interactor: UpdateTaskInteractor,
        faker: Faker,
        dto: UpdateTaskDTO,
) -> None:
    task = Task(
        id=dto.id,
        name=dto.name or faker.pystr(),
        description=dto.description or faker.pystr(),
    )
    update_task_interactor.task_write.update.return_value = task
    update_task_interactor.task_read.get.return_value = task
    result = await update_task_interactor.execute(dto)
    update_task_interactor.task_read.get.assert_awaited_once_with(task.id)
    update_task_interactor.task_write.update.assert_awaited_with(task)
    update_task_interactor.db_session.commit.assert_awaited_once()
    assert result.id == task.id
    assert result.name == task.name
    assert result.description == task.description


async def test_invalid_update_task_interactor(
        update_task_interactor: UpdateTaskInteractor,
        faker: Faker,
) -> None:
    dto = UpdateTaskDTO(
        id=str(faker.uuid4()),
        name=faker.pystr(),
        description=faker.pystr(),
    )
    update_task_interactor.task_read.get.return_value = None
    with pytest.raises(TaskNotFoundException) as err:
        await update_task_interactor.execute(dto)
    assert str(err.value) == "Task not found"


async def test_delete_task_interactor(
        delete_task_interactor: DeleteTaskInteractor,
        faker: Faker,
) -> None:
    dto = IdDTO(
        id=str(faker.uuid4()),
    )
    result = await delete_task_interactor.execute(dto)
    delete_task_interactor.task_read.get.assert_awaited_once_with(dto.id)
    delete_task_interactor.task_write.delete.assert_awaited_once_with(dto.id)
    delete_task_interactor.db_session.commit.assert_awaited_once()
    assert result is None


async def test_invalid_delete_task_interactor(
        delete_task_interactor: DeleteTaskInteractor,
        faker: Faker,
) -> None:
    dto = IdDTO(
        id=str(faker.uuid4()),
    )
    delete_task_interactor.task_read.get.return_value = None
    with pytest.raises(TaskNotFoundException) as err:
        await delete_task_interactor.execute(dto)
    assert str(err.value) == "Task not found"
