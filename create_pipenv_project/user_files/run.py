import os
import sys
import asyncio
import threading
from types import TracebackType
from typing import Any, Callable, Coroutine, Optional, Dict, Type


def excepthook(
    exc_type: Type[BaseException],
    exc_value: Optional[BaseException],
    exc_traceback: Optional[TracebackType],
) -> None:
    try:
        excepthook_logger.critical(repr(exc_value), exc_info=exc_value, stack_info=True)
    except Exception:
        sys.__excepthook__(exc_type, exc_value or exc_type(None), exc_traceback)


def asyncio_exception_handler(
    loop: asyncio.AbstractEventLoop,
    context: Dict[str, Any],
) -> None:
    exception = context.get("exception")

    if exception is None:
        asyncio_exception_handler_logger.warning(context)
    else:
        excepthook(type(exception), exception, None)


def set_error_handlers(*, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
    sys.excepthook = excepthook
    threading.excepthook = lambda args: excepthook(
        args.exc_type,
        args.exc_value,
        args.exc_traceback,
    )

    if loop is not None:
        loop.set_exception_handler(asyncio_exception_handler)


def async_runner(
    main_function: Callable[[asyncio.AbstractEventLoop], Coroutine[Any, Any, int]]
) -> int:
    if os.name == "nt":
        loop_factory = None
    else:
        import uvloop

        loop_factory = uvloop.new_event_loop

    with asyncio.Runner(loop_factory=loop_factory) as runner:
        loop = runner.get_loop()
        set_error_handlers(loop=loop)
        return runner.run(main_function(loop))


def sync_runner(main_function: Callable[[], int]) -> int:
    set_error_handlers()
    return main_function()


if __name__ == "__main__":
    excepthook_logger = get_logger("excepthook")
    asyncio_exception_handler_logger = get_logger("asyncio_exception_handler")
    sys.exit(
        async_runner(main) if asyncio.iscoroutinefunction(main) else sync_runner(main)
    )
