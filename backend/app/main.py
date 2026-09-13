from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.errors import AppError, app_error_handler, generic_exception_handler
from app.api.routes import health_router, sessions_router, chat_router, artifacts_router

setup_logging()

app = FastAPI(
    title="Lenny Growth Assistant API",
    description="Backend API for Lenny Growth Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(health_router)
app.include_router(sessions_router)
app.include_router(chat_router)
app.include_router(artifacts_router)
