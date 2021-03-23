from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAmountBaseOwner
from api.serializers.entries import EntryModelSerializer
from api.views.amount_base import AmountBaseCreateView
from core.models import Entry


class EntryCreateView(AmountBaseCreateView):

    serializer_class = EntryModelSerializer


class EntryViewSet(mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = EntryModelSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsAmountBaseOwner, ]

    def perform_destroy(self, instance):
        instance.soft_delete()
        instance.save()

    def get_queryset(self):
        return Entry.objects.filter(month__user=self.request.user, is_active=True)

    def get_object(self):
        """Retorna el Expense del usuario"""
        return get_object_or_404(
            Entry,
            month__user=self.request.user,
            pk=self.kwargs['id']
        )