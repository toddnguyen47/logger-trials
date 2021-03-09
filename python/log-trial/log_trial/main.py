import logging_trial
import add_num

if __name__ == "__main__":
    logger = logging_trial.init_logger(__name__)
    logging_trial.sample_logging(logger)

    add_num.add_two(1, 2)
