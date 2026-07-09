from datetime import datetime

from app.domain.enums.match_status import MatchStatus
from app.presentation.schemas.common import BaseSchema


class PartnerMatchResponse(BaseSchema):
    id: int
    requester_id: int
    recipient_id: int
    status: MatchStatus
    message: str | None
    created_at: datetime | None = None


class PartnerRequestCreate(BaseSchema):
    recipient_id: int
    message: str | None = None


class PartnerRespondRequest(BaseSchema):
    accept: bool
