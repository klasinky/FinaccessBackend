from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from core.models import Category, Month, Entry


def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
    )


# Urls


LOGIN_USER_URL = reverse('users-login')
CREATE_LIST_MONTH_URL = reverse('months')


def get_entry_url(id):
    return reverse('entries-viewset', args=[id])


def create_entry_url(id):
    return reverse('entries', args=[id])


def create_category():
    return Category.objects.create(name='Comida')


def create_entry(id_month):
    category = create_category()
    month = Month.objects.get(pk=id_month)
    return Entry.objects.create(
        name="Comida",
        description="Desc",
        amount=44,
        category=category,
        month=month
    )


class EntryPrivateAPITests(TestCase):
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
        self.category = create_category()

    def test_create_entry(self):
        """Crear un ingreso"""
        res_month = self.client.post(CREATE_LIST_MONTH_URL, {})
        id = res_month.data['url'].split("/")[-1]
        payload = {
            'name': 'Comida',
            'description': "Una harina pan",
            'amount': 23,
            'category': self.category.pk
        }
        res = self.client.post(create_entry_url(id), payload)
        entry_count = Entry.objects.filter(month__pk=id).count()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entry_count, 1)

    def test_update_entry(self):
        """Modifica la informacion de un ingreso realizado"""
        res_month = self.client.post(CREATE_LIST_MONTH_URL, {})
        id = res_month.data['url'].split("/")[-1]
        payload = {
            'name': 'Informatica',
            'description': "Una laptop",
            'amount': 2300
        }
        entry = create_entry(id);
        res = self.client.patch(get_entry_url(entry.pk), payload)
        entry.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(entry.name, payload['name'])
        self.assertEqual(entry.description, payload['description'])
        self.assertEqual(entry.amount, payload['amount'])

    def test_retrieve_entry(self):
        """Consigue la información de un ingreso realizado"""
        res_month = self.client.post(CREATE_LIST_MONTH_URL, {})
        id = res_month.data['url'].split("/")[-1]
        entry = create_entry(id);
        res = self.client.get(get_entry_url(entry.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(entry.name, res.data['name'])
        self.assertEqual(entry.description, res.data['description'])
        self.assertEqual(entry.amount, res.data['amount'])

    def test_delete_entry(self):
        """Elimina un ingreso realizado"""
        res_month = self.client.post(CREATE_LIST_MONTH_URL, {})
        id = res_month.data['url'].split("/")[-1]
        entry = create_entry(id);
        res = self.client.delete(get_entry_url(entry.pk))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Entry.objects.all().count(), 0)
