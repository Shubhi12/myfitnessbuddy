from dataclasses import dataclass
from datetime import datetime, time

from app.domain.enums.amenity_type import AmenityType


@dataclass
class AmenityCreateDTO:
    community_id: int
    name: str
    amenity_type: AmenityType
    description: str | None
    capacity: int
    open_time: time
    close_time: time
    slot_duration_minutes: int = 60


@dataclass
class AmenityDTO:
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
