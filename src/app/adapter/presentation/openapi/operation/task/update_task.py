from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
    Parameter,
)

from app.adapter.presentation.openapi.exceptions.task import TASK_NOT_FOUND_EXCEPTION
from app.adapter.presentation.openapi.parameter.base import BaseParameterSchema
from app.adapter.presentation.openapi.parameter.task import TaskParameterSchema

DESCRIPTION = """
Update task.

* **task_id** - unique identifier

* **name** - name

* **description** - description
"""

SUMMARY = "Update Task"

REQUEST_BODY_EXAMPLE = {
    "name": "Cooking",
    "description": "Task Description"
}

RESPONSE_EXAMPLE = {
    "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
    "name": "Cooking",
    "description": "Task Description"
}


@dataclass
class UpdateTaskOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["tasks"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.request_body = RequestBody(
            content={
                "json": OpenAPIMediaType(
                    schema=Schema(
                        type=OpenAPIType.OBJECT,
                        properties={
                            "name": TaskParameterSchema.name,
                            "description": TaskParameterSchema.description
                        }
                    ),
                    example=REQUEST_BODY_EXAMPLE
                )
            }
        )
        self.parameters = [
            Parameter(
                name="task_id",
                param_in="path",
                required=True,
                schema=TaskParameterSchema.task_id
            )
        ]
        self.responses = {
            "200": OpenAPIResponse(
                description="Ok",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "id": TaskParameterSchema.id,
                                "name": TaskParameterSchema.name,
                                "description": TaskParameterSchema.description
                            }
                        ),
                        example=RESPONSE_EXAMPLE
                    )
                }
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
