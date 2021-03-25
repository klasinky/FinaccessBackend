from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsCommentOwner
from api.serializers.comments import CommentCreateSerializer, CommentDetailSerializer
from core.models import Post, Comment


class CommentCreateView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = CommentCreateSerializer
    lookup_field = 'id'
    permissions_class = [IsAuthenticated, ]

    def dispatch(self, request, *args, **kwargs):
        id_post = kwargs.pop('idpost')
        self.post_model = get_object_or_404(Post, id=id_post)

        try:
            id_parent = kwargs.pop('idparent')
            self.parent = get_object_or_404(Comment,
                                            id=id_parent,
                                            post=self.post_model)
        except Exception as e:
            self.parent = None

        return super(CommentCreateView, self).dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Añadir el author del comentario al momento de crearlo"""
        serializer.save(
            author=self.request.user,
            post=self.post_model,
            parent=self.parent
        )


class CommentDestroyView(mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = CommentCreateSerializer
    permissions_class = [IsAuthenticated, IsCommentOwner, ]

    def get_object(self):
        """Retorna el comentario del usuario"""
        return get_object_or_404(
            Comment,
            pk=self.kwargs['id']
        )

    def perform_destroy(self, instance):
        instance.soft_delete()
        instance.save()


class CommentListView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = CommentDetailSerializer
    permissions_class = [IsAuthenticated, ]

    def dispatch(self, request, *args, **kwargs):
        id_post = kwargs.pop('idpost')
        self.post_model = get_object_or_404(Post, id=id_post)
        return super(CommentListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(post=self.post_model, is_active=True)


class CommentLikeView(APIView):

    permissions_class = [IsAuthenticated, ]

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.pop('id')
        self.comment = get_object_or_404(Comment, id=id)
        return super(CommentLikeView, self).dispatch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user in self.comment.likes.all():
            self.comment.likes.remove(request.user)
        else:
            self.comment.likes.add(request.user)
        self.comment.save()
        data = CommentDetailSerializer(self.comment).data
        return Response(data, status.HTTP_200_OK)
