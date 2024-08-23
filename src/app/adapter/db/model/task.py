from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model.base import BaseModel
from app.domain.model.task import Task


class Tasks(BaseModel):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False,
    )
    name: Mapped[str] = mapped_column(
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        nullable=False,
    )

    def into(self) -> Task:
        return Task(
            id=self.id,
            name=self.name,
            description=self.description
        )
