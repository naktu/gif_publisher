
import os
import django
import random
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
django.setup()
from gifs.models import *
#
# ### Tag to html
tag = "haru"
e = Tag.objects.get(tag=tag)
f = open(tag+'.html', 'w')
for i in e.gif_set.all():
    f.write('<img src="{}"/>'.format(i.link))
f.close()


#
# tags_to_publish = Tag.objects.filter(tag_to_publish__isnull=False)
# gif_set = Gif.objects.exclude(tagged__in=tags_to_publish).distinct()[:200]
# tags = []
# tag = Tag.objects.exclude(gif__in=gif_set).distinct()
# print(tag.count())
# # for i in gif_set:
# #     tag = Tag.objects.filter(gif__exact=i)
# #     for t in tag:
# #         tags.append(t)






# tag = Tag.objects.exclude(gif__in=gif_set)
# print(tag.count())