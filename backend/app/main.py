from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.logging_config import setup_logging
from app.core.config.settings import get_settings
from app.core.exceptions import AppException, app_exception_handler, unhandled_exception_handler
from app.core.middleware.logging import LoggingMiddleware
from app.core.middleware.request_id import RequestIDMiddleware
from app.infrastructure.cache.redis_client import close_redis_client
from app.presentation.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    setup_logging()
    yield
    await close_redis_client()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Gated community fitness partner matching and amenity booking platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_origin_regex=settings.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        return {"status": "healthy", "service": settings.app_name}

    return app


app = create_app()
