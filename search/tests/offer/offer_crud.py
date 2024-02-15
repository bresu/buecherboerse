# <your_app>/tests/test_offer_api.py

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from search.models import Offer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class OfferAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.token = get_tokens_for_user(cls.user)
        cls.offer_data = {
            'isbn': '1234567890123',
            'price': 100.00,
            'member': cls.user,
            'active': True
        }
        cls.offer = Offer.objects.create(**cls.offer_data)

    def test_create_offer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('offer-list'), {
            'isbn': '9876543210987',
            'price': 150.00,
            'member': self.user.id,
            'active': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)  # Assuming one offer was already created in setUpTestData

    def test_retrieve_offer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isbn'], self.offer.isbn)
        print("OUTPUT: " + str(response.data))

    def test_retrieve_inactive_offer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Soft delete the offer
        self.offer.is_active = False
        self.offer.save()
        # Attempt to retrieve the now inactive offer
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("OUTPUT: " + str(response.data))

    def test_update_offer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.patch(reverse('offer-detail', kwargs={'pk': self.offer.pk}), {
            'price': 120.00,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.wish_price, 120.00)
        print("OUTPUT: " + str(response.data))

    def test_soft_delete_offer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.offer.refresh_from_db()
        self.assertFalse(self.offer.is_active)
        print("OUTPUT: " + str(self.offer.is_active))
