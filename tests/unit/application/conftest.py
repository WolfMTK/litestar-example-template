import pytest

from tests.mocks.task import TaskGatewayMock
from tests.mocks.transaction import TransactionMock


@pytest.fixture
def task_gateway() -> TaskGatewayMock:
    return TaskGatewayMock()


@pytest.fixture
def transaction() -> TransactionMock:
    return TransactionMock()
