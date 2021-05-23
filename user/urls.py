from django.urls import path
from .views import UserViewSet, UserCheckAuthenticated, UserProfileViewSet, users_tops

user_login = UserViewSet.as_view({
    'post': 'login'
})

user_register = UserViewSet.as_view({
    'post': 'register'
})

user_profile = UserViewSet.as_view({
    'get': 'profile',
    'put': 'update',
    'patch': 'partial_update'
})

user_delete = UserViewSet.as_view({
    'patch': 'soft_delete'
})

user_change_password = UserViewSet.as_view({
    'patch': 'change_password'
})

user_public_profile = UserProfileViewSet.as_view({
    'get': 'retrieve',
    'patch':'follow'
})

urlpatterns = [
    path('login', user_login, name="users-login"),
    path('register', user_register, name="users-register"),
    path('me', user_profile, name="users-profile"),
    path('me/delete', user_delete, name='users-soft'),
    path('profile/<str:username>', user_public_profile, name="users-public-profile"),
    path('me/changepassword', user_change_password, name='users-changepassword'),
    path('check', UserCheckAuthenticated.as_view(), name="user-check-authenticated"),
    path('tops', users_tops, name="user-top")
]
