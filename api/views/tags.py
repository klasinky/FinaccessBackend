from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.posts import TagPostSerializer
from core.models import Tag


class TagAPIView(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        data = TagPostSerializer(tags, many=True).data

        return Response(data)
