from dataclasses import dataclass

from litestar.openapi.spec import (
    OpenAPIMediaType,
    Operation,
    Parameter,
    Schema,
    OpenAPIResponse,
    OpenAPIType,
)

from app.presentation.constants import LIMIT, OFFSET, TOTAL
from app.presentation.openapi.parameter.base import BaseParameterSchema
from app.presentation.openapi.parameter.task import TaskParameterSchema

DESCRIPTION = """
Get tasks.

* **limit** - record limit

* **offset** - current page
"""

SUMMARY = "Get Tasks"

RESPONSE_EXAMPLE = {
    "limit": LIMIT,
    "offset": OFFSET,
    "total": TOTAL,
    "values": [
        {
            "id": "01J4HC5WQB3FK3FA1FMXYVYJ6Y",
            "name": "Cooking",
            "description": "Make a meal"
        },
        {
            "id": "05J4HC5WQB3FK3FA1FMXYGFJ7B",
            "name": "Walking",
            "description": "Walk the dog"
        }
    ]
}


@dataclass
class GetTasksOperation(Operation):
    def __post_init__(self) -> None:
        self.tags = ["tasks"]
        self.summary = SUMMARY
        self.description = DESCRIPTION
        self.parameters = [
            Parameter(
                name="limit",
                param_in="query",
                required=False,
                schema=Schema(
                    type=OpenAPIType.INTEGER,
                    description="Record limit",
                    default=LIMIT
                )
            ),
            Parameter(
                name="offset",
                param_in="query",
                required=False,
                schema=Schema(
                    type=OpenAPIType.INTEGER,
                    description="Current page",
                    default=OFFSET
                )
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
                                "limit": BaseParameterSchema.limit,
                                "offset": BaseParameterSchema.offset,
                                "total": BaseParameterSchema.total,
                                "values": Schema(
                                    type=OpenAPIType.OBJECT,
                                    description="Tasks",
                                    properties={
                                        "id": TaskParameterSchema.id,
                                        "name": TaskParameterSchema.name,
                                        "description": TaskParameterSchema.description
                                    }
                                )
                            }
                        ),
                        example=RESPONSE_EXAMPLE
                    )
                }
            )
        }
