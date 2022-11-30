import logging
import os

path = os.path.dirname(os.path.abspath(__file__))

FORMATS = {
    logging.ERROR: "%(asctime)s %(levelname)-5s:(%(name)-10s %(filename)-10s: %(lineno)d): %(message)-30s",
    logging.WARN: "%(asctime)s %(levelname)-5s: (%(name)-10s %(filename)-10s: %(lineno)d): %(message)-30s",
    logging.INFO: "%(message)-30s",
    logging.DEBUG: "%(asctime)s %(levelname)-5s: (%(name)-10s %(filename)-10s: %(lineno)d): %(message)-30s",
}

# https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
def add_log_level(level_name, level_num, method_name=None):
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError("{} already defined in logging module".format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError("{} already defined in logging module".format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError("{} already defined in logger class".format(method_name))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


def add_trace_level():
    trace_level: int = logging.DEBUG - 5
    add_log_level("TRACE", trace_level)
    FORMATS[trace_level] = FORMATS[logging.ERROR]


def configure_log(name: str, logging_level_input: str):
    """function for logging statements to console and logfile"""
    logging_level = getattr(logging, logging_level_input.upper())
    log_format = FORMATS[logging_level]
    if logging_level is not logging.INFO:
        print("error in the next line: str cannot be assigned or something?")
        log_format[logging.INFO] = "%(filename)-10s: %(message)-30s"

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
    if not hasattr(logger, "trace"):
        logger.trace = logger.debug
    return logger
