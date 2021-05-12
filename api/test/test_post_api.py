from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from core.models import Post, Tag


def create_user(**params):
    return get_user_model().objects.create_user(
        username=params['username'],
        name=params['name'],
        email=params['email'],
        password=params['password']
    )


def create_post(user):
    return Post.objects.create(
        title='Titulo',
        description='Descripcion del post',
        author=user
    )

# Urls


LOGIN_USER_URL = reverse('users-login')
CREATE_POST_URL = reverse('posts-create-list')


def get_post_url(id):
    return reverse('posts-viewset', args=[id])

def get_post_like_url(id):
    return reverse('posts-like', args=[id])


class PostPrivateAPITest(TestCase):

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

    def test_create_post(self):
        """Crear un post"""
        payload = {
            'title': 'Test Title',
            'description': 'Test Description'
        }
        res = self.client.post(CREATE_POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post_count = Post.objects.filter(author=self.user).count()
        self.assertEqual(post_count, 1)

    def test_create_post_with_tag(self):
        """Crear un post"""
        tag = Tag.objects.create(name='finanzas')
        payload = {
            'title': 'Test Title',
            'description': 'Test Description',
            'tags': [str(tag.pk),]
        }
        res = self.client.post(CREATE_POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post_count = Post.objects.filter(author=self.user).count()
        self.assertEqual(post_count, 1)
        post = Post.objects.last()
        self.assertEqual(tag in post.tags.all(), True)

    def test_create_post_with_multiple_tags(self):
        """Crear un post"""
        tag = Tag.objects.create(name='finanzas')
        tag2 = Tag.objects.create(name='help')
        tag3 = Tag.objects.create(name='bug')
        payload = {
            'title': 'Test Title',
            'description': 'Test Description',
            'tags': [str(tag.pk),str(tag2.pk),str(tag3.pk), ]
        }

        res = self.client.post(CREATE_POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post_count = Post.objects.filter(author=self.user).count()
        self.assertEqual(post_count, 1)
        post = Post.objects.last()
        self.assertEqual(tag in post.tags.all(), True)
        self.assertEqual(tag2 in post.tags.all(), True)
        self.assertEqual(tag3 in post.tags.all(), True)

    def test_create_post_fail_cache(self):
        """Comprobar que no te deje crear 2 post consecutivos"""
        payload = {
            'title': 'Test Title',
            'description': 'Test Description'
        }
        res = self.client.post(CREATE_POST_URL, payload)
        res2 = self.client.post(CREATE_POST_URL, payload)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_post(self):
        """Obtener un post"""
        post = create_post(self.user)
        res = self.client.get(get_post_url(post.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], post.title)
        self.assertEqual(res.data['description'], post.description)

    def test_update_post(self):
        """Actualizar un post"""
        post = create_post(self.user)
        payload = {
            'title': 'Test Title Modified',
            'description': 'Test Description Modified'
        }
        res = self.client.patch(get_post_url(post.pk), payload)
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['title'], post.title)
        self.assertEqual(payload['description'], post.description)

    def test_change_finished_post(self):
        """Cambiar el campo finished de un post"""
        post = create_post(self.user)
        url = reverse('posts-change-finished', args=[post.pk])
        res = self.client.patch(url, {})
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(post.finished)
        res = self.client.patch(url, {})
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(post.finished)

    def test_soft_delete(self):
        """Eliminar un mes"""
        post = create_post(self.user)
        res = self.client.delete(get_post_url(post.pk))
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(post.is_active)

    def test_update_post_fail_if_not_owner(self):
        """Comprobar que un usuario no pueda editar un post si no es suyo"""
        payload_user = {
            'email': "jum2a@test.com",
            'username': 'juma1234',
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }
        fake_user = create_user(**payload_user)
        post = create_post(fake_user)
        payload = {
            'title': 'Test Title Modified',
            'description': 'Test Description Modified'
        }
        res = self.client.patch(get_post_url(post.pk), payload)
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(post.title, payload['title'])
        self.assertNotEqual(post.description, payload['description'])

    def test_soft_delete_post_fail_if_not_owner(self):
        """Comprobar que un usuario no pueda eliminar un post si no es suyo"""
        payload_user = {
            'email': "jum2a@test.com",
            'username': 'juma1234',
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }
        fake_user = create_user(**payload_user)
        post = create_post(fake_user)
        res = self.client.delete(get_post_url(post.pk))
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(post.is_active)

    def test_change_finished_post_fail_not_owner(self):
        """Comprobar que un usuario no pueda cambiar el estado de un post si no es suyo"""
        payload_user = {
            'email': "jum2a@test.com",
            'username': 'juma1234',
            'name': "Juan Manuel",
            'password': "Juma123!",
            'password_confirmation': "Juma123!"
        }
        fake_user = create_user(**payload_user)
        post = create_post(fake_user)
        url = reverse('posts-change-finished', args=[post.pk])
        res = self.client.patch(url, {})
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(post.finished)

    def test_post_like(self):
        """Dar like a un post"""
        post = create_post(self.user)
        res = self.client.put(get_post_like_url(post.pk))
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(post.total_likes(), 1)

    def test_post_like_fail_cache(self):
        """Comprobar el cache de los likes en el mismo post"""
        post = create_post(self.user)
        self.client.put(get_post_like_url(post.pk))
        res = self.client.put(get_post_like_url(post.pk))
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post.total_likes(), 1)

    def test_different_post_like(self):
        """Comprobar el cache de los likes en diferentes posts"""
        post = create_post(self.user)
        post2 = create_post(self.user)
        res = self.client.put(get_post_like_url(post.pk))
        res2 = self.client.put(get_post_like_url(post2.pk))
        post.refresh_from_db()
        post2.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(post.total_likes(), 1)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(post2.total_likes(), 1)

    def test_list_posts_with_sort(self):
        res = self.client.get(f'{CREATE_POST_URL}?sort=hot')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res2 = self.client.get(f'{CREATE_POST_URL}?sort=top')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
