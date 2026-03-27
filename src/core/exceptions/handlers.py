import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.business.organizations.domain.organization_exceptions import OrganizationError
from src.catalogs.activities.domain.activity_exceptions import ActivityError
from src.catalogs.buildings.domain.building_exceptions import BuildingError
from src.core.exceptions.base import AppError

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.warning(f"AppError: {exc.__class__.__name__} - {exc.message} path={request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.__class__.__name__, "message": str(exc), "path": request.url.path}},
        )

    @app.exception_handler(ActivityError)
    @app.exception_handler(BuildingError)
    @app.exception_handler(OrganizationError)
    async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
        if hasattr(exc, "status_code"):
            status_code = exc.status_code
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            if "NotFound" in exc.__class__.__name__:
                status_code = status.HTTP_404_NOT_FOUND

        logger.info(f"Domain error: {exc.__class__.__name__} - {exc!s} path={request.url.path} status={status_code}")

        return JSONResponse(
            status_code=status_code,
            content={"error": {"code": exc.__class__.__name__, "message": str(exc), "path": request.url.path}},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        logger.warning(f"Validation error: {exc} path={request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": {"code": "ValidationError", "message": str(exc)}},
        )

    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        logger.error(f"Integrity error: {exc} path={request.url.path}")

        if "foreign key constraint" in str(exc.orig).lower():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": {
                        "code": "RelatedEntityNotFound",
                        "message": "Указанное здание или деятельность не существуют",
                        "path": request.url.path,
                    }
                },
            )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"code": "InternalServerError", "message": "Database error"}},
        )
