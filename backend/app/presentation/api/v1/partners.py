from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.dto.partner_dto import PartnerRequestDTO, PartnerRespondDTO
from app.core.di.container import ServiceContainer
from app.domain.entities.partner_match import PartnerMatch
from app.domain.entities.user import User
from app.presentation.api.deps import get_current_user, get_services
from app.presentation.schemas.partner import (
    PartnerMatchResponse,
    PartnerRequestCreate,
    PartnerRespondRequest,
)

router = APIRouter(prefix="/partners", tags=["Partner Matching"])


@router.get("/matches", response_model=list[PartnerMatchResponse])
async def list_matches(
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> list[PartnerMatch]:
    return await services.partner_matching.list_matches(current_user.id)  # type: ignore[arg-type]


@router.post("/request", response_model=PartnerMatchResponse, status_code=201)
async def send_partner_request(
    body: PartnerRequestCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> PartnerMatch:
    return await services.partner_matching.send_request(
        PartnerRequestDTO(
            requester_id=current_user.id,  # type: ignore[arg-type]
            recipient_id=body.recipient_id,
            message=body.message,
        )
    )


@router.patch("/matches/{match_id}/respond", response_model=PartnerMatchResponse)
async def respond_to_match(
    match_id: int,
    body: PartnerRespondRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> PartnerMatch:
    return await services.partner_matching.respond_to_request(
        PartnerRespondDTO(
            match_id=match_id,
            user_id=current_user.id,  # type: ignore[arg-type]
            accept=body.accept,
        )
    )
