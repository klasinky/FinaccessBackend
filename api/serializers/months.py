from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from rest_framework import serializers

from core.models import Month, Entry, Expense
from user.serializers import UserModelSerializer


class MonthModelSerializer(serializers.ModelSerializer):
    """Month serializer"""

    user = UserModelSerializer(read_only=True)
    date = serializers.DateField(read_only=True)
    total_entries = serializers.SerializerMethodField(read_only=True)
    total_expenses = serializers.SerializerMethodField(read_only=True)

    def get_total_entries(self, obj):
        """Retorna el total de ingresos del mes"""
        total = Entry.objects.filter(month=obj)\
            .aggregate(Sum('amount'))['amount__sum'] or 0.0
        return total

    def get_total_expenses(self, obj):
        """Retorna el total de gastos del mes"""
        total = Expense.objects.filter(month=obj)\
            .aggregate(Sum('amount'))['amount__sum'] or 0.0
        return total

    """
    total_entries =
    total_expenses = 
    CATEGORIES = [
        category1: [
            entries: []
            expenses: []
        ]
    ] 
    """
    class Meta:
        model = Month
        fields = (
            'id', 'user', 'date', 'total_entries', 'total_expenses'
        )
