from collections.abc import Iterator

from sqlalchemy import insert, update, case, select, func, delete

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import Tasks
from app.domain.model.id import Id
from app.domain.model.task import Task


class TaskGateway(BaseGateway[Task]):
    async def insert(self, source: Task) -> Task:
        stmt = (
            insert(Tasks)
            .values(
                id=source.id,
                name=source.name,
                description=source.description
            )
            .returning(Tasks)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one().into()

    async def update(self, source: Task) -> Task:
        stmt = (
            update(Tasks)
            .where(
                Tasks.id == source.id
            )
            .values(
                name=case(
                    (source.name is not None, source.name),
                    else_=Tasks.name
                ),
                description=case(
                    (source.description is not None, source.description),
                    else_=Tasks.description
                )
            )
            .returning(Tasks)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()

    async def get(self, source: Id) -> Task | None:
        stmt = (
            select(Tasks)
            .where(
                Tasks.id == source
            )
        )
        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()
        if model is not None:
            return model.into()
        return model

    async def get_list(
            self,
            limit: int,
            offset: int
    ) -> Iterator[Task]:
        stmt = (
            select(Tasks)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return (task.into() for task in result.scalars())

    async def get_total(self) -> int:
        stmt = (
            select(
                func.count(
                    Tasks.id
                )
            )
        )
        result = await self.session.scalar(stmt)
        return result

    async def check_task(self, source: Id) -> bool:
        stmt = select(
            select(Tasks)
            .where(
                Tasks.id == source
            )
            .exists()
        )
        result = await self.session.scalar(stmt)
        return result

    async def delete(self, source: Id) -> Task:
        stmt = (
            delete(Tasks)
            .where(Tasks.id == source)
            .returning(Tasks)
        )
        result = await self.session.execute(stmt)
        return result.scalar().into()
