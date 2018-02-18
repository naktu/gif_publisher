import time
import os
import sys
import django


from gifs.utils import vk
import secret

prj_path = '/home/tutunak/Dropbox/prj/web/gif_publisher'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gif_publisher.settings")
sys.path.append(prj_path)
os.chdir(prj_path)
django.setup()


from gifs import models

def for_download():
    tags_to_publish = models.Tag.objects.filter(tag_to_publish__isnull=False)
    downloaded = models.Location.objects.filter(storage='vk',
                                                storage__isnull=False)
    gif_set = models.Gif.objects.filter(choices=1,
                                        tagged__in=tags_to_publish)
    gif_set = gif_set.exclude(file_store__in=downloaded).distinct().first()

    return gif_set


if __name__ == '__main__':
    while True:
        gif = for_download()
        anime_gif = vk.Group(-96920344, secret.API)
        loc = models.Location.objects.filter(storage__exact='file',
                                             gif__exact=gif)
        print(loc[0].store_path)
        gif_upload = vk.UploadFile('doc',
                                   loc[0].store_path,
                                   secret.API,
                                   -96920344)
        result = gif_upload.upload_doc()
        if result:
            vk_loc = models.Location(storage='vk', store_path=result)
            vk_loc.save()
            gif.file_store.add(vk_loc)
        time.sleep(1800)


