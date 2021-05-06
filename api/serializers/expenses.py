from rest_framework import serializers
from api.serializers.amount_base import AmountBaseModelSerializer
from core.models import Expense


class ExpenseModelSerializer(AmountBaseModelSerializer):
    """Expense Model Serializer"""

    url = serializers.HyperlinkedIdentityField(view_name="expenses-viewset", read_only=True, lookup_field="id")

    class Meta:
        model = Expense
        fields = (
            'url', 'name', 'description', 'amount', 'created_at', 'id', 'category'
        )

