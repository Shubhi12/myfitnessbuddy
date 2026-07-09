from datetime import datetime

from app.presentation.schemas.common import BaseSchema


class CommunityResponse(BaseSchema):
    id: int
    name: str
    address: str
    city: str
    pincode: str
    is_active: bool
    created_at: datetime | None = None


class CommunityCreateRequest(BaseSchema):
    name: str
    address: str
    city: str
    pincode: str
