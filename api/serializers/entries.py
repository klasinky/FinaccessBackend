from rest_framework import serializers

from api.serializers.months import MonthModelSerializer
from core.models import Entry


class EntryModelSerializer(serializers.ModelSerializer):
    """Entry Model Serializer"""

    # url = serializers.HyperlinkedIdentityField(view_name="months-retrieve-update", read_only=True, lookup_field="id")
    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    description = serializers.CharField(max_length=255)
    amount = serializers.FloatField()

    class Meta:
        model = Entry
        fields = (
            'id', 'name', 'description', 'amount'
        )