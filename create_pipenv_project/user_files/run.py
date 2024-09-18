import sys
from PACKAGE_NAME import main
from PACKAGE_NAME.entry_point import main_wrapper

try:
    sys.exit(main_wrapper(main))
except KeyboardInterrupt:
    sys.exit(0)
