import os
import sys
import asyncio
import logging
import threading
import concurrent.futures
from types import TracebackType
from typing import Any, Type, TypeVar, Optional, Callable, Coroutine
from PACKAGE_NAME.logging import get_logger

T = TypeVar("T")


def excepthook(
    exc_type: Type[BaseException],
    exc_value: Optional[BaseException],
    exc_traceback: Optional[TracebackType],
) -> None:
    logger_name = "Global Exception Handler"

    try:
        get_logger(logger_name).critical(repr(exc_value), exc_info=exc_value)
    except Exception:
        logging.getLogger(logger_name).warning(
            f"'{logger_name}' failed. Fallback to 'sys.__excepthook__'."
        )
        sys.__excepthook__(exc_type, exc_value or exc_type(None), exc_traceback)


def asyncio_exception_handler(
    loop: asyncio.AbstractEventLoop,
    context: dict[str, Any],
) -> None:
    exception = context.get("exception")

    if exception is None:
        get_logger("Global Asynchronous Exception Handler").warning(context)
    else:
        excepthook(type(exception), exception, None)


def main_wrapper(
    main: Callable[[asyncio.AbstractEventLoop], Coroutine[Any, Any, int]]
) -> int:
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

        return runner.run(main(loop))


async def _async_wrapper(coro: Coroutine[Any, Any, T]) -> T | Exception:
    try:
        return await coro
    except Exception as error:
        get_logger(coro.__name__).exception(error)
        return error


def run_coro(coro: Coroutine[Any, Any, T]) -> asyncio.Task[T | Exception]:
    return asyncio.create_task(_async_wrapper(coro), name=coro.__name__)


def run_coro_threadsafe(
    coro: Coroutine[Any, Any, T],
    loop: asyncio.AbstractEventLoop,
) -> concurrent.futures.Future[T | Exception]:
    return asyncio.run_coroutine_threadsafe(_async_wrapper(coro), loop)
