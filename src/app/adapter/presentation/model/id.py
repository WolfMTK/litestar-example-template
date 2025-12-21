from pydantic import Field

from .base import Base


class JsonId(Base):
    id: str = Field(
        ...,
        json_schema_extra={
            "title": "id",
            "description": "Unique identifier",
            "example": "01J4HC5WQB3FK3FA1FMXYVYJ6Y"
        }
    )
