from loguru import logger


async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all
    exceptions within task factory tasks.
    :param update:
    :param exception:
    :return:
    """

    logger.exception(exception)
    logger.debug(update)

    return True
