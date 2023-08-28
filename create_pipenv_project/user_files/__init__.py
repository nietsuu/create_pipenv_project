import asyncio
from {% PROJECT_NAME %}.logging import get_logger, trace, MeasureTime


async def main(loop: asyncio.AbstractEventLoop) -> int:
    logger = get_logger("main")

    trace()

    with MeasureTime.cpu(logger, "main"):
        logger.info("Hello world!!")

    return 0
