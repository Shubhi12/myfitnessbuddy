from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.booking_status import BookingStatus


@dataclass
class Booking:
    id: int | None
    user_id: int
    amenity_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
