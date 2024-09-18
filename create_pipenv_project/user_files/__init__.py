import asyncio
from PACKAGE_NAME.environ import PRODUCTION
from PACKAGE_NAME.logging import get_logger


async def main(loop: asyncio.AbstractEventLoop) -> int:
    logger = get_logger("main")

    logger.debug(f"{PRODUCTION=}")

    return 0
