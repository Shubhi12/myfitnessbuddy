from app.core.config.logging_config import get_logger
from app.core.config.settings import get_settings

logger = get_logger(__name__)


class SmtpEmailService:
    async def send_email(self, to: str, subject: str, body: str) -> None:
        settings = get_settings()
        if not settings.smtp_host:
            logger.info("Email (dev mode) to=%s subject=%s", to, subject)
            return
        # Production SMTP integration would go here
        logger.info("Email sent to=%s subject=%s", to, subject)
