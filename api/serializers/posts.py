from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from core.models import Post
from user.serializers import UserModelSerializer


class PostModelSerializer(serializers.HyperlinkedModelSerializer):
    """Post Model Serializer"""
    url = serializers.HyperlinkedIdentityField(view_name="posts-viewset", read_only=True, lookup_field="id")
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=5000)
    finished = serializers.BooleanField(default=False, required=False)
    author = UserModelSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.total_likes()

    class Meta:
        model = Post
        fields = (
            'url', 'title', 'description', 'finished', 'author', 'likes'
        )
