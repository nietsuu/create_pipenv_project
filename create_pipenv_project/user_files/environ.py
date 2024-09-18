import os
from typing import cast, Callable, TypeVar

T = TypeVar("T")


def env(t: Callable[[str], T], key: str) -> T:
    try:
        value = os.environ[key]
    except KeyError:
        print(
            f"Required environment variable '{key}' of "
            f"type '{t.__name__}' is missing."
        )
        exit(1)

    if t is bool:
        value = value.lower().strip()

        for i in ("0", "false", "f", "no", "n"):
            if value == i:
                return cast(T, False)

        return cast(T, True)

    return t(value)


PRODUCTION: str | None = os.getenv("PRODUCTION")
DEFAULT_LOGGING_LEVEL: str = env(str, "DEFAULT_LOGGING_LEVEL")
DEFAULT_FILE_LOGGING: bool = env(bool, "DEFAULT_FILE_LOGGING")
