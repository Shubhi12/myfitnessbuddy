from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.dto.auth_dto import AdminRegisterDTO, LoginDTO, RegisterDTO
from app.core.di.container import ServiceContainer
from app.presentation.api.deps import get_services
from app.presentation.schemas.auth import (
    AdminRegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    body: RegisterRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> TokenResponse:
    dto = RegisterDTO(
        email=body.email,
        password=body.password,
        full_name=body.full_name,
        community_id=body.community_id,
        phone=body.phone,
    )
    tokens = await services.auth.register(dto)
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
    )


@router.post("/admin/register", response_model=TokenResponse, status_code=201)
async def register_admin(
    body: AdminRegisterRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> TokenResponse:
    dto = AdminRegisterDTO(
        email=body.email,
        password=body.password,
        full_name=body.full_name,
        phone=body.phone,
        community_name=body.community_name,
        community_address=body.community_address,
        community_city=body.community_city,
        community_pincode=body.community_pincode,
    )
    tokens = await services.auth.register_admin(dto)
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
    )


@router.post("/admin/login", response_model=TokenResponse)
async def login_admin(
    body: LoginRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> TokenResponse:
    tokens = await services.auth.login_admin(LoginDTO(email=body.email, password=body.password))
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> TokenResponse:
    tokens = await services.auth.login(LoginDTO(email=body.email, password=body.password))
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    body: RefreshTokenRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> TokenResponse:
    tokens = await services.auth.refresh_token(body.refresh_token)
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
    )
