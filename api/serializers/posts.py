from django.urls import reverse
from rest_framework import serializers

from core.models import Post, Tag
from user.serializers import UserModelSerializer


class TagPostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, max_length=255)
    color = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = Tag
        fields = ('name', 'color', 'id')


class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=5000000)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Post
        fields = (
            'title', 'description','tags'
        )


class PostModelSerializer(serializers.HyperlinkedModelSerializer):
    """Post Model Serializer"""
    url = serializers.HyperlinkedIdentityField(view_name="posts-viewset", read_only=True, lookup_field="id")
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=5000000)
    finished = serializers.BooleanField(default=False, required=False)
    author = UserModelSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    url_like = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    tags = TagPostSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def get_is_like(self, obj):
        request = self.context.get('request')
        return request.user in obj.likes.all()

    def get_url_like(self, obj):
        request = self.context.get('request')
        url = reverse('posts-like', args=[obj.pk])
        return f"{request.build_absolute_uri(url)}"

    def get_likes(self, obj):
        return obj.total_likes()

    class Meta:
        model = Post
        fields = (
            'id', 'url', 'title', 'description',
            'finished', 'author', 'likes', 'url_like',
            'is_like', 'tags','created_at'
        )
