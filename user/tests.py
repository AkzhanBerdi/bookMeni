from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from .constants import ResponseMessage

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.email = 'test@email.com'
        self.password = 'password'

    def test_register_correct_keys(self):
        url = reverse('user:register')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(username=self.email).exists())

    def test_register_incorrect_keys(self):
        url = reverse('user:register')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ResponseMessage.INVALID_REGISTRATION_KEY)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(User.objects.filter(username=self.email).exists())

    def test_register_with_existing_email(self):
        User.objects.create.user(
            username=self.email, email=self.email, password=self.password
        )
        url = reverse('user:register')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ResponseMessage.ALREADY_REGISTERED)
        self.assertEqual(User.objects.count(), 1)

class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.username = 'test@mail.com'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username, email=self.username, password=self.password
        )
        self.token = Token.objects.create(user=self.user).key

    def test_login_correct_credentials(self):
        url = reverse('user:login')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token)

    def test_login_incorrect_credentials(self):
        url = reverse('user:login')
        data = {'username': self.username, 'password': 'abc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, ResponseMessage.INVALID_LOGIN_DATA)

    def test_login_incorrect_keys(self):
        url = reverse('user:login')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, ResponseMessage.INVALID_LOGIN_DATA)

# Create your tests here.
