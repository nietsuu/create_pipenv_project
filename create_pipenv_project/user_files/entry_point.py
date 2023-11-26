import os
import sys
import asyncio
import logging
import threading
from types import TracebackType
from typing import Any, Dict, Type, Optional
from PROJECT_NAME import main as async_main
from PROJECT_NAME.logging import get_logger


def excepthook(
    exc_type: Type[BaseException],
    exc_value: Optional[BaseException],
    exc_traceback: Optional[TracebackType],
) -> None:
    logger_name = "Global Exception Handler"

    try:
        get_logger(logger_name).critical(
            repr(exc_value), exc_info=exc_value, stack_info=True
        )
    except Exception:
        logging.getLogger(logger_name).warning(
            f"'{logger_name}' failed. Fallback to 'sys.__excepthook__'."
        )
        sys.__excepthook__(exc_type, exc_value or exc_type(None), exc_traceback)


def asyncio_exception_handler(
    loop: asyncio.AbstractEventLoop,
    context: Dict[str, Any],
) -> None:
    exception = context.get("exception")

    if exception is None:
        get_logger("Global Asynchronous Exception Handler").warning(context)
    else:
        excepthook(type(exception), exception, None)


def main() -> int:
    if os.name == "nt":
        loop_factory = None
    else:
        import uvloop

        loop_factory = uvloop.new_event_loop

    with asyncio.Runner(loop_factory=loop_factory) as runner:
        loop = runner.get_loop()

        loop.set_exception_handler(asyncio_exception_handler)
        sys.excepthook = excepthook
        threading.excepthook = lambda args: excepthook(
            args.exc_type,
            args.exc_value,
            args.exc_traceback,
        )

        return runner.run(async_main(loop))
