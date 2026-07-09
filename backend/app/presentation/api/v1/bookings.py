from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.dto.booking_dto import BookingCancelDTO, BookingCreateDTO
from app.core.di.container import ServiceContainer
from app.domain.entities.booking import Booking
from app.domain.entities.user import User
from app.presentation.api.deps import get_admin_user, get_current_user, get_services
from app.presentation.schemas.booking import BookingCreateRequest, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/me", response_model=list[BookingResponse])
async def list_my_bookings(
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> list[Booking]:
    return await services.booking.list_user_bookings(current_user.id)  # type: ignore[arg-type]


@router.post("", response_model=BookingResponse, status_code=201)
async def create_booking(
    body: BookingCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> Booking:
    return await services.booking.create_booking(
        BookingCreateDTO(
            user_id=current_user.id,  # type: ignore[arg-type]
            amenity_id=body.amenity_id,
            start_time=body.start_time,
            end_time=body.end_time,
            notes=body.notes,
        )
    )


@router.delete("/{booking_id}", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
) -> Booking:
    return await services.booking.cancel_booking(
        BookingCancelDTO(booking_id=booking_id, user_id=current_user.id)  # type: ignore[arg-type]
    )


@router.get("/amenity/{amenity_id}", response_model=list[BookingResponse])
async def list_amenity_bookings(
    amenity_id: int,
    services: Annotated[ServiceContainer, Depends(get_services)],
    _admin: Annotated[User, Depends(get_admin_user)],
) -> list[Booking]:
    return await services.booking.list_amenity_bookings(amenity_id)
