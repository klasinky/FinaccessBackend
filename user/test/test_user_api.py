from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password


def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
        )


CREATE_USER_URL = reverse('users-register')
LOGIN_USER_URL = reverse('users-login')


def getProfileURL(username):
    return reverse('users-profile', args=[username])

def getDetailURL(username):
    return reverse('users-detail', args=[username])



class UserPublicAPITest(TestCase):
    """Probar todos los endpoints que sean públicos"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'username': "juma",
            'email': "juma@test.com",
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }

    def test_create_valid_user(self):
        """Test crear un usuario valido"""

        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exits(self):
        """Comprueba que no se creen 2 usuarios iguales"""
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Comprueba si un usuario puede iniciar sesión"""
        payload = {
            'email': self.payload['email'],
            'password': self.payload['password'],
        }
        create_user(**self.payload)
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', res.data)

    def test_profile_fail_not_credentials(self):
        """Comprobar que no se pueda acceder a un perfil sin estar autenticado"""
        profile_url = getProfileURL(self.payload['username'])
        res = self.client.get(profile_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserPrivateAPITests(TestCase):
    """Probar todos los endpoints que sean privados"""

    def setUp(self):
        self.client = APIClient()

        self.payload = {
            'username': "juma",
            'email': "juma@test.com",
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }

        self.user = create_user(**self.payload)

        res = self.client.post(LOGIN_USER_URL, {
            'email': self.payload['email'],
            'password': self.payload['password']
            })

        token = res.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_user_profile(self):
        """Consigue la información del usuario"""
        profile_url = getProfileURL(self.payload['username'])
        res = self.client.get(profile_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.user.username)

    def test_update_user_profile(self):
        """Actualiza la información del usuario"""
        payload = {
            'username': "maju2",
            'name': "Manuel Juan",
        }
        detail_url = getDetailURL(self.payload['username'])
        res = self.client.patch(detail_url, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)


