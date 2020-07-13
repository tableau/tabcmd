import logging

def get_logger(name):
    """function for logging statements to console and logfile"""
    log_format = '%(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        filename='test.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
