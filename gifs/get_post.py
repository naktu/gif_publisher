import pytumblr
import utils
import logging.config
import os
import django
import random
import datetime


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

T_API  = 'https://api.tumblr.com/v2/'
T_PATH = 'tagged'

logging.config.dictConfig(LOGGING['logging'])
logger = logging.getLogger(__name__)


def main():
    client = pytumblr.TumblrRestClient(consumer_key=django.conf.settings.KEY)
    client = pytumblr.TumblrRestClient(consumer_key='123')
    active_tags = Tag.objects.filter(active=True)
    if not active_tags:
        logger.warning("Can't find any active tag")
    else:
        tag = random.choice(active_tags).tag
        posts = Post.objects.filter(tagged__tag=tag)
        if posts:
            timestamp = posts.order_by('timestamp').first().timestamp
            logger.info('Timestamp for tag {0} = {1}'.format(tag, timestamp))
        else:
            timestamp = round(datetime.datetime.utcnow().timestamp())
            logger.info("Can't find any timestamp for tag {0}, take current timestamp {1}".format(tag, timestamp))

        try:
            resp = client.tagged(tag, before=timestamp)
        except Exception as e:
            logger.error('{}'.format(e))
        else:
            print(len(resp))
            print(type(resp))
            print(resp)
            for i in resp:
                print(i)

main()