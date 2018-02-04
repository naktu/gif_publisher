import logging.config
import os
import django
import string
import random
import datetime
import sys
import time
import requests


prj_path = '/home/tutunak/Dropbox/prj/web/gif_publisher'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
sys.path.append(prj_path)
os.chdir(prj_path)
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
                'filename': 'gifs_download.log'
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
RETRY_LINK = 3
MAX_LINKS_ERROR = 3



logging.config.dictConfig(LOGGING['logging'])
logger = logging.getLogger(__name__)

def main():
    exclude = []
    tags_to_publish = Tag.objects.filter(tag_to_publish__isnull=False)
    gif_set = Gif.objects.filter(choices=1).filter(tagged__in=tags_to_publish).exclude(file__isnull=False)[:10]
    for gif in gif_set:
        n = RETRY_LI
        n = 3
        while n:
            try:
                r = requests.get(gif.link)
            except:
                logger.error('Error when try get url {0} : {1}'.format(gif.link, sys.exc_info()))
                n -= 1
                continue

            if not r:
                logger.error('Not 200 code {}'.format(r.status_code))
                n -= 1
                continue

            if r.content.endswith(b'\x00;'):





if __name__ == '__main__':
    main()

