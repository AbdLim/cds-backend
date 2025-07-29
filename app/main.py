from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config.database import init_db
from app.config import settings
from app.config.logging import setup_logging, logger
from app.routers import api_router


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down application...")


def init_app() -> FastAPI:
    # Set up logging
    setup_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    logger.info(f"Application {settings.PROJECT_NAME} v{settings.VERSION} initialized")
    return app


app = init_app()


@app.get("/")
async def root():
    return {
        "message": "Welcome to CDS API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


def start():
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)
