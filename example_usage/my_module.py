import logging
logger = logging.getLogger(__name__)

class MyModule:
    def __init__(self):
        logger.debug('MyModule - debug')
        logger.info('MyModule - info')
        logger.warning('MyModule - warning')
        logger.error('MyModule - error')
        logger.critical('MyModule - critical')
