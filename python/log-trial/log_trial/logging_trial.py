import logging
from colorama import init as colorama_init
from colorama import Fore, Style
from typing import Optional

colorama_init()


class StreamCustomFormatter(logging.Formatter):
    """Custom Formatter for colored terminal output.

    Ref: https://stackoverflow.com/a/56944256/6323360
    """

    def __init__(self, fmt: str = ""):
        super().__init__(fmt=fmt)

        self._fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        if fmt.strip():
            self._fmt = fmt
        self._fmt = self.stylize_fmt_string("%(asctime)s", Style.DIM)

        self._FORMATS = {
            logging.DEBUG: self.stylize_fmt_string("%(levelname)s", Fore.WHITE),
            logging.INFO: self.stylize_fmt_string("%(levelname)s", Fore.GREEN),
            logging.WARNING: self.stylize_fmt_string("%(levelname)s", Fore.YELLOW),
            logging.ERROR: self.stylize_fmt_string("%(levelname)s", Fore.RED),
            logging.CRITICAL: self.stylize_fmt_string(
                "%(levelname)s", Fore.RED + Style.BRIGHT
            ),
        }

    def format(self, record) -> logging.LogRecord:
        log_fmt = self._FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    def stylize_fmt_string(self, str_to_color: str, color: int) -> str:
        return self._fmt.replace(str_to_color, color + str_to_color + Style.RESET_ALL)


def init_logger(name: Optional[str] = None) -> logging.Logger:
    # Ref: https://www.machinelearningplus.com/python/python-logging-guide/
    # Gets or create a logger
    logger = logging.getLogger(name)

    # Set log level
    # Ref: https://docs.python.org/3/library/logging.html#logging-levels
    # From highest to lowest
    # CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    logger.setLevel(logging.INFO)

    log_format_str = (
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s (%(filename)s:%(lineno)d)"
    )

    # Setup formatter
    formatter = logging.Formatter(fmt=log_format_str)

    # Add file handler
    if name is None:
        name = "root"
    file_handler = logging.FileHandler("logs/" + name + ".log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Add terminal handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StreamCustomFormatter(fmt=log_format_str))
    logger.addHandler(console_handler)

    return logger


def sample_logging(logger: logging.Logger):
    # Add messages now!
    logger.debug("A debug message")
    logger.info("An info message")
    logger.warning("Something is not right.")
    logger.error("A Major error has happened.")
    logger.critical("Fatal error. Cannot continue")
