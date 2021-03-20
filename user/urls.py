from django.urls import path
from .views import UserViewSet

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

user_change_password = UserViewSet.as_view({
    'patch': 'change_password'
})

urlpatterns = [
    path('login', user_login, name="users-login"),
    path('register', user_register, name="users-register"),
    path('profile/<str:username>', user_profile, name="users-profile"),
    path('me/detail/<str:username>', user_detail, name="users-detail"),
    path('me/delete', user_delete, name='users-soft'),
    path('me/changepassword', user_change_password, name='users-changepassword')
]
