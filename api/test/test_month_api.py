from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from core.models import Month


def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
    )

# Urls


def get_month_url(id):
    return reverse('months-viewset', args=[id])


LOGIN_USER_URL = reverse('users-login')
CREATE_LIST_MONTH_URL = reverse('months')


class MonthPrivateAPITests(TestCase):
    """Probar todos los endpoints que sean privados"""

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email': "juma@test.com",
            'username': 'juma123',
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }

        create_user(**payload)

        res = self.client.post(LOGIN_USER_URL, {
            'email': payload['email'],
            'password': payload['password']
        })

        token = res.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_create_month(self):
        """Crear un mes"""
        res = self.client.post(CREATE_LIST_MONTH_URL,{})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_not_allow_create_duplicated_months(self):
        """Comprobrar si no se pueden crear los meses iguales"""
        res = self.client.post(CREATE_LIST_MONTH_URL, {})
        res2 = self.client.post(CREATE_LIST_MONTH_URL, {})
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_month(self):
        """Eliminar un mes"""
        res_month = self.client.post(CREATE_LIST_MONTH_URL, {})
        id = res_month.data['url'].split("/")[-1]
        res = self.client.delete(get_month_url(id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Month.objects.all().count(),0)

    def test_retrieve_month(self):
        """Consigue la información de un mes"""
        res_month = self.client.post(CREATE_LIST_MONTH_URL, {})
        id = res_month.data['url'].split("/")[-1]
        res = self.client.get(get_month_url(id))
        month = Month.objects.get(pk=id)
        date = f"{month.date.year}-{month.date.month:02d}"
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['month']['date'], date)
