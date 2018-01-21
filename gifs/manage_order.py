import logging.config
import os
import django
import random
import datetime
import sys
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
django.setup()


from gifs.models import *


ORDER = 'vk'

order = Order.objects.get(order_name=ORDER)
gifs_order = InOrder.objects.filter(order__exact=order)
tags_to_publish = Tag.objects.filter(tag_to_publish__isnull=False)
start = time.time()
gif_set = Gif.objects.filter(choices=1).filter(tagged__in=tags_to_publish).exclude(inorder__in=gifs_order).distinct()
# gif_set = Gif.objects.filter(choices=1)
# for i in gif_set:
#     print(i)
print(len(gif_set))

gif_set =Gif.objects.filter(choices=1)
print(len(gif_set))
print(Gif.objects.count())
