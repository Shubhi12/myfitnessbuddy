from dataclasses import dataclass
from datetime import datetime


@dataclass
class Community:
    id: int | None
    name: str
    address: str
    city: str
    pincode: str
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
