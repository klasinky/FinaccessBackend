from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.notifications import NotificationModelSerializer
from core.models import Notification


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_notifications(request):
    notifications = Notification.objects.filter(
        to_user=request.user,
        is_read=False,
    )
    data = NotificationModelSerializer(notifications, many=True).data;
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def read_notifications(request, id):
    try:
        notification = Notification.objects.get(
            id=id,
            to_user=request.user
        )
        notification.is_read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
