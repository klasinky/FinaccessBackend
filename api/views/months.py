import datetime

from django.db.models import Q, Sum
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView

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

    pagination_class = LimitOffsetPagination
    serializer_class = MonthModelSerializer
    lookup_field = "id"
    LimitOffsetPagination.default_limit = 9

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
        categories = Category.objects.all()
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

        return list(data)

    @action(detail=True, methods=['GET'])
    def category_expenses_stats(self, request, *args, **kwargs):
        """Obtiene los gastos de cada una de las categorias"""
        instance = self.get_object()
        your_filters = {
            'expense__month__pk': instance.pk,
        }
        return Response(self.get_amount_stats(your_filters, instance, 'expense'))

    @action(detail=True, methods=['GET'])
    def category_entries_stats(self, request, *args, **kwargs):
        """Obtiene los ingresos de cada una de las categorias"""
        instance = self.get_object()
        your_filters = {
            'entry__month__pk': instance.pk,
        }
        return Response(self.get_amount_stats(your_filters, instance, 'entry'))

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

    @action(detail=True, methods=['GET'])
    def get_analysis(self, request, *args, **kwargs):
        current_month = self.get_object()
        current_month_expenses = self.get_amount_stats('', current_month, 'expense')
        current_month_entries = self.get_amount_stats('', current_month, 'entry')
        date = current_month.date
        date = date.replace(day=1)
        last_month_date = date - datetime.timedelta(days=1)
        last_month_count = Month.objects.filter(
            date__month=last_month_date.month,
            date__year=last_month_date.year
        ).count()
        data = []
        # Variables para tomar el total (No por categoria)
        current_expense_global = 0
        current_entries_global = 0
        previous_expense_global = 0
        previous_entries_global = 0
        if last_month_count > 0:
            previous_month = Month.objects.filter(
                date__month=last_month_date.month,
                date__year=last_month_date.year
            )[0]
            previous_month_expenses = self.get_amount_stats('', previous_month, 'expense')
            previous_month_entries = self.get_amount_stats('', previous_month, 'entry')

            for i in range(0, len(current_month_entries)):
                category_name = current_month_expenses[i]['name']
                total_current_expenses = current_month_expenses[i]['total']
                total_previous_expenses = previous_month_expenses[i]['total']

                total_current_entries = current_month_entries[i]['total']
                total_previous_entries = previous_month_entries[i]['total']

                # Estadisticas globales
                current_entries_global += total_current_entries
                current_expense_global += total_current_expenses
                previous_entries_global += total_previous_entries
                previous_expense_global += total_previous_expenses
                # Expenses
                try:
                    increase_expenses = (total_current_expenses - total_previous_expenses) / total_previous_expenses
                    increase_expenses = round(increase_expenses * 100, 2)
                except ZeroDivisionError:
                    if total_current_expenses > 0:
                        increase_expenses = 100
                    else:
                        increase_expenses = 0

                # Entries
                try:
                    increase_entries = (total_current_entries - total_previous_entries) / total_previous_entries
                    increase_entries = round(increase_entries * 100, 2)
                except ZeroDivisionError:
                    if total_current_entries > 0:
                        increase_entries = 100
                    else:
                        increase_entries = 0

                data.append({
                    'category': category_name,
                    'increase_expenses': increase_expenses,
                    'increase_entries': increase_entries
                })
        else:
            for i in range(0, len(current_month_entries)):
                category_name = current_month_expenses[i]['name']
                current_expense_global += current_month_expenses[i]['total']
                current_entries_global += current_month_entries[i]['total']

                data.append({
                    'category': category_name,
                    'increase_expenses': 100,
                    'increase_entries': 100
                })

        try:
            increase_global_entries = (current_entries_global - previous_entries_global) / previous_entries_global
            increase_global_entries = round(increase_global_entries * 100, 2)
        except ZeroDivisionError:
            if current_entries_global > 0:
                increase_global_entries = 100
            else:
                increase_global_entries = 0

        try:
            increase_global_expenses = (current_expense_global - previous_expense_global) / previous_expense_global
            increase_global_expenses = round(increase_global_expenses * 100, 2)
        except ZeroDivisionError:
            if current_expense_global > 0:
                increase_global_expenses = 100
            else:
                increase_global_expenses = 0

        result = {
            'increase_expenses': increase_global_expenses,
            'increase_entries': increase_global_entries,
            'categories': data
        }
        return Response(result, 200)


class MonthOverView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """
        Calcula los ingresos y gastos, filtra por
        el mes  y el año actual y de por vida.
        """
        filter_query = request.query_params.get('q')
        query = Q()
        if filter_query:
            today = datetime.datetime.now()
            if filter_query == 'month':
                query.add(Q(date__year=today.year), Q.AND)
                query.add(Q(date__month=today.month), Q.AND)
            if filter_query == 'year':
                query.add(Q(date__year=today.year), Q.AND)

        month_data = Month.objects.filter(query, Q(is_active=True), Q(user=request.user))
        total_entries = 0
        total_expenses = 0
        for month in month_data:
            entries = Entry.objects.filter(month=month). \
                aggregate(Sum('amount'))
            total_entries += entries['amount__sum'] or 0
            expenses = Expense.objects.filter(month=month). \
                aggregate(Sum('amount'))
            total_expenses += expenses['amount__sum'] or 0

        data = {
            'total_expenses': total_expenses,
            'total_entries': total_entries
        }

        return Response(data, status=status.HTTP_200_OK)
