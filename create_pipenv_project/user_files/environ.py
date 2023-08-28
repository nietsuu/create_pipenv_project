import os

try:
    PYTHONDEVMODE = bool(int(os.environ["PYTHONDEVMODE"]))
except KeyError:
    PYTHONDEVMODE = True

try:
    LOGGING_LEVEL = os.environ["LOGGING_LEVEL"]
except KeyError:
    LOGGING_LEVEL = "DEBUG"
