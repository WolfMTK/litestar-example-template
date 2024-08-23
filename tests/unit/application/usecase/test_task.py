from collections.abc import Iterator

import pytest

from app.application.exceptions.task import TaskNotFoundException
from app.application.model.task import (
    CreateTaskView,
    TaskView,
    UpdateTaskView,
    TaskListView,
)
from app.application.usecase.task import TaskUseCase
from tests.mocks.task import TaskGatewayMock
from tests.mocks.transaction import TransactionMock


async def test_create_task(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )

    view = CreateTaskView(
        name="Cooking",
        description="Task Description"
    )
    task = await usecase.create_task(view)
    assert isinstance(task, TaskView)
    assert task.id == gateway.task_id
    assert task.name == view.name
    assert task.description == view.description

    assert transaction.commited
    assert not transaction.rolled_back


async def test_update_task(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    view = UpdateTaskView(
        id=str(gateway.task_id),
        name="Cooking",
        description="Task Description"
    )
    task = await usecase.update_task(view)
    assert isinstance(task, TaskView)
    assert task.id == view.id
    assert task.name == view.name
    assert task.description == view.description

    assert transaction.commited
    assert not transaction.rolled_back


async def test_invalid_update_task(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    gateway.is_check = False
    view = UpdateTaskView(
        id=str(gateway.task_id),
        name="Cooking",
        description="Task Description"
    )
    with pytest.raises(TaskNotFoundException) as err:
        _ = await usecase.update_task(view)
    assert str(err.value) == "Task not found"

    assert not transaction.commited
    assert not transaction.rolled_back


async def test_get_task(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    stored_task = await gateway.get(gateway.task_id)
    task = await usecase.get_task(str(gateway.task_id))
    assert isinstance(task, TaskView)
    assert task.id == str(gateway.task_id)
    assert task.name == stored_task.name
    assert task.description == stored_task.description

    assert not transaction.commited
    assert not transaction.rolled_back


async def test_invalid_get_task(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    gateway.is_check = False
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    with pytest.raises(TaskNotFoundException) as err:
        _ = await usecase.get_task(str(gateway.task_id))
    assert str(err.value) == "Task not found"

    assert not transaction.commited
    assert not transaction.rolled_back


async def test_get_tasks(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    tasks = await usecase.get_tasks(
        gateway.limit,
        gateway.offset
    )
    assert isinstance(tasks, TaskListView)
    assert tasks.total == gateway.total
    assert isinstance(tasks.tasks, Iterator)
    assert len(list(tasks.tasks)) == gateway.total

    assert not transaction.commited
    assert not transaction.rolled_back


async def test_delete_task(
        transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    stored_task = await gateway.get(gateway.task_id)
    task = await usecase.delete_task(str(gateway.task_id))
    assert isinstance(task, TaskView)
    assert task.id == str(gateway.task_id)
    assert task.name == stored_task.name
    assert task.description == stored_task.description

    assert transaction.commited
    assert not transaction.rolled_back


async def test_invalid_delete_task(
transaction: TransactionMock,
        task_gateway: TaskGatewayMock
) -> None:
    gateway = task_gateway
    gateway.is_check = False
    usecase = TaskUseCase(
        transaction=transaction,
        task_gateway=gateway
    )
    with pytest.raises(TaskNotFoundException) as err:
        _ = await usecase.delete_task(str(gateway.task_id))
    assert str(err.value) == "Task not found"

    assert not transaction.commited
    assert not transaction.rolled_back
