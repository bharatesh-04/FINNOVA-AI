"""Initialize FastAPI API routes"""
from fastapi import APIRouter

from . import auth_routes
from . import transaction_routes
from . import analytics_routes
from . import budget_routes
from . import goal_routes
from . import receipt_routes
from . import chat_routes

api_router = APIRouter(prefix="/api/v1")

# Include routers
api_router.include_router(auth_routes.router)
api_router.include_router(transaction_routes.router)
api_router.include_router(analytics_routes.router)
api_router.include_router(budget_routes.router)
api_router.include_router(goal_routes.router)
api_router.include_router(receipt_routes.router)
api_router.include_router(chat_routes.router)

__all__ = ["api_router"]
