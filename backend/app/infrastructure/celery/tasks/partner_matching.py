from app.core.config.logging_config import get_logger
from app.infrastructure.celery.app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="process_partner_matching")
def process_partner_matching_task(user_id: int) -> dict[str, str]:
    logger.info("Processing partner matching for user %s", user_id)
    return {"status": "processed", "user_id": str(user_id)}
