from django.urls import reverse
from rest_framework import serializers
from core.models import Comment
from user.serializers import UserProfileSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    """CommentCreate Model Serializer"""
    description = serializers.CharField(allow_null=False,
                                        min_length=10,
                                        max_length=500)

    class Meta:
        model = Comment
        fields = ('description',)


class CommentDetailSerializer(serializers.ModelSerializer):
    """CommentDetail Serializer"""
    description = serializers.CharField(allow_null=False,
                                        min_length=10,
                                        max_length=500,
                                        read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    author = UserProfileSerializer()
    parent = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    url_like = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_like(self, obj):
        request = self.context.get('request')
        return request.user in obj.likes.all()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.author

    def get_url_like(self, obj):
        request = self.context.get('request')
        url = reverse('comments-like', args=[obj.pk])
        return f"{request.build_absolute_uri(url)}"

    def get_likes(self, obj):
        return obj.total_likes()

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.pk
        else:
            return None

    class Meta:
        model = Comment
        fields = ('description', 'author', 'parent', 'likes', 'url_like','created_at','is_like','is_owner','id')
