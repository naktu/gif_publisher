#!/usr/bin/env python
from rest_framework import serializers
from gifs.models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class GifSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    # tagged = TagSerializer(many=True, read_only=True)
    tagged = serializers.StringRelatedField(many=True)
    class Meta:
        model = Gif
        fields = '__all__'
        depth = 1




