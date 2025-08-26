"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from aimlpy.setting import Settings

"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/11/2024
"""
import logging
import sys


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.ERROR:
            record.msg = f"\033[31m{record.msg}\033[0m"
        return super().format(record)


def setup_logging():
    level = getattr(logging, Settings.LOG_LEVEL.upper(), logging.INFO)
    formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('service.log')
    file_handler.setFormatter(formatter)

    handlers = [
        stream_handler,
        file_handler
    ]

    logging.basicConfig(level=level, handlers=handlers)
    logging.getLogger('ib_async.client').setLevel(logging.ERROR)
    logging.getLogger('ib_async.wrapper').setLevel(logging.ERROR)
    logging.getLogger('pyngrok.process').setLevel(logging.ERROR)
    logging.getLogger('pyngrok.ngrok').setLevel(logging.ERROR)


setup_logging()


def get_logger(name: str):
    return logging.getLogger(name)
