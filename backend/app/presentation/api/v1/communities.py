from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.di.container import ServiceContainer
from app.domain.entities.community import Community
from app.presentation.api.deps import get_admin_user, get_services
from app.presentation.schemas.community import CommunityCreateRequest, CommunityResponse

router = APIRouter(prefix="/communities", tags=["Communities"])


@router.get("", response_model=list[CommunityResponse])
async def list_communities(
    services: Annotated[ServiceContainer, Depends(get_services)],
    skip: int = 0,
    limit: int = 50,
) -> list[Community]:
    return await services.community.list_all(skip, limit)


@router.get("/{community_id}", response_model=CommunityResponse)
async def get_community(
    community_id: int,
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> Community:
    return await services.community.get_by_id(community_id)


@router.post("", response_model=CommunityResponse, status_code=201)
async def create_community(
    body: CommunityCreateRequest,
    services: Annotated[ServiceContainer, Depends(get_services)],
    _admin: Annotated[object, Depends(get_admin_user)],
) -> Community:
    community = Community(
        id=None,
        name=body.name,
        address=body.address,
        city=body.city,
        pincode=body.pincode,
    )
    return await services.community.create(community)
