from fastapi import APIRouter, Response
from app.metrics import metrics_response

router = APIRouter(tags=["Observability"])

@router.get("/metrics", summary="Prometheus Metrics Endpoint")
def get_metrics():
    payload, content_type = metrics_response()
    return Response(content=payload, media_type=content_type)

@router.get("/health", summary="Health Check Endpoint")
def health_check():
    return {"status": "healthy"}