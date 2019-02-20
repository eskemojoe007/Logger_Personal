import logging.config
import os
import yaml
import colored_logger
from my_module import MyModule

# Initialize colors (important for windows)
colored_logger.init()

# Read in the yaml to a dictionary
with open(os.path.join('example_usage', 'logging.yaml'), 'rt') as f:
    CONFIG = yaml.safe_load(f.read())

# Set up the names
logging.config.dictConfig(CONFIG)

# Set the logger
logger = logging.getLogger(__name__)

def main():
    # pylint: disable=C0301
    logger.info(
        'cool coolcool cool cool cool cool cool cool Cool cool cool cool cool cool cool cool cool cool cool cool cool cool cool cool cool cool')
    logger.debug('main - debug')
    logger.info('main - info')
    logger.warning('main - warning')
    logger.error('main - error')
    logger.critical('main - critical')
    MyModule()


if __name__ == '__main__':
    main()
