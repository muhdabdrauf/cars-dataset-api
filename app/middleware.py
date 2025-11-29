import time 
import logging
from fastapi import Request
from starlette.responses import Response
from app.metrics import REQUEST_COUNT, REQUEST_LATENCY, IN_PROGRESS

logger = logging.getLogger("app.middleware")

async def logging_metrics_middleware(request: Request, call_next):
    start = time.time()
    IN_PROGRESS.inc()
    try:
        response: Response = await call_next(request)
        status = response.status_code
        return response
    except Exception as exc:
        status = 500
        raise
    finally:
        duration = time.time() - start
        IN_PROGRESS.dec()

        try:
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                http_status=status
            ).inc()
        except Exception:
            pass
        logger.info(
            "request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status":status,
                "duration": duration,  
                "client": request.client.host if request.client else None,
            }
        )