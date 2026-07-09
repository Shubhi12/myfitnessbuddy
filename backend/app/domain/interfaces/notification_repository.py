from abc import ABC, abstractmethod

from app.domain.entities.notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        ...

    @abstractmethod
    async def list_by_user(self, user_id: int, unread_only: bool = False) -> list[Notification]:
        ...

    @abstractmethod
    async def mark_as_read(self, notification_id: int) -> None:
        ...
