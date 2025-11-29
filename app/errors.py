from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse 
from fastapi.exception_handlers import RequestValidationError


async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": exc.detail if isinstance(exc.detail, str) else exc.__class__.__name__,
            "details": str(exc.detail),
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "error": "Validation Error",
            "details": exc.errors(),
        },
    )