from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.auth_dto import LoginDTO, RegisterDTO
from app.core.di.container import ServiceContainer, build_services
from app.core.exceptions.base import AppException
from app.core.security.jwt import decode_token
from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole
from app.infrastructure.database.session import get_db_session

security = HTTPBearer()


async def get_services(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ServiceContainer:
    return build_services(session)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user_id = int(payload["sub"])
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = await services.user.get_by_id(user_id)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
