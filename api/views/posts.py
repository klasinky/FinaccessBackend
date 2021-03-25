from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAccountOwner, IsPostOwner
from api.serializers.posts import PostModelSerializer
from core.models import Post


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = PostModelSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsAuthenticated, IsPostOwner, ]

        return [p() for p in permissions]

    def get_object(self):
        """Retorna el Post del usuario"""
        return get_object_or_404(
            Post,
            pk=self.kwargs['id']
        )

    def get_queryset(self):
        return Post.objects.filter(is_active=True)

    def perform_create(self, serializer):
        """Añadir el author del post al momento de crearlo"""
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete()
        instance.save()

    @action(detail=False, methods=['PATCH'])
    def change_finished_post(self, request, *args, **kwargs):
        """Cambia la variable finished"""
        serializer_context = {
            'request': request,
        }
        post = self.get_object()
        post.finished = not post.finished

        post.save()
        data = PostModelSerializer(post, context=serializer_context).data
        return Response(data, status=status.HTTP_200_OK)
