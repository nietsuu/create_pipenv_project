import asyncio
from {% PROJECT_NAME %}._main_runner import async_main_runner
from {% PROJECT_NAME %}.logging import get_logger, trace, MeasureTime


async def async_main(loop: asyncio.AbstractEventLoop) -> int:
    logger = get_logger("main")

    trace()

    with MeasureTime.cpu(logger, "main"):
        logger.info("Hello world!!")

    return 0


def main() -> int:
    return async_main_runner(async_main)
