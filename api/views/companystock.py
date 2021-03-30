from django.urls import reverse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from app import settings
from core.models import UserCompany, CompanyStock


class CompanyStockView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        """Retorna los datos del mercado de la compañía"""
        stock_company = get_object_or_404(
            UserCompany,
            user=request.user,
            pk=id)

        url = "https://www.alphavantage.co/query?" \
            f"function=TIME_SERIES_DAILY_ADJUSTED&symbol="\
            f"{stock_company.companystock.symbol}"\
            f"&outputsize=compact&apikey={settings.STOCK_API_KEY}"

        res = requests.get(url)
        data = res.json()
        data = data['Time Series (Daily)']
        index = 0
        prices = []
        for item in data:
            prices.append({
                'date': item,
                'close': data[item].get('4. close')
            })
        stock = {
            'name': stock_company.companystock.name,
            'prices': prices
        }

        return Response(list(stock), status=status.HTTP_200_OK)

    def post(self, request, id):
        """Suscribirse a una acción"""
        company = get_object_or_404(CompanyStock, id=id)
        if UserCompany.objects.filter(user=request.user).exists():
            return Response({'detail': 'Ya estas suscrito a esa acción'},
                            status=status.HTTP_400_BAD_REQUEST)

        UserCompany.objects.create(user=request.user, companystock=company)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id):
        """Elimina la suscripción a una acción"""
        user_company = get_object_or_404(UserCompany, id=id)
        if user_company.user != request.user:
            return Response({'detail': 'No tienes permisos para eliminar a este recurso'},
                            status=status.HTTP_400_BAD_REQUEST)
        user_company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyStockListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """Lista todas las acciones a la que esta suscrita"""
        data = UserCompany.objects.filter(user=request.user).distinct()
        stock_list = []
        for item in data:
            url = reverse('companystock-view', args=[item.companystock.pk])

            stock = {
                'id': item.companystock.pk,
                'name': item.companystock.name,
                'url': request.build_absolute_uri(url)
            }
            stock_list.append(stock)
        return Response(list(stock_list), status=status.HTTP_200_OK)


class CompanyListView(APIView):

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        companies = CompanyStock.objects.all()
        data = []
        for company in companies:
            data.append({
                'id': company.id,
                'name': company.name,
                'symbol': company.symbol
            })
        return Response(list(data), status=status.HTTP_200_OK)