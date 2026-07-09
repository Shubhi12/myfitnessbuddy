from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.user_role import UserRole


@dataclass
class UserUpdateDTO:
    full_name: str | None = None
    phone: str | None = None


@dataclass
class UserListQueryDTO:
    community_id: int
    skip: int = 0
    limit: int = 50


@dataclass
class UserDTO:
    id: int
    email: str
    full_name: str
    phone: str | None
    role: UserRole
    community_id: int
    is_active: bool
    created_at: datetime | None = None
