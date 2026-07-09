from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.booking import Booking
from app.domain.enums.booking_status import BookingStatus
from app.domain.interfaces.booking_repository import BookingRepository
from app.infrastructure.database.models.booking_model import BookingModel


def _to_entity(model: BookingModel) -> Booking:
    return Booking(
        id=model.id,
        user_id=model.user_id,
        amenity_id=model.amenity_id,
        start_time=model.start_time,
        end_time=model.end_time,
        status=BookingStatus(model.status),
        notes=model.notes,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class BookingRepositoryImpl(BookingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, booking_id: int) -> Booking | None:
        result = await self._session.get(BookingModel, booking_id)
        return _to_entity(result) if result else None

    async def create(self, booking: Booking) -> Booking:
        model = BookingModel(
            user_id=booking.user_id,
            amenity_id=booking.amenity_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            status=booking.status.value,
            notes=booking.notes,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, booking: Booking) -> Booking:
        model = await self._session.get(BookingModel, booking.id)
        if not model:
            raise ValueError(f"Booking {booking.id} not found")
        model.status = booking.status.value
        model.notes = booking.notes
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_by_user(self, user_id: int) -> list[Booking]:
        stmt = select(BookingModel).where(BookingModel.user_id == user_id)
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]

    async def list_by_amenity(self, amenity_id: int) -> list[Booking]:
        stmt = select(BookingModel).where(BookingModel.amenity_id == amenity_id)
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]

    async def find_conflicts(
        self, amenity_id: int, start_time: datetime, end_time: datetime
    ) -> list[Booking]:
        stmt = select(BookingModel).where(
            BookingModel.amenity_id == amenity_id,
            BookingModel.status.in_(
                [BookingStatus.PENDING.value, BookingStatus.CONFIRMED.value]
            ),
            and_(
                BookingModel.start_time < end_time,
                BookingModel.end_time > start_time,
            ),
        )
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]
