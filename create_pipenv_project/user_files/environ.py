import os
from typing import cast, Callable, TypeVar

T = TypeVar("T")


def env(t: Callable[[str], T], key: str) -> T:
    value = os.environ[key]

    if t is bool:
        value = value.lower().strip()

        for i in ("0", "false", "f", "no", "n"):
            if value == i:
                return cast(T, False)

        return cast(T, True)

    return t(value)


LOGGING_LEVEL: str = env(str, "LOGGING_LEVEL")
FILE_LOGGING: bool = env(bool, "FILE_LOGGING")
