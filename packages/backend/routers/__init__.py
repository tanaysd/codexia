from .health import router as health_router
from .assess import router as assess_router
from .plan import router as plan_router
from .act import router as act_router
from .brief import router as brief_router
from .chat import router as chat_router

__all__ = [
    "health_router",
    "assess_router",
    "plan_router",
    "act_router",
    "brief_router",
    "chat_router",
]
