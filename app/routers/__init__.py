from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.attendance import router as attendance_router
from app.routers.admin import router as admin_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(attendance_router, prefix="/attendance", tags=["attendance"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
