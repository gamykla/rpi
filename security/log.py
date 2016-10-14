import os

import logging.config


def init_logging():
    config_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "configuration")
    logging.config.fileConfig(
        os.path.join(config_directory, "logging.cfg"),
        disable_existing_loggers=False)
