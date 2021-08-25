"""File to allow initialization of a logger that outputs to both files and terminal by default"""

import logging
from typing import Optional
import re
import os
import enum

import colorama
from colorama import Fore, Style


colorama.init()

_LOGS_FOLDER = "logs"
_LOG_FORMAT_STR_STREAM = "[%(asctime)s] [%(levelname)-10s] [%(filename)s:%(lineno)d] >>> %(message)s "
_LOG_FORMAT_STR_FILE = _LOG_FORMAT_STR_STREAM + " [Logger Name: %(name)s]"
_DATE_FMT_STR = "%Y-%m-%dT%H:%M:%S"


class LoggerType(enum.Enum):
    """Enum for logger type"""

    BOTH = 0
    TERMINAL = 1
    FILE = 2


def init_logger(name: Optional[str] = None, logger_type: Optional[LoggerType] = LoggerType.BOTH) -> logging.Logger:
    """Initialize and return a logger that can be used via `logger.debug(), logger.warn()`, etc.

    Args:
        name (Optional[str], optional): The name of the logger. If `None`, use the root logger. \
Defaults to `None`, e.g. the root name will be used.
        logger_type: Optional[LoggerType]: The type of handler you want to the handler to output. \
Defaults to both file and terminal handlers.

    Returns:
        logging.Logger: The Logger object that can be used to call logging functions on.
    """
    # Ref: https://www.machinelearningplus.com/python/python-logging-guide/
    # Gets or create a logger
    logger = logging.getLogger(name)

    # Set default log level. Each handler will then decide which level it will handle
    # Ref: https://docs.python.org/3/library/logging.html#logging-levels
    # From highest to lowest
    # CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    logger.setLevel(logging.DEBUG)

    # Setup formatter
    formatter = logging.Formatter(fmt=_LOG_FORMAT_STR_FILE, datefmt=_DATE_FMT_STR)

    # Add default `root` file handler
    if name is None:
        name = "root"

    _add_handlers_according_to_logger_type(name, formatter, logger, logger_type)

    return logger


def _add_handlers_according_to_logger_type(
    name: str, formatter: logging.Formatter, logger: logging.Logger, logger_type: LoggerType
):
    """Add handlers according to logger type. Will default to both file and terminal handlers"""
    # Add handlers accordingly
    if logger_type == LoggerType.BOTH:
        _add_file_handler(name, formatter, logger)
        _add_terminal_handler(logger)
    elif logger_type == LoggerType.TERMINAL:
        _add_terminal_handler(logger)
    elif logger_type == LoggerType.FILE:
        _add_file_handler(name, formatter, logger)
    else:
        # Add both by default
        _add_file_handler(name, formatter, logger)
        _add_terminal_handler(logger)


def _add_file_handler(name: str, formatter: logging.Formatter, logger: logging.Logger):
    """Add file handler for logs"""
    if not os.path.exists(_LOGS_FOLDER):
        os.mkdir(_LOGS_FOLDER)
    file_handler = logging.FileHandler("logs/" + name + ".log")
    file_handler.setFormatter(formatter)
    # For files, we probably want to log all levels
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)


def _add_terminal_handler(logger: logging.Logger):
    """Add terminal handler for logs"""
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StreamCustomFormatter(fmt=_LOG_FORMAT_STR_STREAM, datefmt=_DATE_FMT_STR))
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)


class StreamCustomFormatter(logging.Formatter):
    """Custom Formatter for colored terminal output.

    Ref: https://stackoverflow.com/a/56944256/6323360
    """

    def __init__(self, fmt: str = "", datefmt: Optional[str] = ""):
        super().__init__(fmt=fmt, datefmt=datefmt)

        self._fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        if fmt.strip():
            self._fmt = fmt
        self._fmt = self._stylize_fmt_string("%(asctime)s", Style.DIM)
        self._datefmt = datefmt

        self._format_styles = {
            logging.DEBUG: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.WHITE),
            logging.INFO: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.GREEN),
            logging.WARNING: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.YELLOW),
            logging.ERROR: self._stylize_fmt_string_regex(r"%\(levelname\)\S*s", Fore.RED),
            logging.CRITICAL: self._stylize_fmt_string_regex(r"%\(levelname\)\S+s", Fore.RED + Style.BRIGHT),
        }

    def format(self, record) -> logging.LogRecord:
        log_fmt = self._format_styles.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt=self._datefmt)
        return formatter.format(record)

    def _stylize_fmt_string(self, str_to_replace: str, color: int) -> str:
        return self._fmt.replace(str_to_replace, color + str_to_replace + Style.RESET_ALL)

    def _stylize_fmt_string_regex(self, regex_to_color: str, color: int) -> str:
        matched = re.search(regex_to_color, self._fmt)
        str_to_color = matched.group(0)
        return self._fmt.replace(str_to_color, color + str_to_color + Style.RESET_ALL)


def sample_logging(logger: logging.Logger):
    """Sample function on how logging works"""
    # Add messages now!
    logger.debug("A debug message")
    logger.info("An info message")
    logger.warning("Something is not right.")
    logger.error("A Major error has happened.")
    logger.critical("Fatal error. Cannot continue")
