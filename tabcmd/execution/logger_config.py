import logging
import os

path = os.path.dirname(os.path.abspath(__file__))

FORMATS = {
    logging.ERROR: "ERROR: %(message)s",
    logging.WARN:  "WARN:  %(message)s",
    logging.DEBUG: "DEBUG: %(name)-10s: %(lineno)d: %(message)-10s",
    logging.INFO:  "%(message)s",
    "TRACE":       "TRACE: %(asctime)-12s %(name)-10s: %(lineno)d: %(message)-10s",
    "DEFAULT":     "%(message)s",
}


def configure_log(name: str, logging_level_input: str):
    """function for logging statements to console and logfile"""
    logging_level = getattr(logging, logging_level_input.upper())
    log_format = FORMATS[logging_level]
    logging.basicConfig(
        level=logging_level, format=log_format, filename="tabcmd.log", filemode="a", datefmt="%Y-%m" "-%d " "%H:%M:%S"
    )
    console = logging.StreamHandler()
    console.setLevel(logging_level)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def log(file_name, logging_level):
    logger = configure_log(file_name, logging_level)
    return logger
