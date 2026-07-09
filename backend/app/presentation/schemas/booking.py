from datetime import datetime

from app.domain.enums.booking_status import BookingStatus
from app.presentation.schemas.common import BaseSchema


class BookingResponse(BaseSchema):
    id: int
    user_id: int
    amenity_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    notes: str | None
    created_at: datetime | None = None


class BookingCreateRequest(BaseSchema):
    amenity_id: int
    start_time: datetime
    end_time: datetime
    notes: str | None = None
