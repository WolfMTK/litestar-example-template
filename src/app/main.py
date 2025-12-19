from typing import AsyncIterable

from litestar import Litestar
from litestar.datastructures import State
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin, RedocRenderPlugin
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import load_config, ApplicationConfig
from app.infrastructure.db import get_engine, get_session_maker, get_async_session
from app.ioc import IoC
from app.adapter.presentation.controllers import TaskController


async def _get_session(state: State) -> AsyncIterable[AsyncSession]:
    session_maker: async_sessionmaker[AsyncSession] = state.session_maker
    async for session in get_async_session(session_maker):
        yield session


def create_app() -> Litestar:
    config = load_config()

    engine = get_engine(config.db.url)
    session_maker = get_session_maker(engine)

    app = Litestar(
        debug=config.debug,
        route_handlers=[TaskController],
        dependencies={
            "session": Provide(_get_session),
            "ioc": Provide(IoC, sync_to_thread=True),
        },
        openapi_config=_init_openapi_config()
    )
    app.state.session_maker = session_maker
    return app


def _init_openapi_config() -> OpenAPIConfig:
    config = OpenAPIConfig(
        title="Example Service",
        description="Example service",
        version="0.0.1",
        render_plugins=[
            SwaggerRenderPlugin(),
            RedocRenderPlugin(),
        ],
        # components=Components(
        #     security_schemes={
        #         "BearerToken": SecurityScheme(
        #             type="http",
        #             scheme="bearer"
        #         )
        #     }
        # )
    )
    return config


def _init_dependencies(config: ApplicationConfig) -> dict[str, Provide]:
    db_config = config.db

    dependencies = {
        "session": Provide(create_async_session_maker(db_config.url)),
        "ioc": Provide(IoC, sync_to_thread=True),
    }
    return dependencies
