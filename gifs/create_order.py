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

gif_set = Gif.objects.filter(choices=1).filter(tagged__in=tags_to_publish).exclude(inorder__in=gifs_order).distinct()[:3000]

print(gif_set)

for gif in gif_set:
    in_order = InOrder(
        order=order,
        gif=gif
    )
    in_order.save()

