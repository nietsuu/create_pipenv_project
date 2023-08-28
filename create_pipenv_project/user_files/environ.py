import os

PYTHONDEVMODE: bool = bool(int(os.environ["PYTHONDEVMODE"]))
LOGGING_LEVEL: str = os.environ["LOGGING_LEVEL"]
