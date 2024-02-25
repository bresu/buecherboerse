from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from search.models import Seller, Offer, Book, Exam

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class BulkCreateOfferAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.seller = Seller.objects.create(fullName="John Doe", email="john@example.com", matriculationNumber="12345678")
        cls.exam = Exam.objects.create(name="FÜM1")
        cls.book = Book.objects.create(isbn="1234567890123", title="Buchtitel", authors="Ich & Du", maxPrice=200, edition=1, publisher="Manz", exam=cls.exam)
        cls.token = get_tokens_for_user(cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.valid_offer_data = {
            'price': 100.00,
            'seller_id': self.seller.id,
            'member_id': self.user.id,
            'book_id': self.book.isbn,
            'active': True,
            'marked': True,
            'note': "Valid note"
        }

    def test_bulk_create_offer_empty_list(self):
        response = self.client.post(reverse('offer-bulk-create'), data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_create_offer_single(self):
        response = self.client.post(reverse('offer-bulk-create'), data=[self.valid_offer_data], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertIsNotNone(response.data[0]['id'])

    def test_bulk_create_offer_with_non_existing_seller(self):
        offers_data = [
            self.valid_offer_data,
            self.valid_offer_data,
            {**self.valid_offer_data, 'seller_id': 9999}  # Non-existing seller
        ]
        response = self.client.post(reverse('offer-bulk-create'), data=offers_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Offer.objects.count(), 0)  # No offers should be created

    def test_bulk_create_offer_multiple_valid(self):
        offers_data = [self.valid_offer_data, self.valid_offer_data, self.valid_offer_data]
        response = self.client.post(reverse('offer-bulk-create'), data=offers_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 3)
        for offer_response in response.data:
            self.assertIsNotNone(offer_response['id'])
