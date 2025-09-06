from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, assess, plan, act, brief

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(assess.router, prefix="/v1")
app.include_router(plan.router, prefix="/v1")
app.include_router(act.router, prefix="/v1")
app.include_router(brief.router, prefix="/v1")
