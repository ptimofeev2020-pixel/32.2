from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@mail.ru', password='Pass12345!', last_name='Иванов')
        self.other = User.objects.create_user(email='o@mail.ru', password='Pass12345!')

    def test_register(self):
        response = self.client.post(reverse('users:register'), {'email': 'new@mail.ru', 'password': 'Pass12345!'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)

    def test_register_duplicate_email(self):
        response = self.client.post(reverse('users:register'), {'email': 'u@mail.ru', 'password': 'Pass12345!'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens(self):
        response = self.client.post(reverse('users:login'), {'email': 'u@mail.ru', 'password': 'Pass12345!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_own_profile_full(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('users:user-detail', args=[self.user.pk]))
        self.assertIn('payments', response.data)
        self.assertIn('last_name', response.data)

    def test_other_profile_public_only(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get(reverse('users:user-detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('payments', response.data)
        self.assertNotIn('last_name', response.data)
        self.assertNotIn('password', response.data)

    def test_edit_only_own_profile(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(reverse('users:user-detail', args=[self.user.pk]), {'city': 'X'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(reverse('users:user-detail', args=[self.other.pk]), {'city': 'Казань'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payments_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('users:payment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
