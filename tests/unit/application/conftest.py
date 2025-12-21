from unittest.mock import create_autospec, MagicMock

import pytest
from faker import Faker

from app.application.interactor.task import GetTaskInteractor, RegisterTaskInteractor, GetTaskListInteractor, \
    UpdateTaskInteractor, DeleteTaskInteractor
from app.application.interface.db import DBSession
from app.application.interface.gateway import ITaskRead, ITaskWrite


@pytest.fixture
def get_task_interactor() -> GetTaskInteractor:
    task_read = create_autospec(ITaskRead)
    return GetTaskInteractor(
        task_read=task_read,
    )


@pytest.fixture
def register_task_interactor(faker: Faker) -> RegisterTaskInteractor:
    db_session = create_autospec(DBSession)
    task_write = create_autospec(ITaskWrite)
    ulid_generator = MagicMock(return_value=str(faker.uuid4()))
    return RegisterTaskInteractor(
        db_session=db_session,
        task_write=task_write,
        ulid_generator=ulid_generator,
    )


@pytest.fixture
def get_task_list_interactor() -> GetTaskListInteractor:
    task_read = create_autospec(ITaskRead)
    return GetTaskListInteractor(
        task_read=task_read,
    )


@pytest.fixture
def update_task_interactor() -> UpdateTaskInteractor:
    db_session = create_autospec(DBSession)
    task_write = create_autospec(ITaskWrite)
    task_read = create_autospec(ITaskRead)
    return UpdateTaskInteractor(
        db_session=db_session,
        task_write=task_write,
        task_read=task_read,
    )


@pytest.fixture
def delete_task_interactor() -> DeleteTaskInteractor:
    db_session = create_autospec(DBSession)
    task_write = create_autospec(ITaskWrite)
    task_read = create_autospec(ITaskRead)
    return DeleteTaskInteractor(
        db_session=db_session,
        task_write=task_write,
        task_read=task_read,
    )
