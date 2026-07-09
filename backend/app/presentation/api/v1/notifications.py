from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.di.container import ServiceContainer
from app.domain.entities.notification import Notification
from app.domain.entities.user import User
from app.presentation.api.deps import get_current_user, get_services
from app.presentation.schemas.common import MessageResponse
from app.presentation.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    current_user: Annotated[User, Depends(get_current_user)],
    services: Annotated[ServiceContainer, Depends(get_services)],
    unread_only: bool = False,
) -> list[Notification]:
    return await services.notification.list_for_user(
        current_user.id,  # type: ignore[arg-type]
        unread_only=unread_only,
    )


@router.patch("/{notification_id}/read", response_model=MessageResponse)
async def mark_notification_read(
    notification_id: int,
    services: Annotated[ServiceContainer, Depends(get_services)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> MessageResponse:
    await services.notification.mark_as_read(notification_id)
    return MessageResponse(message="Notification marked as read")
