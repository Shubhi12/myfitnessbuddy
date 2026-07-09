from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums.user_role import UserRole


@dataclass
class User:
    id: int | None
    email: str
    full_name: str
    phone: str | None
    role: UserRole
    community_id: int
    is_active: bool = True
    hashed_password: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None
