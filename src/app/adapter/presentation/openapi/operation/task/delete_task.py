from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    Parameter,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
)

from app.adapter.presentation.openapi.exceptions.task import TASK_NOT_FOUND_EXCEPTION
from app.adapter.presentation.openapi.parameter.base import BaseParameterSchema
from app.adapter.presentation.openapi.parameter.task import TaskParameterSchema

DESCRIPTION = """
Delete task.

* **task_id** - unique identifier
"""

SUMMARY = "Delete Task"


@dataclass
class DeleteTaskOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["tasks"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.parameters = [Parameter(
            name="task_id",
            param_in="path",
            required=True,
            schema=TaskParameterSchema.task_id
        )]
        self.responses = {
            "200": OpenAPIResponse(
                description="Not Content",
                content=None
            ),
            "404": OpenAPIResponse(
                description="Not Found",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "status_code": BaseParameterSchema.status_code,
                                "detail": BaseParameterSchema.detail
                            }
                        ),
                        example=TASK_NOT_FOUND_EXCEPTION
                    )
                }
            )
        }
