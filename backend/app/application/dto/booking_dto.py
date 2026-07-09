from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.booking_status import BookingStatus


@dataclass
class BookingCreateDTO:
    user_id: int
    amenity_id: int
    start_time: datetime
    end_time: datetime
    notes: str | None = None


@dataclass
class BookingCancelDTO:
    booking_id: int
    user_id: int


@dataclass
class BookingDTO:
    id: int
    user_id: int
    amenity_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    notes: str | None
    created_at: datetime | None = None
