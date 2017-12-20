from django.db import models

class Blog(models.Model):
    name = models.TextField()
    url = models.URLField(name="Blog url")
    offset = models.IntegerField(name='Offset for next end search', blank=True, null=True)
    full_parse = models.BooleanField(name="All old posts is parsed", default=False)
    # When checked - Status True. When all blogs checked - set for all True
    checked = models.BooleanField(name="Checked last time", default=False)

    def __str__(self):
        return str(self.name)

class Tag_source(models.Model):
    tag = models.TextField(name='Tag on tumblr')

    def __str__(self):
        return str(self.tag)

class Post(models.Model):
    id = models.BigIntegerField(name='Post id')
    type = models.TextField(name='Type of post')
    url = models.URLField(name='Link to post')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag_source)

    def __str__(self):
        return str(self.id)

class Media(models.Model):
    url = models.URLField(unique=True)
    file = models.TextField(name='File on disk')
    type = models.TextField(name='Type of file')
    post = models.ForeignKey(Post)

    def __str__(self):
        return str(self.url)


