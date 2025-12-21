from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    RequestBody,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
)

from app.adapter.presentation.openapi.parameter.task import TaskParameterSchema

DESCRIPTION = """
Create task.

* **name** - name

* **description** - description
"""

SUMMARY = "Create Task"

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
class CreateTaskOperation(Operation):
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
                        },
                        required=("name", "description")
                    ),
                    example=REQUEST_BODY_EXAMPLE
                )
            }
        )
        self.responses = {
            "201": OpenAPIResponse(
                description="Created",
                content={
                    "json": OpenAPIMediaType(
                        schema=Schema(
                            type=OpenAPIType.OBJECT,
                            properties={
                                "id": TaskParameterSchema.id,
                            }
                        ),
                        example=RESPONSE_EXAMPLE
                    )
                }
            )
        }
