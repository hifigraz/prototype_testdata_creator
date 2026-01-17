import logging

logging.basicConfig(
    format="%(ascttime)s %(level)s %(message)s", encoding="utf-8", level=logging.DEBUG
)


def get_logger(name: str = __name__, debug: bool = False):
    logger = logging.getLogger(name)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger
