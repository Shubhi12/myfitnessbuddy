from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.match_status import MatchStatus


@dataclass
class PartnerMatch:
    id: int | None
    requester_id: int
    recipient_id: int
    status: MatchStatus
    message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
