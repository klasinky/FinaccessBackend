from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


LOGIN_USER_URL = reverse('users-login')
GET_CURRENCIES_URL = reverse('currency')


def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
    )


class CurrencyPrivateAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email': "juma@test.com",
            'username': 'juma123',
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }
        self.user = create_user(**payload)

        res = self.client.post(LOGIN_USER_URL, {
            'email': payload['email'],
            'password': payload['password']
        })

        token = res.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_currencies(self):
        """Test retrieve all currencies"""
        res = self.client.get(GET_CURRENCIES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_currencies_error_not_logged(self):
        """Test anonymous user cannot see all currencies"""
        res = APIClient().get(GET_CURRENCIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
