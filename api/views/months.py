from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from api.permissions import IsAccountOwner
from api.serializers.entries import EntryModelSerializer
from api.serializers.expenses import ExpenseModelSerializer
from api.serializers.months import MonthModelSerializer
from core.models import Month, Expense, Entry, Category
from rest_framework.response import Response


class MonthViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = MonthModelSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsAuthenticated, IsAccountOwner]

        return [p() for p in permissions]

    def get_queryset(self):
        return Month.objects.filter(user=self.request.user, is_active=True)

    def get_object(self):
        """Retorna el MONTH del usuario"""
        return get_object_or_404(
            Month,
            user=self.request.user,
            pk=self.kwargs['id']
        )

    def perform_destroy(self, instance):
        instance.soft_delete()
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_month = self.get_serializer(instance)
        category = Category.objects.filter(Q(expense__month=instance) | Q(entry__month=instance))
        categories = []
        for c in category:
            expenses = Expense.objects.filter(month=instance, category=c, is_active=True)
            entries = Entry.objects.filter(month=instance, category=c, is_active=True)
            data = {
                str(c.name): {
                    'expenses': ExpenseModelSerializer(expenses, many=True).data,
                    'entries': EntryModelSerializer(entries, many=True).data,
                }
            }
            categories.append(data)

        # expenses = Expense.objects.filter(month=instance, is_active=True)
        # entries = Entry.objects.filter(month=instance, is_active=True)

        data = {
            'month': serializer_month.data,
            # 'expenses': ExpenseModelSerializer(expenses, many=True).data,
            # 'entries': EntryModelSerializer(entries, many=True).data
            'categories': categories
        }

        return Response(data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


