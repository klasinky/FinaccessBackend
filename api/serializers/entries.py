from rest_framework import serializers
from api.serializers.amount_base import AmountBaseModelSerializer
from core.models import Entry


class EntryModelSerializer(AmountBaseModelSerializer):
    """Entry Model Serializer"""

    url = serializers.HyperlinkedIdentityField(view_name="entries-viewset", read_only=True, lookup_field="id")

    class Meta:
        model = Entry
        fields = (
            'url', 'name', 'description', 'amount', 'created_at', 'id', 'category'
        )