from rest_framework import serializers

from app import settings
from core.models import Tag, Post


class TagPostSerializer(serializers.ModelSerializer):
    """Serializer para indicar el Tag de los post"""
    name = serializers.CharField(read_only=True, max_length=255)
    color = serializers.CharField(read_only=True, max_length=255)
    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        request = self.context.get('request')
        url = None
        if obj.image:
            params = f'{settings.STATIC_URL}images{obj.image.url}'
            url = request.build_absolute_uri(params)
        return url

    class Meta:
        model = Tag
        fields = ('name', 'color', 'id','image')


class TagDetailSerializer(serializers.ModelSerializer):
    """Serializer que calcula el numero de post por tag"""
    name = serializers.CharField(read_only=True, max_length=255)
    num_post = serializers.SerializerMethodField()

    def get_num_post(self, obj):
        num_post = Post.objects.filter(tags=obj, is_active=True).distinct().count()
        return num_post

    class Meta:
        model = Tag
        fields = ('name', 'num_post', 'id')
