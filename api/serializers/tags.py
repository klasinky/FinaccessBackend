from rest_framework import serializers

from core.models import Tag, Post


class TagPostSerializer(serializers.ModelSerializer):
    """Serializer para indicar el Tag de los post"""
    name = serializers.CharField(read_only=True, max_length=255)
    color = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = Tag
        fields = ('name', 'color', 'id')


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
