import datetime

from django.db.models import Q, Count
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import random

from api.permissions import IsPostOwner
from api.serializers.posts import PostModelSerializer, PostCreateSerializer
from core.models import Post, PostLike, User
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
        """
        Lista todos los post. filtra por la cantidad de likes
        hot = post con mas likes en el dia
        top = post con mas likes
        """
        sorting = self.request.query_params.get('sort')
        filter_by_followers = self.request.query_params.get('followers')
        query = Q()
        filter_query = Q()

        if filter_by_followers is not None:

            followers_list = self.request.user.following.all().values_list('following__id', flat=True)
            filter_query = Q(author__id__in=followers_list)

        if sorting is not None:
            if sorting == 'hot':
                week_end = datetime.datetime.now()
                week_start = week_end - datetime.timedelta(days=7)
                post_likes = PostLike.objects.filter(created_at__gte=week_start)
                query = Q(postlike__in=post_likes)

            post_list = Post.objects.annotate(num_likes=Count(
                'likes', filter=query
            )).filter(filter_query, is_active=True,).order_by('-num_likes')

            return post_list

        return Post.objects.filter(filter_query, is_active=True)

    def create(self, request, *args, **kwargs):
        cache_key = f'post_created-{request.user.pk}'
        if cache.has_key(cache_key):
            return Response({'detail': 'Tienes que esperar 5 minutos para crear otro post'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        cache.set(cache_key, True, timeout=300)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Añadir el author del post al momento de crearlo"""
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete()
        instance.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PostCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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
        cache_key = f'post_liked{self.post.pk}-{request.user.pk}'
        if cache.has_key(cache_key):
            return Response({'detail': 'Tienes que esperar 10 segundos para repetir esta acción'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user in self.post.likes.all():
            like = PostLike.objects.get(post=self.post, user=request.user)
            like.delete()

        else:
            like = PostLike.objects.create(post=self.post, user=request.user)
            like.save()
        self.post.save()
        cache.set(cache_key, True, timeout=10)
        data = PostModelSerializer(self.post, context=serializer_context).data
        return Response(data, status.HTTP_200_OK)


class PostRecommendationView(APIView):
    permissions_class = [IsAuthenticated, ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post = None

    def dispatch(self, request, *args, **kwargs):
        id_post = kwargs.pop('id')
        self.post = get_object_or_404(Post, id=id_post)
        return super(PostRecommendationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        # Si el post contiene TAGS, se buscan los similares
        if self.post.tags.all().count() > 0:
            post_list = Post.objects\
                .filter(tags__in=self.post.tags.all(), is_active=True)\
                .exclude(pk=self.post.pk).distinct()[:3]
        # Si no contiene tags, buscan 3 randoms
        else:
            valid_id_list = Post.objects.filter(is_active=True).values_list('id', flat=True)
            random_id_list = random.sample(list(valid_id_list), min(len(valid_id_list), 3))
            post_list = Post.objects.filter(id__in=random_id_list)

        data = PostModelSerializer(post_list, context=serializer_context, many=True).data

        return Response(data, status.HTTP_200_OK)


class PostByUser(APIView):
    permissions_class = [IsAuthenticated, ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.pop('username')
        self.user = get_object_or_404(User, username=username)
        return super(PostByUser, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        posts = Post.objects.filter(author=self.user, is_active=True)
        data = PostModelSerializer(posts, context=serializer_context, many=True).data
        return Response(data, status=status.HTTP_200_OK)
