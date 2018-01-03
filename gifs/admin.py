from django.contrib import admin
from gifs.models import *

# admin.site.register(Blog, Post, Tag_source, Media)
admin.site.register([Tag, Post, GifLink])