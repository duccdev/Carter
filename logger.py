import colors
import config
from datetime import datetime
from logging import Handler, LogRecord, DEBUG, INFO, WARNING, ERROR, CRITICAL

debug = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.BLUE}{colors.BOLD}DEBUG   {colors.END} {msg}"
)
info = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.BLUE}{colors.BOLD}INFO    {colors.END} {msg}"
)
warn = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.YELLOW}{colors.BOLD}WARN    {colors.END} {msg}"
)
error = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.RED}{colors.BOLD}ERROR   {colors.END} {msg}"
)
critical = lambda msg: print(
    f"{config.LOG_PREFIX} {colors.BOLD}{datetime.now().strftime('%H:%M:%S')}{colors.END} {colors.BLUE}{colors.BOLD}CRITICAL{colors.END} {msg}"
)


class LoggingHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        if record.levelno == INFO:
            info(
                f"{colors.LIGHT_PURPLE}{record.name}{colors.END}: {record.getMessage()}"
            )
