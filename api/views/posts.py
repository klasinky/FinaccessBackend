from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAccountOwner, IsPostOwner
from api.serializers.posts import PostModelSerializer
from core.models import Post
from django.core.cache import cache


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

    def create(self, request, *args, **kwargs):
        if cache.has_key('post_created'):
            return Response({'detail': 'Tienes que esperar 5 minutos para crear otro post'},
                            status=status.HTTP_400_BAD_REQUEST)
        response = super(PostViewSet, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.set('post_created', True, timeout=300)
        return response

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


class PostLikeView(APIView):
    permissions_class = [IsAuthenticated, ]

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.pop('id')
        self.post = get_object_or_404(Post, id=id)
        return super(PostLikeView, self).dispatch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }

        if cache.has_key(f'post_liked{self.post.pk}'):
            return Response({'detail': 'Tienes que esperar 10 s'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user in self.post.likes.all():
            self.post.likes.remove(request.user)
        else:
            self.post.likes.add(request.user)
        self.post.save()
        cache.set(f'post_liked{self.post.pk}', True, timeout=10)
        data = PostModelSerializer(self.post, context=serializer_context).data
        return Response(data, status.HTTP_200_OK)
