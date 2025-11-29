from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# Create limiter using client IP
limiter = Limiter(key_func=get_remote_address)

# Custom JSON response when rate limit is hit
async def rate_limit_exceeded_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "status": 429,
            "error": "Too Many Requests",
            "detail": f"Rate limit exceeded: {exc.detail}"
        }
    )
