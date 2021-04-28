from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Currency
from user.serializers import CurrencyModelSerializer


class CurrencyAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        currencies = Currency.objects.all()
        data = CurrencyModelSerializer(currencies, many=True).data
        return Response(data)