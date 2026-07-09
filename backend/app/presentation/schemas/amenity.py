from datetime import datetime, time

from app.domain.enums.amenity_type import AmenityType
from app.presentation.schemas.common import BaseSchema


class AmenityResponse(BaseSchema):
    id: int
    community_id: int
    name: str
    amenity_type: AmenityType
    description: str | None
    capacity: int
    open_time: time
    close_time: time
    slot_duration_minutes: int
    is_active: bool
    created_at: datetime | None = None


class AmenityCreateRequest(BaseSchema):
    community_id: int
    name: str
    amenity_type: AmenityType
    description: str | None = None
    capacity: int = 1
    open_time: time
    close_time: time
    slot_duration_minutes: int = 60
