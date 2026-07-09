from dataclasses import dataclass

from app.application.dto.booking_dto import BookingCancelDTO, BookingCreateDTO
from app.core.exceptions.base import ConflictError, ForbiddenError, NotFoundError
from app.domain.entities.booking import Booking
from app.domain.entities.notification import Notification
from app.domain.enums.booking_status import BookingStatus
from app.domain.interfaces.amenity_repository import AmenityRepository
from app.domain.interfaces.booking_repository import BookingRepository
from app.domain.interfaces.notification_repository import NotificationRepository
from app.infrastructure.celery.tasks.booking_reminders import send_booking_reminder_task


@dataclass
class BookingService:
    booking_repo: BookingRepository
    amenity_repo: AmenityRepository
    notification_repo: NotificationRepository

    async def create_booking(self, dto: BookingCreateDTO) -> Booking:
        amenity = await self.amenity_repo.get_by_id(dto.amenity_id)
        if not amenity or not amenity.is_active:
            raise NotFoundError("Amenity", dto.amenity_id)

        if dto.end_time <= dto.start_time:
            raise ConflictError("End time must be after start time")

        conflicts = await self.booking_repo.find_conflicts(
            dto.amenity_id, dto.start_time, dto.end_time
        )
        if len(conflicts) >= amenity.capacity:
            raise ConflictError("Amenity is fully booked for the selected time slot")

        booking = Booking(
            id=None,
            user_id=dto.user_id,
            amenity_id=dto.amenity_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            status=BookingStatus.CONFIRMED,
            notes=dto.notes,
        )
        created = await self.booking_repo.create(booking)

        await self.notification_repo.create(
            Notification(
                id=None,
                user_id=dto.user_id,
                title="Booking Confirmed",
                message=f"Your booking for {amenity.name} is confirmed.",
            )
        )

        if created.id:
            send_booking_reminder_task.delay(created.id)

        return created

    async def cancel_booking(self, dto: BookingCancelDTO) -> Booking:
        booking = await self.booking_repo.get_by_id(dto.booking_id)
        if not booking:
            raise NotFoundError("Booking", dto.booking_id)
        if booking.user_id != dto.user_id:
            raise ForbiddenError("You can only cancel your own bookings")
        if booking.status in (BookingStatus.CANCELLED, BookingStatus.COMPLETED):
            raise ConflictError("Booking cannot be cancelled")

        booking.status = BookingStatus.CANCELLED
        return await self.booking_repo.update(booking)

    async def list_user_bookings(self, user_id: int) -> list[Booking]:
        return await self.booking_repo.list_by_user(user_id)

    async def list_amenity_bookings(self, amenity_id: int) -> list[Booking]:
        return await self.booking_repo.list_by_amenity(amenity_id)
