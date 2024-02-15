from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from search.models import Seller, Offer  # Adjust the import path as necessary


class OfferAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user1 and get the token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a test seller and offer
        self.seller = Seller.objects.create(fullName="Test Seller", matriculationNumber="12345678", email="seller@example.com")
        self.offer = Offer.objects.create(isbn="1234567890123", price=100.00, member=self.user, active=True)

    def test_get_offer_detail_authenticated(self):
        # Obtain a JWT token
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        token = response.data['access']
        print("Token Response:", response.data)  # Print the token response

        # Use the token to authenticate the request
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Attempt to retrieve the offer
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        print("Authenticated Offer Detail Response:\n", response.data)  # Print the offer detail response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isbn'], self.offer.isbn)

    def test_get_offer_detail_unauthenticated(self):
        # Attempt to retrieve the offer without authentication
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        print("Unauthenticated Offer Detail Response:\n", response.data)  # Print the unauthenticated response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
