import logging

DEBUG = False


def debug_print(message: str) -> None:
    if DEBUG:
        logging.debug(message)
