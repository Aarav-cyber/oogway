from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import uuid
import logging

logger = logging.getLogger("lenny_backend")


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class SessionNotFoundError(AppError):
    def __init__(self, session_id: str):
        super().__init__(
            code="SESSION_NOT_FOUND",
            message=f"Session '{session_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class LLMUnavailableError(AppError):
    def __init__(self, provider: str, details: str = ""):
        msg = f"The requested LLM provider '{provider}' is unavailable."
        if details:
            msg += f" Details: {details}"
        super().__init__(
            code="LLM_UNAVAILABLE",
            message=msg,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class LLMConfigurationError(AppError):
    def __init__(self, details: str):
        super().__init__(
            code="LLM_CONFIGURATION_ERROR",
            message=f"LLM Configuration Error: {details}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class DatabaseError(AppError):
    def __init__(self, details: str = "A database error occurred."):
        super().__init__(
            code="DATABASE_ERROR",
            message=details,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class RetrievalError(AppError):
    def __init__(self, details: str = "Error retrieving transcript chunks."):
        super().__init__(
            code="RETRIEVAL_ERROR",
            message=details,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class ArtifactGenerationError(AppError):
    def __init__(self, details: str = "Error generating artifact."):
        super().__init__(
            code="ARTIFACT_GENERATION_ERROR",
            message=details,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def app_error_handler(request: Request, exc: AppError):
    request_id = str(uuid.uuid4())
    logger.error(
        f"AppError [{exc.code}]: {exc.message}",
        extra={"request_id": request_id, "error_code": exc.code, "path": request.url.path}
    )
    headers = {
        "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
        "Access-Control-Allow-Credentials": "true",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request_id,
            }
        },
        headers=headers,
    )


async def generic_exception_handler(request: Request, exc: Exception):
    request_id = str(uuid.uuid4())
    logger.exception(
        f"Unhandled exception on {request.url.path}",
        extra={"request_id": request_id, "error_code": "INTERNAL_SERVER_ERROR"}
    )
    headers = {
        "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
        "Access-Control-Allow-Credentials": "true",
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred.",
                "request_id": request_id,
            }
        },
        headers=headers,
    )
