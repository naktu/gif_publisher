import logging.config
import os
import django
import sys
import time
import requests
import string
import datetime


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
MAX_RETRY_LINK = 3
MAX_LINKS_ERROR = 3
LEN_PREF_FILENAME = 5
PREF_SYMBOLS = string.ascii_letters + string.digits
TIMEOUT = 5


logging.config.dictConfig(LOGGING['logging'])
logger = logging.getLogger(__name__)


def for_download():
    while True:
        tags_to_publish = Tag.objects.filter(tag_to_publish__isnull=False)
        downloaded = Location.objects.filter(storage='file').filter(storage__isnull=False)
        gif_set = Gif.objects.filter(choices=1).filter(tagged__in=tags_to_publish).exclude(file_store__in=downloaded).distinct().first()
        print(gif_set)
        if gif_set:
            yield gif_set
        else:
            yield None


def main():
    max_links_errors = MAX_LINKS_ERROR
    # gifs = for_download()
    while max_links_errors:
        tags_to_publish = Tag.objects.filter(tag_to_publish__isnull=False)
        downloaded = Location.objects.filter(storage='file').filter(storage__isnull=False)
        gif = Gif.objects.filter(choices=1).filter(tagged__in=tags_to_publish).exclude(
            file_store__in=downloaded).distinct().first()
        print(gif)
        max_retry_link = MAX_RETRY_LINK
        while max_retry_link:
            logger.info('Starting nex image')
            logger.info('Sleep sometime')
            time.sleep(TIMEOUT)
            try:
                r = requests.get(gif.link)
            except:
                logger.error('Error when try get url {0} : {1}'.format(gif.link, sys.exc_info()))
                max_retry_link -= 1
                continue

            if not r:
                logger.error('Not 200 code {}'.format(r.status_code))
                max_retry_link -= 1
                continue


            if not r.content.endswith(b'\x00;'):        # every gif object should have end like this
                logger.error('Not correct gif {}'.format(gif.link))
                max_retry_link -= 1
                continue

            prefix = ''.join(random.choice(PREF_SYMBOLS) for _ in range(LEN_PREF_FILENAME))
            folder = datetime.datetime.now().strftime('%Y%m')
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = prefix + os.path.basename(gif.link)
            file_name = os.path.join(folder, file_name)
            print(file_name)
            with open(file_name, 'wb') as f:
                f.write(r.content)
            location = Location(storage='file', store_path=file_name)
            location.save()
            gif.file_store.add(location)
            logger.info('For gif id={0} save file image {1}'.format(gif.id, file_name))
            break

        if max_retry_link == 0:
            max_links_errors -= 1
        else:
            max_links_errors = MAX_LINKS_ERROR


if __name__ == '__main__':
    os.chdir(PATH)
    main()

