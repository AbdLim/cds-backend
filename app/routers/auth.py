from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from uuid import UUID

from app.config.database import get_session
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    Token,
    TokenRefresh,
    RefreshRequest,
)
from app.services.auth import AuthService
from app.dependencies.auth import get_current_user_id

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session),
):
    auth_service = AuthService(session)
    return await auth_service.authenticate_user(login_data.email, login_data.password)


@router.post("/register", response_model=Token)
async def register(
    register_data: RegisterRequest,
    session: Session = Depends(get_session),
):
    auth_service = AuthService(session)
    return await auth_service.register_user(register_data.model_dump())


@router.post("/refresh", response_model=TokenRefresh)
async def refresh_token(
    refresh_data: RefreshRequest,
    session: Session = Depends(get_session),
):
    auth_service = AuthService(session)
    return await auth_service.refresh_token(refresh_data.refresh_token)


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    auth_service = AuthService(session)
    return await auth_service.logout(token)


@router.post("/logout-all")
async def logout_all(
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    auth_service = AuthService(session)
    return await auth_service.logout_all(current_user_id)
