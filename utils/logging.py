"""Logging utilites for the bot"""

import logging
import sys
from logging.handlers import TimedRotatingFileHandler


def logging_setup() -> logging.Logger:
    """Sets up logging for the bot

    Returns:
        Logger: Root logger
    """
    log_formatter = logging.Formatter(
        '[{asctime}] [{levelname:<8}] {name}: {message}', style='{')

    root = logging.getLogger('discord')

    logging.getLogger('discord.http')

    console_handler: logging.StreamHandler = logging.StreamHandler()

    console_handler.setFormatter(log_formatter)

    file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(filename='./logs/discord.log', when='h', interval=1)

    file_handler.setFormatter(log_formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    root.setLevel(logging.INFO)

    root.log(logging.INFO, '### Starting Bot ###')

    sys.excepthook = root

    return root
