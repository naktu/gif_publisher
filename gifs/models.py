import random
from django.db import models


class TagToPublish(models.Model):
    tag_to_publish = models.TextField()
    ru_tag = models.TextField(blank=True)
    eng_tag = models.TextField(blank=True)

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

    def __str__(self):
        return self.link

    def tag_to_publish(self):
        t = ''
        for tag in self.tagged.all():
            tag_to_publish = tag.tag_to_publish
            if tag_to_publish:
                t = tag_to_publish
        # if tag_to_publish:
        #     return tag_to_publish
        if t:
            return t


    def tags(self):
        # return ':'.join(i.tag for i in self.tagged.all())
        return ''.join("<br>{}<br>".format(i.tag) for i in self.tagged.all())

    tags.allow_tags = True


class Order(models.Model):
    order_name = models.TextField(blank=True)

    def __str__(self):
        return self.order_name


class InOrder(models.Model):
    class Meta:
        unique_together = (('order', 'gif'))
    order = models.ForeignKey(Order)
    gif = models.ForeignKey(Gif)
    place_in_order = models.IntegerField(blank=True, null=True)
    published = models.BooleanField(default=False)
    to_public = models.NullBooleanField(blank=True, default=None, null=True)

    def image(self):
        return '<image src={} />'.format(self.gif)

    image.allow_tags = True
