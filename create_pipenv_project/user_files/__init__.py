import asyncio


async def async_main(loop: asyncio.AbstractEventLoop) -> int:
    get_logger("main").info("Hello world!!")
    return 0


def main() -> int:
    return async_main_runner(async_main)
