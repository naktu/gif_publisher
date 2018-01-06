from django.db import models

# class Blog(models.Model):
#     name = models.TextField()
#     url = models.URLField(name="Blog url")
#     offset = models.IntegerField(name='Offset for next end search', blank=True, null=True)
#     full_parse = models.BooleanField(name="All old posts is parsed", default=False)
#     # When checked - Status True. When all blogs checked - set for all True
#     checked = models.BooleanField(name="Checked last time", default=False)
#
#     def __str__(self):
#         return str(self.name)
#
# class Tag_source(models.Model):
#     tag = models.TextField(name='Tag on tumblr')
#
#     def __str__(self):
#         return str(self.tag)
#
# class Post(models.Model):
#     id = models.BigIntegerField(name='Post id')
#     type = models.TextField(name='Type of post')
#     url = models.URLField(name='Link to post')
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     tag = models.ManyToManyField(Tag_source)
#
#     def __str__(self):
#         return str(self.id)
#
# class Media(models.Model):
#     url = models.URLField(unique=True)
#     file = models.TextField(name='File on disk')
#     type = models.TextField(name='Type of file')
#     post = models.ForeignKey(Post)
#
#     def __str__(self):
#         return str(self.url)

class TagToPublish(models.Model):
    tag_to_publish = models.TextField()

    def __str__(self):
        return self.tag_to_publish


class Tag(models.Model):
    tag = models.TextField(unique=True)
    active = models.BooleanField(default=False)
    tag_to_publish = models.ForeignKey(TagToPublish, blank=True, null=True, on_delete=models.SET_NULL)
    not_to_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.tag

    def count(self):
        return self.gif_set.count()


class Post(models.Model):
    tumblr_post_id = models.BigIntegerField()
    post_url = models.URLField(blank=True)
    timestamp = models.IntegerField(null=False)
    json = models.TextField()
    tagged = models.ForeignKey(Tag)

    def __str__(self):
        return self.post_url


# class Tagged(models.Model):
#     post = models.ForeignKey(Post)
#     tag = models.ForeignKey(Tag)




class Gif(models.Model):
    link = models.URLField(unique=True)
    # link = models.ImageField()
    post = models.ForeignKey(Post)
    tagged = models.ManyToManyField(Tag)
    to_publish = models.BooleanField(default=False)
    never_publish = models.BooleanField(default=False)
    choices = models.IntegerField(
        choices=[
            (1, 'To publish'),
            (2, 'Never Publish'),
            (0, 'Null')
    ], default=0)

    def image(self):
        return '<image src={} />'.format(self.link)

    image.allow_tags = True
    # image.

    def __str__(self):
        return self.link

    def tag_to_publish(self):
        for tag in self.tagged.all():
            tag_to_publish = tag.tag_to_publish
            if tag_to_publish:
                return tag_to_publish

    def next(self):
        try:
            return Gif.objects.get(pk=self.pk+1)
        except:
            return None
