from rest_framework import serializers

from api.serializers.categories import CategoryInfoSerializer


class AmountBaseModelSerializer(serializers.HyperlinkedModelSerializer):
    """AmountBase Model Serializer"""

    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    description = serializers.CharField(max_length=255)
    amount = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
    category = CategoryInfoSerializer(read_only=True)

    class Meta:
        abstract = True
