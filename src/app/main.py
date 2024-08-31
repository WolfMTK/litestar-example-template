from litestar import Litestar
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin, RedocRenderPlugin

from app.adapter.persistence.db import create_async_session_maker
from app.config import load_config, ApplicationConfig
from app.ioc import IoC
from app.presentation.controllers.task import TaskController


def create_app() -> Litestar:
    config = load_config()

    app = Litestar(
        debug=config.debug,
        route_handlers=[TaskController],
        dependencies=_init_dependencies(config),
        openapi_config=_init_openapi_config()
    )
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
        "session": Provide(create_async_session_maker(db_config.db_url)),
        "ioc": Provide(IoC, sync_to_thread=True),
    }
    return dependencies
