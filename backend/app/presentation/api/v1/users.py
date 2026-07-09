from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.dto.user_dto import UserUpdateDTO
from app.core.di.container import ServiceContainer
from app.domain.entities.user import User
from app.presentation.api.deps import get_current_user, get_services
from app.presentation.schemas.user import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UserUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> User:
    return await services.user.update_profile(
        current_user.id,  # type: ignore[arg-type]
        UserUpdateDTO(full_name=body.full_name, phone=body.phone),
    )
