import logging
import os

path = os.path.dirname(os.path.abspath(__file__))
PYTHON_INFO_LOGGING_LEVEL = 20


def get_logger(name, logging_level):
    """function for logging statements to console and logfile"""
    logging_level = getattr(logging, logging_level.upper())
    if logging_level == PYTHON_INFO_LOGGING_LEVEL:
        log_format = "%(message)s"
    else:
        log_format = "%(levelname)-5s %(asctime)-12s %(name)-10s  %(message)-10s"
    logging.basicConfig(
        level=logging_level, format=log_format, filename="tabcmd.log", filemode="a", datefmt="%Y-%m" "-%d " "%H:%M:%S"
    )
    console = logging.StreamHandler()
    console.setLevel(logging_level)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def log(file_name, logging_level):
    logger = get_logger(file_name, logging_level)
    return logger
