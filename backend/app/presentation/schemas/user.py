from datetime import datetime

from pydantic import EmailStr

from app.domain.enums.user_role import UserRole
from app.presentation.schemas.common import BaseSchema


class UserResponse(BaseSchema):
    id: int
    email: EmailStr
    full_name: str
    phone: str | None
    role: UserRole
    community_id: int
    is_active: bool
    created_at: datetime | None = None


class UserUpdateRequest(BaseSchema):
    full_name: str | None = None
    phone: str | None = None
