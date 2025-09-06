import logging
from .config import settings


def configure() -> None:
    logging.basicConfig(level=getattr(logging, settings.log_level, "INFO"))
