import logging

DEBUG = True


def debug_print(message: str) -> None:
    if DEBUG:
        logging.debug(message)
