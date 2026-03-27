import logging

from dishka.integrations.fastapi import setup_dishka
from fastapi import Depends, FastAPI

from src.business.organizations.api.organization_routers import organization_router
from src.catalogs.activities.api.activity_routers import activity_router
from src.catalogs.buildings.api.building_routers import building_router
from src.core.di_container import get_di_container
from src.core.exceptions.handlers import setup_exception_handlers
from src.core.logging import LoggingMiddleware, setup_logging, setup_logging_handlers
from src.core.security import verify_api_key


def create_app() -> FastAPI:
    setup_logging()
    logger = logging.getLogger(__name__)

    app = FastAPI(title="Geo Catalog API", dependencies=[Depends(verify_api_key)])

    app.add_middleware(LoggingMiddleware)

    container = get_di_container()
    setup_dishka(container, app)

    setup_exception_handlers(app)
    setup_logging_handlers(app)

    app.include_router(activity_router)
    app.include_router(building_router)
    app.include_router(organization_router)

    logger.info("Application started successfully")
    return app


app = create_app()
