from django.contrib import admin
from gifs.models import *
from django.db import models

# admin.site.register(Blog, Post, Tag_source, Media)


class GifAdmin(admin.ModelAdmin):
    # fields = ['link', 'post', 'tagged', 'image', 'next']
    filter_horizontal = ('tagged',)
    list_display = ('id','choices', 'image', 'tag_to_publish' )
    list_filter = ['choices',]
    readonly_fields = ('image',)
    list_editable = ['choices']


admin.site.register(Gif, GifAdmin)

class TagAdmin(admin.ModelAdmin):
    # fields = ['tag', 'tag_to_publish']
    # filter_horizontal = ('tagged',)
    search_fields = ['tag']
    list_display = ('tag', 'tag_to_publish', 'active', 'not_to_publish', 'count')
    list_filter = ['active', 'not_to_publish', 'tag_to_publish']
    list_editable = ['tag_to_publish', 'active', 'not_to_publish']
    def get_queryset(self, request):
        qs = super(TagAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('gif'))
        return qs

    def count(self, obj):
        return obj.gif__count

    count.admin_order_field = 'gif__count'

admin.site.register(Tag, TagAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_url','timestamp')

admin.site.register(Post, PostAdmin)

class TagToPublishAdmin(admin.ModelAdmin):
    list_display = ('id','tag_to_publish',)
    list_editable = ('tag_to_publish',)


admin.site.register(TagToPublish,TagToPublishAdmin)