from datetime import datetime

from app.presentation.schemas.common import BaseSchema


class NotificationResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime | None = None
