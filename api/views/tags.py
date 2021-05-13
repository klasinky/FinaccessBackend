from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.posts import TagPostSerializer
from api.serializers.tags import TagDetailSerializer
from core.models import Tag


class TagAPIView(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        data = TagPostSerializer(tags, many=True).data

        return Response(data)


class TagDetailView(APIView):

    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tags = Tag.objects.all()
        data = TagDetailSerializer(tags, many=True).data
        return Response(data)