from prometheus_client import Counter, Histogram
from .config import Settings

_settings = Settings()

REQUESTS_TOTAL = Counter(
    f"{_settings.METRICS_NAMESPACE}_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    f"{_settings.METRICS_NAMESPACE}_request_latency_seconds",
    "HTTP request latency, in seconds",
    ["method", "path"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2],
)

RATE_LIMIT_DROPPED = Counter(
    f"{_settings.METRICS_NAMESPACE}_rate_limit_dropped_total",
    "Requests dropped due to rate limiting",
    ["path"],
)


def record_request(method: str, path: str, status: int, dur_s: float) -> None:
    REQUESTS_TOTAL.labels(method=method, path=path, status=str(status)).inc()
    REQUEST_LATENCY.labels(method=method, path=path).observe(dur_s)


def inc_rate_limited(path: str) -> None:
    RATE_LIMIT_DROPPED.labels(path=path).inc()
