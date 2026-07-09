from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.config.logging_config import get_logger
from app.core.exceptions.base import AppException

logger = get_logger(__name__)


async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    logger.warning("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "details": exc.details},
    )


async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
