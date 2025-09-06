from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response
from fastapi.responses import ORJSONResponse
from .routers import health_router, assess_router, plan_router, act_router, brief_router
from .core.config import Settings
from .core.security import SecurityMiddleware
from .core.logging import configure as configure_logging
import os

_registry = CollectorRegistry()
REQUESTS = Counter("codexia_requests_total", "HTTP requests", ["path"], registry=_registry)


def get_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Codexia API", version=os.getenv("APP_VERSION","0.1.0"), default_response_class=ORJSONResponse)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SecurityMiddleware)

    settings = Settings()  # ensures paths exist

    @app.middleware("http")
    async def metrics_mw(request, call_next):
        resp = await call_next(request)
        try: REQUESTS.labels(path=request.url.path).inc()
        except Exception: pass
        return resp

    app.include_router(health_router)
    app.include_router(assess_router)
    app.include_router(plan_router)
    app.include_router(act_router)
    app.include_router(brief_router)

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(_registry), media_type=CONTENT_TYPE_LATEST)

    return app

app = get_app()
