from dataclasses import dataclass

from litestar.openapi.spec import (
    Schema,
    OpenAPIType,
)


@dataclass
class TaskParameterSchema:
    id: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Unique identifier"
    )
    name: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Task name"
    )
    description: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Task Description"
    )
    task_id: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Unique identifier",
        default="01J4HC5WQB3FK3FA1FMXYVYJ6Y"
    )
