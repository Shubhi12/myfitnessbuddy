from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.dto.amenity_dto import AmenityCreateDTO
from app.core.di.container import ServiceContainer
from app.domain.entities.amenity import Amenity
from app.domain.entities.user import User
from app.presentation.api.deps import get_admin_user, get_current_user, get_services
from app.presentation.schemas.amenity import AmenityCreateRequest, AmenityResponse

router = APIRouter(prefix="/amenities", tags=["Amenities"])


@router.get("", response_model=list[AmenityResponse])
async def list_amenities(
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> list[Amenity]:
    return await services.amenity.list_by_community(current_user.community_id)


@router.get("/{amenity_id}", response_model=AmenityResponse)
async def get_amenity(
    amenity_id: int,
    services: Annotated[ServiceContainer, Depends(get_services)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> Amenity:
    return await services.amenity.get_by_id(amenity_id)


@router.post("", response_model=AmenityResponse, status_code=201)
async def create_amenity(
    body: AmenityCreateRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
    _admin: Annotated[User, Depends(get_admin_user)],
) -> Amenity:
    return await services.amenity.create(
        AmenityCreateDTO(
            community_id=body.community_id,
            name=body.name,
            amenity_type=body.amenity_type,
            description=body.description,
            capacity=body.capacity,
            open_time=body.open_time,
            close_time=body.close_time,
            slot_duration_minutes=body.slot_duration_minutes,
        )
    )
