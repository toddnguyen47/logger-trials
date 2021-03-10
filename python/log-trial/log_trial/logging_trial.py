import logging
from colorama import init as colorama_init
from colorama import Fore, Style
from typing import Optional
import re

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
        self._fmt = self._stylize_fmt_string("%(asctime)s", Style.DIM)

        self._FORMATS = {
            logging.DEBUG: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.WHITE),
            logging.INFO: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.GREEN),
            logging.WARNING: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.YELLOW),
            logging.ERROR: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.RED),
            logging.CRITICAL: self._stylize_fmt_string_regex(
                r"%\(levelname\)\S+s", Fore.RED + Style.BRIGHT
            ),
        }

    def format(self, record) -> logging.LogRecord:
        log_fmt = self._FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    def _stylize_fmt_string(self, str_to_replace: str, color: int) -> str:
        return self._fmt.replace(str_to_replace, color + str_to_replace + Style.RESET_ALL)

    def _stylize_fmt_string_regex(self, regex_to_color: str, color: int) -> str:
        matched = re.search(regex_to_color, self._fmt)
        str_to_color = matched.group(0)
        return self._fmt.replace(str_to_color, color + str_to_color + Style.RESET_ALL)


def init_logger(name: Optional[str] = None) -> logging.Logger:
    """Initialize and return a logger that can be used via `logger.debug(), logger.warn()`, etc.

    Args:
        name (Optional[str], optional): The name of the logger. If `None`, use the root logger. \
Defaults to `None`.

    Returns:
        logging.Logger: The Logger object that can be used to call logging functions on.
    """
    # Ref: https://www.machinelearningplus.com/python/python-logging-guide/
    # Gets or create a logger
    logger = logging.getLogger(name)

    # Set log level
    # Ref: https://docs.python.org/3/library/logging.html#logging-levels
    # From highest to lowest
    # CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    logger.setLevel(logging.INFO)

    log_format_str = (
        "[%(asctime)s] [%(levelname)-10s] (%(message)s) "
        + "[Logger Name: %(name)s] [%(filename)s:%(lineno)d]"
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
