from dataclasses import dataclass
from datetime import datetime, time

from app.domain.enums.amenity_type import AmenityType


@dataclass
class Amenity:
    id: int | None
    community_id: int
    name: str
    amenity_type: AmenityType
    description: str | None
    capacity: int
    open_time: time
    close_time: time
    slot_duration_minutes: int
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
