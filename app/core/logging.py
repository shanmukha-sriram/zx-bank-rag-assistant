import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=level, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", stream=sys.stdout)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)