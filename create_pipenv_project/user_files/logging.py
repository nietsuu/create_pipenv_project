import os
import time
import logging
from contextlib import contextmanager
from typing import Optional, Union, Iterator


def get_logger(
    name: str,
    *,
    level: Union[int, str] = os.getenv("DEFAULT_LOGGING_LEVEL") or logging.DEBUG,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler("logs.txt")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    for handler in logger.handlers:
        handler.setLevel(level)

    return logger


class Formatter(logging.Formatter):
    def __init__(self, *, colored: bool = True) -> None:
        self.colored = colored
        self.last_record: Optional[logging.LogRecord] = None

    def format(self, record: logging.LogRecord) -> str:
        space = " " * (len("CRITICAL") - len(record.levelname))

        if self.colored:
            formatter = logging.Formatter(
                "\n\033[91m%(name)s\033[0m\n"
                f"[\033[95m%(asctime)s\033[0m \033[93m%(levelname)s\033[0m{space}] %(message)s"
            )
        else:
            formatter = logging.Formatter(
                "\n%(name)s\n" f"[%(asctime)s %(levelname)s{space}] %(message)s"
            )

        if self.last_record is not None:
            if record.name == self.last_record.name:
                if self.colored:
                    formatter = logging.Formatter(
                        f"[\033[95m%(asctime)s\033[0m \033[93m%(levelname)s\033[0m{space}] %(message)s"
                    )
                else:
                    formatter = logging.Formatter(
                        f"[%(asctime)s %(levelname)s{space}] %(message)s"
                    )

        self.last_record = record
        return formatter.format(record)


stream_formatter = Formatter()
file_formatter = Formatter(colored=False)


@contextmanager
def debug_wall_time(
    logger_name: Union[str, logging.Logger],
    block_name: Optional[str] = None,
) -> Iterator[None]:
    if isinstance(logger_name, logging.Logger):
        logger = logger_name
    else:
        logger = get_logger(logger_name)

    msg = block_name or logger.name
    logger.debug(f"Measuring wall clock time of {msg}...")

    start_time = time.time()
    yield None

    logger.debug(f"Wall clock time of {msg}: {round(time.time() - start_time, 2)}s")


@contextmanager
def debug_cpu_time(
    logger_name: Union[str, logging.Logger],
    block_name: Optional[str] = None,
) -> Iterator[None]:
    if isinstance(logger_name, logging.Logger):
        logger = logger_name
    else:
        logger = get_logger(logger_name)

    msg = block_name or logger.name
    logger.debug(f"Measuring CPU time of {msg}...")

    start_time = time.process_time()
    yield None

    logger.debug(f"CPU time of {msg}: {round(time.process_time() - start_time, 2)}s")
