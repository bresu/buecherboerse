from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='test@gmail.com')

    def test_obtain_token_success(self):
        """
        Normalfall: Successfully obtaining a token with valid credentials.
        """
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_failure(self):
        """
        Fehlerfall: Fail to obtain a token with invalid credentials.
        """
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        """
        Normalfall: Successfully refresh the access token.
        """
        # First, obtain a refresh token
        obtain_url = reverse('token_obtain_pair')
        obtain_data = {'username': 'testuser', 'password': 'testpassword123'}
        obtain_response = self.client.post(obtain_url, obtain_data)
        refresh_token = obtain_response.data['refresh']

        # Now, try to refresh the access token
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

        # Note: A specific "failure" case for token refresh might involve an expired or invalid refresh token,
        # which would require manipulating token lifetimes or using a known invalid token.

    def test_user_detail_retrieval_success(self):
        """
        Normalfall: Successfully retrieving user1 details when authenticated.
        """
        self.client.force_authenticate(user=self.user)  # Simulate being logged in
        url = reverse('auth_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_detail_retrieval_failure(self):
        """
        Fehlerfall: Fail to retrieve user1 details when not authenticated.
        """
        url = reverse('auth_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        """
        Normalfall: Successfully "logging out" by instructing the client to discard the token.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('auth_logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_detail_unauthenticated_access(self):
        """
        Ensure that unauthenticated access to the user1 detail endpoint
        returns a 401 Unauthorized response.
        """
        url = reverse('auth_user')  # Use the correct name for your user1 detail endpoint
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)