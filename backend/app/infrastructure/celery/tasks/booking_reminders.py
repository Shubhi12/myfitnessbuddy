from app.core.config.logging_config import get_logger
from app.infrastructure.celery.app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="send_booking_reminder")
def send_booking_reminder_task(booking_id: int) -> dict[str, str]:
    logger.info("Sending booking reminder for booking %s", booking_id)
    return {"status": "sent", "booking_id": str(booking_id)}
