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


# ORDER = 'vk'
# order = Order.objects.get(order_name=ORDER)
# gifs_unordered = InOrder.objects.filter(order__exact=order).all()
#
# for i in gifs_unordered:
#     i.place_in_order = None
#     i.save()
