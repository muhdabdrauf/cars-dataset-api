from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry

REQUEST_COUNT = Counter(
    'car_api_requests_total',
    'Total HTTP  requests',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'car_api_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)
IN_PROGRESS = Gauge(
    'car_api_inprogress_requests',
    'Number of in-progress requests'
)  

def metrics_response():
    payload = generate_latest()
    return payload, CONTENT_TYPE_LATEST