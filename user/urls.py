# from django.urls import path, include

# from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserViewSet

# router = DefaultRouter()
# router.register('users', UserViewSet, basename='users')

user_login = UserViewSet.as_view({
    'post': 'login'
})

user_register = UserViewSet.as_view({
    'post': 'register'
})

user_profile = UserViewSet.as_view({
    'get': 'profile'
})

user_detail = UserViewSet.as_view({
    'get': 'detail',
    'put': 'update',
    'patch': 'partial_update'
})

user_delete = UserViewSet.as_view({
    'patch': 'soft_delete'
})
urlpatterns = [
    path('login/', user_login, name="users-login"),
    path('register/', user_register, name="users-register"),
    path('profile/<str:username>', user_profile, name="users-profile"),
    path('me/detail/<str:username>', user_detail, name="users-detail"),
    path('me/delete', user_delete, name='users-soft')
]
