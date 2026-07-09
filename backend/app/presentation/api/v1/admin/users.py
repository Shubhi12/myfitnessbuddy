from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.dto.user_dto import UserListQueryDTO
from app.core.di.container import ServiceContainer
from app.domain.entities.user import User
from app.presentation.api.deps import get_admin_user, get_services
from app.presentation.schemas.user import UserResponse

router = APIRouter(prefix="/admin/users", tags=["Admin - Users"])


@router.get("", response_model=list[UserResponse])
async def list_users(
    services: Annotated[ServiceContainer, Depends(get_services)],
    admin: Annotated[User, Depends(get_admin_user)],
    skip: int = 0,
    limit: int = 50,
) -> list[User]:
    return await services.user.list_by_community(
        UserListQueryDTO(community_id=admin.community_id, skip=skip, limit=limit)
    )
