from rest_framework import serializers

from api.serializers.entries import EntryModelSerializer
from api.serializers.expenses import ExpenseModelSerializer
from core.models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    """"""
    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    entries = EntryModelSerializer(source='entry_set', many=True, read_only=True)
    expenses = ExpenseModelSerializer(source='entry_set', many=True, read_only=True)

    class Meta:
        model = Category
        field = (
            'id', 'name', 'entries', 'expenses'
        )
