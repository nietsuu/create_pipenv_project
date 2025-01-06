from PACKAGE_NAME.logging import get_logger
from PACKAGE_NAME.environ import PRODUCTION

logger = get_logger("PACKAGE_NAME")


async def main() -> None:
    logger.debug(f"{PRODUCTION=}")


async def shutdown() -> None:
    logger.debug("Shutdown")
