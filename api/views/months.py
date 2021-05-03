from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from api.permissions import IsAccountOwner
from api.serializers.categories import CategoryModelSerializer
from api.serializers.entries import EntryModelSerializer
from api.serializers.expenses import ExpenseModelSerializer
from api.serializers.months import MonthModelSerializer
from core.models import Month, Expense, Entry, Category
from rest_framework.response import Response
from django.apps import apps


class MonthViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin,
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
            pk=self.kwargs['id'],
            is_active=True
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_context = {
            'request': request,
        }

        serializer_month = self.get_serializer(instance,
                                               context=serializer_context)
        category = Category.objects.filter(Q(expense__month=instance) |
                                           Q(entry__month=instance)).distinct()

        categories = []

        for c in category:
            expenses = Expense.objects.filter(month=instance,
                                              category=c, is_active=True)
            entries = Entry.objects.filter(month=instance,
                                           category=c, is_active=True)

            category_serializer = CategoryModelSerializer(c,
                                                          context=serializer_context,
                                                          month=instance)
            data = {
                'category': category_serializer.data,
                'category_data': {
                    'expenses': ExpenseModelSerializer(expenses,
                                                       many=True,
                                                       context=serializer_context).data,
                    'entries': EntryModelSerializer(entries,
                                                    many=True,
                                                    context=serializer_context).data,
                }
            }

            categories.append(data)

        data = {
            'month': serializer_month.data,
            'categories': categories
        }

        return Response(data)

    def get_amount_stats(self, filter_category, month, model_name):
        """
            https://stackoverflow.com/questions/38778080/pass-kwargs-into-django-filter
        """
        categories = Category.objects.filter(**filter_category).distinct()
        data = []
        total = 0
        model = apps.get_model('core', model_name)
        for c in categories:
            model_instance = model.objects.filter(month=month, category=c)

            for instance in model_instance:
                total += instance.amount

            data.append({
                'name': str(c.name),
                'total': total,
            })
            total = 0

        return Response(list(data))

    @action(detail=True, methods=['GET'])
    def category_expenses_stats(self, request, *args, **kwargs):
        """Obtiene los gastos de cada una de las categorias"""
        instance = self.get_object()
        your_filters = {
            'expense__month__pk': instance.pk,
        }
        return self.get_amount_stats(your_filters, instance, 'expense')

    @action(detail=True, methods=['GET'])
    def category_entries_stats(self, request, *args, **kwargs):
        """Obtiene los ingresos de cada una de las categorias"""
        instance = self.get_object()
        your_filters = {
            'entry__month__pk': instance.pk,
        }
        return self.get_amount_stats(your_filters, instance, 'entry')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['GET'])
    def get_amount_base_all(self, request, *args, **kwargs):
        month = self.get_object()
        entries = Entry.objects.filter(month=month, is_active=True)
        expenses = Expense.objects.filter(month=month, is_active=True)
        results = []
        serializer_context = {
            'request': request,
        }
        for entry in entries:
            results.append({
                'data': EntryModelSerializer(entry, context=serializer_context).data,
                'is_expense': False,
            })
        for expense in expenses:
            results.append({
                'data': ExpenseModelSerializer(expense, context=serializer_context).data,
                'is_expense': True,
            })
        results = sorted(results, key=lambda k: k['data']['created_at'])
        return Response(results, status=status.HTTP_200_OK)
