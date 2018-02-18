
import os
import django
import random
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
django.setup()

from gifs.models import *

# f = TagToPublish.objects.get(tag_to_publish='konosuba')
# print(f)
# e = Tag.objects.filter('tag_to_publish').select_related()
# for i in e:
#     print(e)
# e = TagToPublish.objects.all()
# for i in e:
#     g = i.tag_set.all()
#     print(g)
#     for j in g:
#         f = j.gif_set.all()
#         print(f)
#         print(i)
#
# e = Gif.objects.order_by('?')[:200]
# print()
# # f = random.choice(e)
# # print(f)
# # f = random.sample(e, 100)
# ff = 0
# for i in e:
#     # g = e.prefetch_related()
#     g = i.tagged.all()
#     for j in g:
#         # print(j)
#         l = j.tag_to_publish
#         if l:
#             ff +=1
#             print(l)
#             print(i.link)
#             break
# print(ff)


# e = Tag.objects.all()
# for i in e:
#     f = i.gif_set.all()
#     print(i.tag)
#     print(f)
#     print(time.sleep(10))
# for tag in self.tagged.all():
#     tag_to_publish = tag.tag_to_publish
#         if tag_to_publish:
#             return tag_to_publish


tag = "yandere"
e = Tag.objects.get(tag=tag)
f = open(tag+'.html', 'w')
for i in e.gif_set.all():
    f.write('<img src="{}"/>'.format(i.link))
f.close()
# order = Order.objects.get(order_name='vk')
# gif = Gif.objects.get(pk=4)
# l = InOrder(order=order, gif=gif)
# l.save()
# gif = Gif.objects.get(pk=1542)
# print(gif)


