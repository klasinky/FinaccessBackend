from rest_framework import serializers

from core.models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    id_type = serializers.IntegerField(read_only=True)
    notification_type = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)
    from_user = serializers.SerializerMethodField()

    def get_from_user(self, obj):
        if not obj.from_user:
            return None
        return obj.from_user.username

    class Meta:
        model = Notification
        fields = ('created_at','from_user', 'id_type', 'notification_type', 'content')
