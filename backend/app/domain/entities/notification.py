from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    id: int | None
    user_id: int
    title: str
    message: str
    is_read: bool = False
    created_at: datetime | None = None
