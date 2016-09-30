import logging
import logging.handlers


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s %(asctime)s - %(levelname)s - %(message)s')
    syslogHandler = logging.handlers.SysLogHandler(address='/dev/log')
    syslogHandler.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    logger.addHandler(syslogHandler)
    return logger
