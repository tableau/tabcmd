import logging
import os
path = os.path.dirname(os.path.abspath(__file__))
def get_logger(name, logging_level):
    """function for logging statements to console and logfile"""
    logging_level = getattr(logging, logging_level.upper())
    log_format = '%(message)s'
    logging.basicConfig(level=logging_level,
                        format=log_format,
                        filename= path+"'\'test.log",
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging_level)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
