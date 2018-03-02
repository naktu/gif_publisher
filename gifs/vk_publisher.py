# Public new post in order if we have not 150 posts in order
import time
import django
import os
import sys



prj_path = '/home/tutunak/Dropbox/prj/web/gif_publisher'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
sys.path.append(prj_path)
os.chdir(prj_path)
django.setup()

from gifs import models
from gifs.utils import vk

import secret
def main():
    anime_gif = vk.Group(-96920344, secret.API)
    order = anime_gif.order_size()
    if not (order < 150):
        time.sleep(1800)
        return
    time.sleep(1)
    last = anime_gif.last_postponed()
    if not last:
        return
    last_date = last[0]['date']
    order = models.Order.objects.get(order_name__exact='vk')
    in_order = models.InOrder.objects.filter(
        order__exact=order
    ).exclude(
        published=True
    ).order_by(
        'place_in_order'
    ).first()
    gif = in_order.gif
    loc = models.Location.objects.filter(gif=gif)
    to_pub_attach = None
    for l in loc:
        if l.storage == 'vk':
            to_pub_attach = l.store_path
        elif l.storage == 'file':
            file_pub = l.store_path
    if not to_pub_attach:
        gif_upload = vk.UploadFile('doc',
                                   file_pub,
                                   secret.API,
                                   -96920344)
        result = gif_upload.upload_doc()
        if result:
            vk_loc = models.Location(storage='vk', store_path=result)
            vk_loc.save()
            gif.file_store.add(vk_loc)
            to_pub_attach = result
        time.sleep(1)
    print(gif.id)
    pub_tag = models.TagToPublish.objects.filter(tag__gif=gif)[0]
    tags =set()
    tags.add(pub_tag.tag_to_publish)
    tags.add(pub_tag.ru_tag)
    tags.add(pub_tag.eng_tag)

    message_tag = []
    for tag in tags:
        message_tag.append("_".join(n.capitalize() for n in tag.split()))



    params = {
        'from_group': 1,
        'publish_date': last_date + 3600,
        'message': '\n'.join('#' + n for n in message_tag),
        'attachment': to_pub_attach

    }
    l = anime_gif.post(**params)
    print(l)
    in_order.published = True
    in_order.save()

if __name__ == '__main__':
    while True:
        main()
        print('GO to sleep 1800 seconds')
        time.sleep(600)
