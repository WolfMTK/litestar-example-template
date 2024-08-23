from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.usecase.task import TaskUseCase


class InteractorFactory(ABC):
    @abstractmethod
    def task_usecase(self) -> AbstractAsyncContextManager[TaskUseCase]: ...
