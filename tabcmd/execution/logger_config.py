import logging
import logging.handlers
import os
import sys

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


def _below_warning(record: logging.LogRecord) -> bool:
    return record.levelno < logging.WARNING


def add_trace_level():
    trace_level: int = logging.DEBUG - 5
    add_log_level("TRACE", trace_level)
    FORMATS[trace_level] = FORMATS[logging.ERROR]


def configure_log(name: str, logging_level_input: str):
    """function for logging statements to console and logfile"""
    logging_level = getattr(logging, logging_level_input.upper())
    log_format = FORMATS[logging_level]
    if logging_level is not logging.INFO:
        FORMATS[logging.INFO] = "%(filename)-10s: %(message)-30s"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)

    # Only add handlers once to avoid duplicates on repeated configure_log calls
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) for h in root_logger.handlers):
        file_handler = logging.handlers.RotatingFileHandler("tabcmd.log", maxBytes=1_000_000, backupCount=5)
        file_handler.setLevel(logging_level)
        file_handler.setFormatter(logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S"))
        root_logger.addHandler(file_handler)

    named_logger = logging.getLogger(name)
    if not any(
        isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler) for h in named_logger.handlers
    ):
        # INFO and below → stdout so PowerShell doesn't treat normal output as errors.
        # WARNING and above → stderr so real errors are still distinguishable.
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging_level)
        stdout_handler.addFilter(_below_warning)
        stdout_handler.setFormatter(logging.Formatter(log_format))
        named_logger.addHandler(stdout_handler)

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(logging.Formatter(FORMATS[logging.ERROR]))
        named_logger.addHandler(stderr_handler)

    return named_logger


def log(file_name, logging_level):
    logger = configure_log(file_name, logging_level)
    if not hasattr(logger, "trace"):
        logger.trace = logger.debug
    return logger
