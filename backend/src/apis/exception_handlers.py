# src/core/exception_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from src.helpers.schemas.api_response import APIResponse
from src.exceptions.base import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            status=exc.status_code,
            message=exc.message,
            data=None,
        ).to_dict(),
    )


async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
):
    # Default
    message = "Database integrity error"
    status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exc.orig, UniqueViolationError):
        message = "Duplicate value violates unique constraint"
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code,
        content=APIResponse(
            status=status_code,
            message=message,
            data=None,
        ).to_dict(),
    )



async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            data=None,
        ).to_dict(),
    )
