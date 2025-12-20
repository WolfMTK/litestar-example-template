from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin, RedocRenderPlugin

from app.adapter.presentation.controllers import TaskController
from app.config import load_config, ApplicationConfig
from app.provider import AppProvider


def get_app() -> Litestar:
    config = load_config()
    container = make_async_container(
        AppProvider(),
        context={
            ApplicationConfig: config,
        },
    )
    app = Litestar(
        debug=config.debug,
        route_handlers=[TaskController],
        openapi_config=OpenAPIConfig(
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
        ),
    )
    setup_dishka(container=container, app=app)
    return app
