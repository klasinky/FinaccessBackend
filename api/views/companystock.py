from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from app import settings


class CompanyStockData(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        url = "https://www.alphavantage.co/query?" \
              "function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM" \
              f"&outputsize=compact&apikey={settings.STOCK_API_KEY}"

        res = requests.get(url)
        data = res.json()
        data = data['Time Series (Daily)']
        index = 0
        stock = []
        for key in data:
            if index >= 7:
                break
            stock.append({
                'date': key,
                'close': data[key].get('4. close')
            })
            index += 1
        return Response(list(stock), status=status.HTTP_200_OK)
