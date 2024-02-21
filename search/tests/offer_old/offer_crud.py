# test_offer_api.py
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from search.models import Seller, Offer
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class OfferAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.seller = Seller.objects.create(fullName="John Doe", email="john@example.com", matriculationNumber="12345678")
        cls.token = get_tokens_for_user(cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.offer_data = {
            'isbn': '1234567890123',
            'price': 100.00,
            'seller_id': self.seller.id,  # Use seller's id for creation
            'member': self.user.id,  # Assuming member is a User
            'active': True
        }
        # Create an offer for use in tests
        self.offer = Offer.objects.create(
            isbn='1234567890123',
            price=100.00,
            seller=self.seller,
            member=self.user,
            active=True
        )

    def test_create_offer(self):
        response = self.client.post(reverse('offer-list'), data=self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)  # One is created in setUp

    def test_retrieve_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isbn'], self.offer.isbn)

    def test_patch_offer(self):
        new_price = 150.00
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, {'price': new_price}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.price, new_price)

    def test_put_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        updated_offer_data = {
            'isbn': '9816543210987',
            'price': 200.00,
            'seller_id': self.seller.id,  # Use the same seller's id or a different one if your test case requires it
            'member': self.user.id,  # Assuming member references a User instance
            'active': False  # Change attributes as needed for your test case
        }
        response = self.client.put(url, data=updated_offer_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.isbn, updated_offer_data['isbn'])
        self.assertEqual(self.offer.price, updated_offer_data['price'])
        self.assertEqual(self.offer.active, updated_offer_data['active'])

        # Add more assertions as necessary to verify all fields were updated correctly

    def test_delete_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)
