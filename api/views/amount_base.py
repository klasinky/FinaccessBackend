from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Month, Category


class AmountBaseCreateView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, ]

    def dispatch(self, request, *args, **kwargs):
        id_month = kwargs.pop('id')
        self.month = get_object_or_404(Month, id=id_month)
        return super(AmountBaseCreateView, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        category = request.data['category']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = get_object_or_404(Category, id=category)

        self.perform_create(serializer, category=category)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, category):
        serializer.save(category=category, month=self.month)