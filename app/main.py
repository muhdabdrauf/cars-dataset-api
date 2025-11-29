from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors import http_error_handler, validation_exception_handler
from app.limits import limiter, rate_limit_exceeded_handler
from app.database import Base, engine
from app.routers import cars
from app.routers.observability import router as observability_router
from app.logging_config import setup_logging
from app.middleware import logging_metrics_middleware

# Setup logging
setup_logging()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Dataset API",
    description="""
A RESTful API for managing car data including brands, models, colors, and purchase information.  
Supports CRUD operations, filtering, pagination, and API key security.
""",
    version="1.0.0",
)

#limiter middleware
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)

#register middleware
app.middleware("http")(logging_metrics_middleware)

# Register routers
app.include_router(cars.router)
app.include_router(observability_router) # health check and metrics

# Register global error handlers
app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
@limiter.limit("20/minute")
def root(request: Request):
    return {"message": "Welcome to the Car API"}