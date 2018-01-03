import requests
import utils
import logging.config
import os
import django
import random
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
django.setup()
# This file store private setting in the current directory. For this project, it is api key.
from settings import *
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
            'stream': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['stream'],
                'level': 'INFO'
            }
        }

    },
}

T_API = 'https://api.tumblr.com/v2/'

logging.config.dictConfig(LOGGING['logging'])
logger = logging.getLogger(__name__)


def main():
    active_tags = Tag.objects.filter(active=True)
    if not active_tags:
        logger.warning("Can't find any active tag")
    else:
        tag = random.choice(active_tags).tag
        print(tag)
        unix_time = Post.objects.filter(tagged__tag=tag)
        if unix_time:
            pass
        else:
            start_time = datetime.datetime.timestamp()


    # tagged_url = "{}tagged"
    # params = {
    #     # 'key': key,
    #
    # }
    #TODO select random (get old posts, get new posts)
    #TODO randome site for cheking
    #TODO add posts/tags/content to database

    # client = pytumblr.TumblrRestClient(
    #     consumer_key=key
    # )
    # print(client.tagged("anime_gif"))


main()