import time
import logging
import inspect
from contextlib import contextmanager
from typing import Optional, Union, Iterator, Dict, Any
from PROJECT_NAME.environ import DEFAULT_LOGGING_LEVEL, DEFAULT_FILE_LOGGING


class MeasureTime:
    @staticmethod
    @contextmanager
    def wall_clock(
        logger_name: Union[str, logging.Logger],
        block_name: Optional[str] = None,
    ) -> Iterator[Dict[str, float | None]]:
        if isinstance(logger_name, logging.Logger):
            logger = logger_name
        else:
            logger = get_logger(logger_name)

        msg = block_name or logger.name
        logger.debug(f"Measuring wall clock time of {msg}...")

        start_time = time.time()
        res: Dict[str, float | None] = {
            "start_time": start_time,
            "end_time": None,
            "delta": None,
        }
        yield res

        end_time = time.time()
        delta = end_time - start_time

        res["end_time"] = end_time
        res["delta"] = delta

        logger.debug(f"Wall clock time of {msg}: {round(delta, 2)}s")

    @staticmethod
    @contextmanager
    def cpu(
        logger_name: Union[str, logging.Logger],
        block_name: Optional[str] = None,
    ) -> Iterator[Dict[str, float | None]]:
        if isinstance(logger_name, logging.Logger):
            logger = logger_name
        else:
            logger = get_logger(logger_name)

        msg = block_name or logger.name
        logger.debug(f"Measuring CPU time of {msg}...")

        start_time = time.perf_counter()
        res: Dict[str, float | None] = {
            "start_time": start_time,
            "end_time": None,
            "delta": None,
        }
        yield res

        end_time = time.perf_counter()
        delta = end_time - start_time

        res["end_time"] = end_time
        res["delta"] = delta

        logger.debug(f"CPU time of {msg}: {round(delta, 2)}s")


class _Formatter(logging.Formatter):
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


_stream_formatter = _Formatter()
_file_formatter = _Formatter(colored=False)


def get_logger(
    name: str,
    *,
    level: str = DEFAULT_LOGGING_LEVEL,
    file_logging: bool = DEFAULT_FILE_LOGGING,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(_stream_formatter)
        logger.addHandler(stream_handler)

        if file_logging:
            file_handler = logging.FileHandler("logs.txt")
            file_handler.setFormatter(_file_formatter)
            logger.addHandler(file_handler)

    for handler in logger.handlers:
        handler.setLevel(level)

    return logger


def trace(msg: Any = None) -> None:
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    logger = get_logger(f"Trace {caller.filename}")

    if msg is None:
        logger.debug(f"Line {caller.lineno}")
    else:
        logger.debug(f"Line {caller.lineno}: {msg}")
