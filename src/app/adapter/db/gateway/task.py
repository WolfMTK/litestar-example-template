from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.model.id import Id
from app.domain.model.task import Task, TaskList


class TaskGateway:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, task: Task) -> Task:
        query = text(
            """
            INSERT INTO 
                tasks (id, name, description)
            VALUES 
                (:id, :name, :description) 
            RETURNING
                    id, name, description
            """
        )
        result = await self.session.execute(
            statement=query,
            params={
                "id": str(task.id),
                "name": task.name,
                "description": task.description,
            }
        )
        row = result.fetchone()
        return Task(
            id=row.id,
            name=row.name,
            description=row.description,
        )

    async def get(self, task_id: Id) -> Task | None:
        query = text(
            """
            SELECT 
                t.id, t.name, t.description
            FROM 
                tasks t
            WHERE 
                t.id = :id
            """
        )
        result = await self.session.execute(
            statement=query,
            params={
                "id": str(task_id),
            }
        )
        row = result.fetchone()
        if not row:
            return None
        return Task(
            id=row.id,
            name=row.name,
            description=row.description,
        )

    async def get_list(self, limit: int, offset: int) -> TaskList:
        query = text(
            """
            SELECT 
                t.id, t.name, t.description
            FROM 
                tasks t
            ORDER BY 
                t.id 
            LIMIT
                :limit
            OFFSET 
                :offset
            """
        )
        result = await self.session.execute(
            statement=query,
            params={
                "limit": limit,
                "offset": limit * offset,
            }
        )
        rows = result.fetchall()
        return TaskList(
            limit=limit,
            offset=offset,
            total=await self._get_total(),
            values=[Task(
                id=row.id,
                name=row.name,
                description=row.description,
            ) for row in rows]
        )

    async def update(self, task: Task) -> Task:
        query = text(
            """
            UPDATE
                tasks t
            SET 
                name = :name,
                description = :description
            WHERE 
                t.id = :id 
            RETURNING
                t.id, t.name, t.description
            """
        )
        result = await self.session.execute(
            statement=query,
            params={
                "id": str(task.id),
                "name": task.name,
                "description": task.description,
            }
        )
        row = result.fetchone()
        return Task(
            id=row.id,
            name=row.name,
            description=row.description,
        )

    async def delete(self, task_id: Id) -> None:
        query = text(
            """
            DELETE FROM
                tasks t
            WHERE
                 t.id = :id
            """
        )
        await self.session.execute(
            statement=query,
            params={
                "id": str(task_id),
            }
        )

    async def _get_total(self) -> int:
        query = text(
            """
            SELECT 
                COUNT(t.id) total
            FROM 
                tasks t
            """
        )
        result = await self.session.execute(
            statement=query,
        )
        row = result.fetchone()
        return row.total
