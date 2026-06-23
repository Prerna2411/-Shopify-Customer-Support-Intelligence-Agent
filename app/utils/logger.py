import logging

from app.utils.config import get_settings


def get_logger(name: str) -> logging.Logger:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    return logging.getLogger(name)
