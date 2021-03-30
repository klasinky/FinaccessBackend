from rest_framework import serializers


class AmountBaseModelSerializer(serializers.HyperlinkedModelSerializer):
    """AmountBase Model Serializer"""

    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    description = serializers.CharField(max_length=255)
    amount = serializers.FloatField()

    class Meta:
        abstract = True