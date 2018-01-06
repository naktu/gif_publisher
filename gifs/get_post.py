import pytumblr
import logging.config
import os
import django
import random
import datetime
import sys


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

T_API = 'https://api.tumblr.com/v2/'
T_PATH = 'tagged'

logging.config.dictConfig(LOGGING['logging'])
logger = logging.getLogger(__name__)


def parse_response(resp):
    if type(resp) is dict:
        return {
            'status': 'fail',
            'data': resp
        }
    elif type(resp) is list:
        result = []
        for post in resp:
            data = {}
            raw_post = post
            if post.pop('type', None) == 'photo':
                data['tumblr_post_id'] = post.pop('id', None)
                data['timestamp'] = post.pop('timestamp', None)
                data['tags'] = post.pop('tags', None)
                photos = post.pop('photos', None)
                if photos:
                    data['gif_links'] = [image['original_size']['url'] for image in photos if image['original_size']['url'].endswith('.gif') ]
                else:
                    data['gif_links'] = None
                for key in data:
                    if data[key] is None:
                        logger.error('Some post data is empty: {}'.format(data))
                        logger.info('RAW Data: {}'.format(raw_post))
                data['json'] = post
                if data['gif_links']: result.append(data)
        return {
            'result': 'ok',
            'data': result
        }
    else:
        return {
            'result': 'fail',
            'data': "Response not list or dict: {}".format(resp)
        }


def main():
    client = pytumblr.TumblrRestClient(consumer_key=django.conf.settings.KEY)
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
            sys.exit(1)
        for_db = parse_response(resp)
        if for_db['result'] == 'ok':
            for row in for_db['data']:
                post = Post(
                    tumblr_post_id=row['tumblr_post_id'],
                    timestamp=row['timestamp'],
                    json=row['json']
                )
                post.save()

                tags = []
                for tag in row['tags']:
                    new_tag = Tag(tag=tag)
                    new_tag.save()
                    tags.append(new_tag)
        else:
            pass




main()
