from rest_framework import serializers

from api.serializers.months import MonthModelSerializer
from core.models import Expense


class ExpenseModelSerializer(serializers.ModelSerializer):
    """"""
    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    description = serializers.CharField(max_length=255)
    amount = serializers.FloatField()
    month = MonthModelSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = (
            'id', 'name', 'description', 'amount', 'month'
        )
