from dataclasses import dataclass

from app.domain.entities.notification import Notification
from app.domain.interfaces.notification_repository import NotificationRepository


@dataclass
class NotificationService:
    notification_repo: NotificationRepository

    async def list_for_user(self, user_id: int, unread_only: bool = False) -> list[Notification]:
        return await self.notification_repo.list_by_user(user_id, unread_only)

    async def mark_as_read(self, notification_id: int) -> None:
        await self.notification_repo.mark_as_read(notification_id)
