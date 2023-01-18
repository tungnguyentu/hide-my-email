import logging
import uuid

LOGGING_VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


from contextvars import ContextVar

correlation_id: ContextVar[float] = ContextVar(
  'correlation_id', default=uuid.uuid4().hex
)


class ContextFilter(logging.Filter):
    """"Provides correlation id parameter for the logger"""

    def filter(self, record):
        record.correlation_id = correlation_id.get()
        return True


def setup_app_level_logger(name: str, level: str = "INFO") -> logging.Logger:
    if level not in LOGGING_VALID_LEVELS:
        raise ValueError(f"'{level}' is not a valid logging level. Valid levels: {LOGGING_VALID_LEVELS}")
    level = logging.getLevelName(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        (
            "%(asctime)s"
            " - %(process)s"
            " - %(threadName)s"
            " - %(name)s"
            " - %(funcName)s:%(lineno)s"
            " - %(levelname)s"
            " - %(message)s"
        )
    )
    # ISO8061 FORMAT
    formatter.default_time_format = "%Y-%m-%dT%H:%M:%S"
    # SHOW NANOSECONDS 1 milisecond = 1^6 nanoseconds
    formatter.default_msec_format = "%s,%.6f"

    # LOG RECORDS WILL BE DELIVERD VIA STDERR STREAM
    # PROCCES MANAGERS LIKE SUPERVISOR OR K8S WILL PUSH THE OUTPUT FROM STDERR TO OTHER POSITIONS
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    logger.addFilter(ContextFilter())
    logger.addHandler(stream_handler)
    return logger
