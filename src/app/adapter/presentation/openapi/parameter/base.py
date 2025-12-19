from dataclasses import dataclass

from litestar.openapi.spec import (
    Schema,
    OpenAPIType,
)


@dataclass
class BaseParameterSchema:
    status_code: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="HTTP Status Code"
    )
    detail: Schema = Schema(
        type=OpenAPIType.STRING,
        description="Error description"
    )
    limit: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Record limit"
    )
    offset: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Current page"
    )
    total: Schema = Schema(
        type=OpenAPIType.INTEGER,
        description="Number of records"
    )
