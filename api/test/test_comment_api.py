from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
    )


# Urls


LOGIN_USER_URL = reverse('users-login')


class CommentPrivateAPITests(TestCase):
    pass
    # def setUp(self):
    #     self.client = APIClient()
    #     payload = {
    #         'email': "juma@test.com",
    #         'username': 'juma123',
    #         'name': "Juan Manuel",
    #         'password': "Juma123!",
    #         'password_confirmation': "Juma123!"
    #     }
    #
    #     create_user(**payload)
    #
    #     res = self.client.post(LOGIN_USER_URL, {
    #         'email': payload['email'],
    #         'password': payload['password']
    #     })
    #
    #     token = res.data['access_token']
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
