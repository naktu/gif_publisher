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
gifs_unordered = InOrder.objects.filter(order__exact=order).filter(place_in_order=None)
gifs_order = InOrder.objects.filter(order__exact=order).exclude(place_in_order=None).order_by('place_in_order')[:5]

tag = []
for item in gifs_order:
    tag.append(item.gif.tag_to_publish())

h = 10
last_order = []

while True:
    gifs_unordered = InOrder.objects.filter(order__exact=order).filter(place_in_order=None)
    if gifs_unordered == last_order:
        break
    gifs_order = InOrder.objects.filter(order__exact=order).exclude(place_in_order=None).order_by('-place_in_order')[:5]

    # gifs_last = InOrder.objects.filter(order__exact=order).exclude(place_in_order=None).order_by('place_in_order').last()
    # print(gifs_last.place_in_order)
    if gifs_unordered:
        tag = []
        for item in gifs_order:
            tag.append(item.gif.tag_to_publish())
        for item in gifs_unordered:

            if item.gif.tag_to_publish() not in tag:
                if gifs_order:
                    item.place_in_order = 1 + gifs_order.first().place_in_order
                else:
                    item.place_in_order = 1
                item.save()
                break
    else:
        print('Done')
        break
    last_order = gifs_unordered[:]




