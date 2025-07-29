from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.product import router as product_router
from app.routers.order import router as order_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(product_router, prefix="/product", tags=["product"])
api_router.include_router(order_router, prefix="/order", tags=["order"])
