from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.categories import CategoryModelSerializer
from core.models import Category


class CategoryAPIView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append({
                'id': category.pk,
                'name': category.name,
            })
        return Response(data)