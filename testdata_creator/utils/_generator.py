from .. import config

logger = config.get_logger(__name__, True)


def generator_main():
    logger.debug("Hello")
