from rest_framework import serializers
from core.models import Entry


class EntryModelSerializer(serializers.HyperlinkedModelSerializer):
    """Entry Model Serializer"""

    url = serializers.HyperlinkedIdentityField(view_name="entries-viewset", read_only=True, lookup_field="id")
    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    description = serializers.CharField(max_length=255)
    amount = serializers.FloatField()

    class Meta:
        model = Entry
        fields = (
            'url', 'name', 'description', 'amount'
        )