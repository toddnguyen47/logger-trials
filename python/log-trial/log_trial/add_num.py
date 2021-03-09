import logging_trial

_logger = logging_trial.init_logger(__name__)


def add_two(num1: int, num2: int) -> int:
    sum1 = num1 + num2
    _logger.debug(num1)
    _logger.info(num2)
    _logger.warning("{}, {}".format(num1, num2))
    _logger.error(sum1)
    _logger.critical("Fatal error. Cannot continue")
    return sum1
