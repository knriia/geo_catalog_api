import logging
import sys
import time
from collections.abc import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        logger = logging.getLogger("api")

        start_time = time.time()

        logger.info(f"→ {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000

            logger.info(
                f"← {request.method} {request.url.path} status={response.status_code} time={process_time:.2f}ms"
            )
            return response

        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"✗ {request.method} {request.url.path} error={type(e).__name__} time={process_time:.2f}ms")
            raise


def setup_logging_handlers(app: FastAPI) -> None:
    logger = logging.getLogger("exceptions")

    original_handlers = app.exception_handlers.copy()

    def log_exception(request: Request, exc: Exception) -> Response:
        logger.error(f"Unhandled exception: {type(exc).__name__}: {exc}", exc_info=True)
        handler = original_handlers.get(type(exc))
        if handler:
            return handler(request, exc)
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    app.add_exception_handler(Exception, log_exception)
