class BaseTaskException(Exception):
    pass


class TaskNotFoundException(BaseTaskException):
    def __str__(self) -> str:
        return "Task not found"
