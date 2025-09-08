from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response
from fastapi.responses import ORJSONResponse
from routers import health_router, assess_router, plan_router, act_router, brief_router, chat_router
from core.config import Settings
from core.security import SecurityMiddleware, cors_config
from core.logging import configure as configure_logging, RequestLoggingMiddleware
import os


def get_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Codexia API", version=os.getenv("APP_VERSION","0.1.0"), default_response_class=ORJSONResponse)

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CORSMiddleware, **cors_config())
    app.add_middleware(SecurityMiddleware)

    settings = Settings()  # ensures paths exist

    app.include_router(health_router)
    app.include_router(assess_router)
    app.include_router(plan_router)
    app.include_router(act_router)
    app.include_router(brief_router)
    app.include_router(chat_router)

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app

app = get_app()
