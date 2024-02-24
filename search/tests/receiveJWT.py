from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase, RequestFactory
from search.middleware import JWTAuthenticationMiddleware


class AuthTestCase(APITestCase):
    def setUp(self):
        # Create a test user1
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

    def test_obtain_jwt_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)


class JWTAuthenticationMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = JWTAuthenticationMiddleware(get_response=lambda request: HttpResponse())

    def test_jwt_token_in_cookie(self):
        # Simulate a request with an access token cookie
        request = self.factory.get('/some-path', HTTP_COOKIE='access_token=your_jwt_token_here')
        self.middleware(request)

        # Check if the Authorization header is correctly set
        self.assertIn('HTTP_AUTHORIZATION', request.META)
        self.assertEqual(request.META['HTTP_AUTHORIZATION'], 'Bearer your_jwt_token_here')