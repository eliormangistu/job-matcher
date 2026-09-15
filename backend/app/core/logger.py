import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def configure_logging() -> None:
    logger = logging.getLogger("job-matcher")

    if logger.handlers:
        return

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "service=%(service)s | action=%(action)s | "
        "%(message)s"
    )

    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


class ServiceLogger:
    def __init__(self, service: str):
        self.service = service
        self.logger = logging.getLogger("job-matcher")

    def info(
        self,
        message: str,
        *,
        action: str,
        **extra,
    ) -> None:
        self.logger.info(
            message,
            extra={
                "service": self.service,
                "action": action,
                **extra,
            },
        )

    def warning(
        self,
        message: str,
        *,
        action: str,
        **extra,
    ) -> None:
        self.logger.warning(
            message,
            extra={
                "service": self.service,
                "action": action,
                **extra,
            },
        )

    def error(
        self,
        message: str,
        *,
        action: str,
        **extra,
    ) -> None:
        self.logger.error(
            message,
            extra={
                "service": self.service,
                "action": action,
                **extra,
            },
        )

    def exception(
        self,
        message: str,
        *,
        action: str,
        **extra,
    ) -> None:
        self.logger.exception(
            message,
            extra={
                "service": self.service,
                "action": action,
                **extra,
            },
        )
