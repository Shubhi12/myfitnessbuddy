from app.core.config.logging_config import get_logger
from app.infrastructure.celery.app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="send_notification")
def send_notification_task(user_id: int, title: str, message: str) -> dict[str, str]:
    logger.info("Sending notification to user %s: %s", user_id, title)
    return {"status": "sent", "user_id": str(user_id), "title": title}
