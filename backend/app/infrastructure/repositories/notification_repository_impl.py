from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.notification import Notification
from app.domain.interfaces.notification_repository import NotificationRepository
from app.infrastructure.database.models.notification_model import NotificationModel


def _to_entity(model: NotificationModel) -> Notification:
    return Notification(
        id=model.id,
        user_id=model.user_id,
        title=model.title,
        message=model.message,
        is_read=model.is_read,
        created_at=model.created_at,
    )


class NotificationRepositoryImpl(NotificationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, notification: Notification) -> Notification:
        model = NotificationModel(
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            is_read=notification.is_read,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list_by_user(self, user_id: int, unread_only: bool = False) -> list[Notification]:
        stmt = select(NotificationModel).where(NotificationModel.user_id == user_id)
        if unread_only:
            stmt = stmt.where(NotificationModel.is_read.is_(False))
        result = await self._session.scalars(stmt)
        return [_to_entity(m) for m in result.all()]

    async def mark_as_read(self, notification_id: int) -> None:
        model = await self._session.get(NotificationModel, notification_id)
        if model:
            model.is_read = True
            await self._session.flush()
