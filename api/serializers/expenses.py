from rest_framework import serializers
from core.models import Expense


class ExpenseModelSerializer(serializers.HyperlinkedModelSerializer):
    """Expense Model Serializer"""

    url = serializers.HyperlinkedIdentityField(view_name="expenses-viewset", read_only=True, lookup_field="id")
    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    description = serializers.CharField(max_length=255)
    amount = serializers.FloatField()

    class Meta:
        model = Expense
        fields = (
            'url', 'name', 'description', 'amount'
        )

