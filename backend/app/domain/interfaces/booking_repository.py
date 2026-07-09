from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.entities.booking import Booking


class BookingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, booking_id: int) -> Booking | None:
        ...

    @abstractmethod
    async def create(self, booking: Booking) -> Booking:
        ...

    @abstractmethod
    async def update(self, booking: Booking) -> Booking:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: int) -> list[Booking]:
        ...

    @abstractmethod
    async def list_by_amenity(self, amenity_id: int) -> list[Booking]:
        ...

    @abstractmethod
    async def find_conflicts(
        self, amenity_id: int, start_time: datetime, end_time: datetime
    ) -> list[Booking]:
        ...
