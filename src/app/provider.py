from typing import AsyncIterable

import ulid
from dishka import Provider, from_context, Scope, provide, AnyOf, provide_all
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.adapter.db.gateway import TaskGateway
from app.application.interactor.task import (
    RegisterTaskInteractor,
    GetTaskInteractor,
    GetTaskListInteractor,
    UpdateTaskInteractor,
    DeleteTaskInteractor,
)
from app.application.interface.db import DBSession
from app.application.interface.gateway import ITaskWrite, ITaskRead
from app.application.interface.ulid_generator import ULIDGenerator
from app.config import ApplicationConfig
from app.infrastructure.db import get_engine, get_session_maker


class AppProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=ApplicationConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: ApplicationConfig) -> async_sessionmaker[AsyncSession]:
        db_config = config.db
        engine = get_engine(db_config.url)
        session_maker = get_session_maker(engine)
        return session_maker

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, DBSession]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_ulid_generator(self) -> ULIDGenerator:
        return ulid.ULID

    task_gateway = provide(
        TaskGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            ITaskWrite,
            ITaskRead,
        ]
    )

    interactors = provide_all(
        RegisterTaskInteractor,
        GetTaskInteractor,
        GetTaskListInteractor,
        UpdateTaskInteractor,
        DeleteTaskInteractor,
    )
