from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model.base import BaseModel


class Tasks(BaseModel):
    __tablename__ = "tasks"

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
