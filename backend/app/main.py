import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    analytics_routes,
    auth_routes,
    budget_routes,
    chat_routes,
    goal_routes,
    receipt_routes,
    transaction_routes,
)
from app.core.config import settings
from app.db.session import check_database_connection, init_db

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


def _masked_database_url() -> str:
    if "://" not in settings.DATABASE_URL or "@" not in settings.DATABASE_URL:
        return settings.DATABASE_URL
    scheme, rest = settings.DATABASE_URL.split("://", 1)
    host_part = rest.split("@", 1)[1]
    return f"{scheme}://***@{host_part}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("%s API starting", settings.APP_NAME)
    logger.info("Environment: %s", settings.ENVIRONMENT)
    logger.info("Database: %s", _masked_database_url())

    try:
        init_db()
        logger.info("Database initialized")
    except Exception:
        logger.exception("Database initialization failed")
        if settings.is_production:
            raise

    yield

    logger.info("%s API shutdown", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal finance management platform",
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
    lifespan=lifespan,
)


# CORS middleware
cors_origins = (
    ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"]
    if settings.DEBUG
    else settings.CORS_ORIGINS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)



@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )
    if settings.is_production:
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains",
        )
    return response

app.include_router(auth_routes.router)
app.include_router(transaction_routes.router)
app.include_router(analytics_routes.router)
app.include_router(budget_routes.router)
app.include_router(goal_routes.router)
app.include_router(receipt_routes.router)
app.include_router(chat_routes.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Finnova AI API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if check_database_connection() else "unavailable",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
