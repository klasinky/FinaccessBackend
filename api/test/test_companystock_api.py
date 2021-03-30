from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.models import CompanyStock, UserCompany


def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
    )


def create_company()->CompanyStock:
    return CompanyStock.objects.create(
        name='Tesla',
        symbol='tsla'
    )


def create_usercompany(user, company)->UserCompany:
    return UserCompany.objects.create(
        user=user,
        companystock=company)


# Urls


LOGIN_USER_URL = reverse('users-login')
COMPANY_STOCK_LIST = reverse('companystock-list')
ALL_COMPANIES_LIST = reverse('companystock-all')


def get_companyview_url(id):
    return reverse('companystock-view', args=[id])


class CompanyStockPrivateAPITests(TestCase):
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

        self.user = create_user(**payload)

        res = self.client.post(LOGIN_USER_URL, {
            'email': payload['email'],
            'password': payload['password']
        })

        token = res.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


    def test_subscribe_company(self):
        """Suscribirse a una accion"""
        company = create_company()
        res = self.client.post(get_companyview_url(company.pk))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        user_company_count = UserCompany.objects.filter(
            user=self.user,
            companystock=company
        ).count()
        self.assertEqual(user_company_count, 1)

    def test_subscribe_company_fail(self):
        """Comprobrar que no te puedes suscribir 2 veces a la misma acción"""
        company = create_company()
        self.client.post(get_companyview_url(company.pk))
        res = self.client.post(get_companyview_url(company.pk))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_company_count = UserCompany.objects.filter(
            user=self.user,
            companystock=company
        ).count()
        self.assertEqual(user_company_count, 1)

    def test_delete_subscribe_company(self):
        """Borrar una acción a la cual estas suscrito"""
        company = create_company()
        user_company = create_usercompany(self.user, company)
        res = self.client.delete(get_companyview_url(user_company.pk))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        user_company_count = UserCompany.objects.filter(
            user=self.user,
            companystock=company
        ).count()
        self.assertEqual(user_company_count, 0)

    def test_delete_subscribe_company_fail(self):
        """Comprobar que otro usuario no puede eliminar tu suscripción"""
        company = create_company()
        payload = {
            'email': "maju@test.com",
            'username': 'maju123',
            'name': "Manuel Juan ",
            'password': "Muja123!",
        }
        fake_user = create_user(**payload)
        user_company = create_usercompany(fake_user, company)
        res = self.client.delete(get_companyview_url(user_company.pk))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_company_count = UserCompany.objects.filter(
            user=fake_user,
            companystock=company
        ).count()
        self.assertEqual(user_company_count, 1)

    def test_get_subscribe_company(self):
        """Obtener las acciones a las que esta suscrita"""
        company = create_company()
        user_company = create_usercompany(self.user, company)
        res = self.client.get(COMPANY_STOCK_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_companies(self):
        """Obtener todas las acciones disponibles"""
        create_company()
        res = self.client.get(ALL_COMPANIES_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)