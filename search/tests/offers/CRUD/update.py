from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from search.models import Seller, Offer, Book, Exam


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class OfferAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.seller = Seller.objects.create(fullName="John Doe", email="john@example.com", matriculationNumber="12345678")
        cls.exam = Exam.objects.create(name="FÜM1")
        cls.book = Book.objects.create(isbn="1234567890123", title="Buchtitel", authors="Ich & Du", maxPrice=200,edition=1,publisher="Manz", exam_id=1)
        cls.token = get_tokens_for_user(cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.offer = Offer.objects.create(
            book_id=self.book.isbn,
            price=100.00,
            seller_id=self.seller.id,
            member_id=self.user.id,
        )

    def test_put_offer_valid(self):
        offer_data = {
            'book_id': self.book.isbn,
            'price': 999.00,
            'seller_id': self.seller.id,
            'member_id': self.user.id,
            'marked': False
        }

        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.put(url,data=offer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(float(response.data['price'])), 999)
        self.assertNotEquals(response.data['marked'], self.offer.marked)


    def test_put_offer_invalid(self):
        offer_data = {
            'book_id': self.book.isbn,
            'price': 999.00,    # valid
            'seller_id': self.seller.id,
            'member_id': self.user.id,
            'active': False     # invalid
        }

        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.put(url, data=offer_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(int(float(response.data['price'])), 999)

    def test_patch_offer_valid(self):
        patch_data = {
            'marked': not self.offer.marked,
            'location': 'ABC'
        }

        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, data=patch_data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(response.data['marked'], True)
        self.assertNotEqual(response.data['location'], None)


    def test_patch_offer_invalid_active(self):
        patch_data = {
            'active': True
        }

        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, data=patch_data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    def test_patch_offer_invalid_createdAt(self):
        patch_data = {
            'createdAt': '2024-02-21T15:41:15.892802Z'
        }

        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.patch(url, data=patch_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
