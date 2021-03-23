import datetime
from django.db.models import Sum
from rest_framework import serializers
from core.models import Month, Entry, Expense


class MonthModelSerializer(serializers.HyperlinkedModelSerializer):
    """Month serializer"""

    url = serializers.HyperlinkedIdentityField(view_name="months-viewset",
                                               read_only=True,
                                               lookup_field="id")
    date = serializers.DateField(read_only=True, format="%Y-%m")
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

    def create(self, validated_data):
        user = validated_data['user']
        now = datetime.date.today()
        if Month.objects.filter(user=user, date__month=now.month, date__year=now.year).exists():
            raise serializers.ValidationError({"detail": "No puedes crear dos meses iguales"})

        obj = Month.objects.create(**validated_data)
        return obj

    class Meta:
        model = Month
        fields = (
            'url', 'date', 'total_entries', 'total_expenses'
        )
