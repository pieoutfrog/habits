from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTokenTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )

    def test_get_user_token(self):
        data = {
            'username': 'Oleg',
            'password': 'Oleg'
        }

        response = self.client.post(
            reverse('users:token_obtain_pair'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserCreateTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_user_create(self):
        data = {
            'username': 'Oleg',
            'password': 'Oleg',
            'chat_id': '918273645'
        }

        response = self.client.post(
            reverse('users:user_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )

    def test_users_list(self):
        response = self.client.get(
            reverse('users:user_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )

    def test_user_retrieve(self):
        response = self.client.get(
            reverse('users:user_detail',
                    args=[self.user.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )

    def test_user_update(self):
        data = {
            'username': 'test1',
        }
        response = self.client.patch(
            reverse('users:user_update',
                    args=[self.user.pk]),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDestroyTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Oleg',
            password='Oleg',
            chat_id='918273645'
        )

    def test_user_destroy(self):
        response = self.client.delete(
            reverse('users:user_delete',
                    args=[self.user.pk]),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)