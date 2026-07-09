from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.match_status import MatchStatus
from app.domain.enums.workout_type import WorkoutType


@dataclass
class PartnerRequestDTO:
    requester_id: int
    recipient_id: int
    message: str | None = None


@dataclass
class PartnerRespondDTO:
    match_id: int
    user_id: int
    accept: bool


@dataclass
class PartnerMatchDTO:
    id: int
    requester_id: int
    recipient_id: int
    status: MatchStatus
    message: str | None
    created_at: datetime | None = None


@dataclass
class PartnerDiscoveryQueryDTO:
    community_id: int
    exclude_user_id: int
    workout_types: list[WorkoutType] | None = None
    skip: int = 0
    limit: int = 20
