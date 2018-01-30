import logging.config
import os
import django
import string
import random
import datetime
import sys
import time
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
django.setup()

from gifs.models import *

LOGGING = {
    'logging': {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(module)s  %(message)s'
            }
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'gifs.logger.log'
            },
            'stream': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },

        },
        'loggers': {
            '': {
                'handlers': ['stream', 'file'],
                'level': 'INFO'
            }
        }

    },
}

PATH = '/media/hdd1/images/gif_publisher'



logging.config.dictConfig(LOGGING['logging'])
logger = logging.getLogger(__name__)


