from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAmountBaseOwner
from api.serializers.expenses import ExpenseModelSerializer
from api.views.amount_base import AmountBaseCreateView, AmountBaseUploadXLS, AmountBaseDownloadXLS
from core.models import Expense


class ExpenseCreateView(AmountBaseCreateView):
    serializer_class = ExpenseModelSerializer


class ExpenseViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = ExpenseModelSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsAmountBaseOwner, ]

    def get_queryset(self):
        return Expense.objects.filter(month__user=self.request.user, is_active=True)

    def get_object(self):
        """Retorna el Expense del usuario"""
        return get_object_or_404(
            Expense,
            month__user=self.request.user,
            pk=self.kwargs['id']
        )


class ExpenseUploadXLS(AmountBaseUploadXLS):
    model = Expense


class ExpenseDownloadXLS(AmountBaseDownloadXLS):
    model = Expense
    filename = "Expense_report_"
