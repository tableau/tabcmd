import logging
import os

path = os.path.dirname(os.path.abspath(__file__))


def get_logger(name, logging_level):
    """function for logging statements to console and logfile"""
    logging_level = getattr(logging, logging_level.upper())
    # TODO: in INFO level, we should leave out the (name) field
    log_format = '%(levelname)s %(name)s  %(message)s'
    logging.basicConfig(level=logging_level,
                        format=log_format,
                        filename="test.log",
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging_level)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def log(file_name, logging_level):
    logger = get_logger(file_name, logging_level)
    return logger
