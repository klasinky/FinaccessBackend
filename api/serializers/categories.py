from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from core.models import Category, Entry, Expense


class CategoryModelSerializer(serializers.ModelSerializer):
    """Category Model Serializer"""

    name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True)
    total_entries = SerializerMethodField(read_only=True)
    total_expenses = SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        self.month = kwargs.pop('month')
        super(CategoryModelSerializer, self).__init__(*args, **kwargs)

    def get_total_entries(self, obj):
        """Retorna el total de ingresos del mes"""
        total = Entry.objects.filter(category=obj, month=self.month) \
                    .aggregate(Sum('amount'))['amount__sum'] or 0.0
        return total

    def get_total_expenses(self, obj):
        """Retorna el total de gastos del mes"""
        total = Expense.objects.filter(category=obj, month=self.month) \
                    .aggregate(Sum('amount'))['amount__sum'] or 0.0
        return total

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'total_entries', 'total_expenses'
        )
