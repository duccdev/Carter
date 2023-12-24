import colors
import config
from datetime import datetime

info = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.BLUE}{colors.BOLD}INFO {colors.END} {msg}"
)
error = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.RED}{colors.BOLD}ERROR{colors.END} {msg}"
)
warn = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.YELLOW}{colors.BOLD}WARN {colors.END} {msg}"
)
