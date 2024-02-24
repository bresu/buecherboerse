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


    def test_create_offer(self):
        offer_data = {
            'price': 100.00,
            'seller_id': self.seller.id,  # Use seller's id for creation
            'member_id': self.user.id,  # Assuming member is a User
            'book_id': self.book.isbn,
            'active': True,
            'marked': True,
            'note': "i am a note"
        }
        response = self.client.post(reverse('offer-list'), data=offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)  # One is created in setUp
        print(response.data)

    def test_create_offer_fails_no_price(self):
        offer_data = {
            'seller_id': self.seller.id,  # Use seller's id for creation
            'member_id': self.user.id,  # Assuming member is a User
            'book_id': self.book.isbn,
            'exam_id': self.exam.id,
            'active': True
        }
        response = self.client.post(reverse('offer-list'), data=offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)

    def test_create_offer_optional_fields_defaults(self):
        # missing active and marked when posting sets both values to true
        offer_data = {
            'price': 10,
            'seller_id': self.seller.id,  # Use seller's id for creation
            'member_id': self.user.id,  # Assuming member is a User
            'book_id': self.book.isbn,
        }
        response = self.client.post(reverse('offer-list'), data=offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['active'], True)
        self.assertEqual(response.data['marked'], True)

    def test_create_offer_illegal_book_id(self):
        offer_data = {
            'price': 10,
            'book_id': 9999,
            'seller_id': self.seller.id,  # Use seller's id for creation
            'member_id': self.user.id,  # Assuming member is a User
        }
        response = self.client.post(reverse('offer-list'), data=offer_data, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_offer_illegal_seller_id(self):
        offer_data = {
            'price': 10,
            'book_id': self.book.isbn,
            'seller_id': 9999,
            'member_id': self.user.id,  # Assuming member is a User
        }
        response = self.client.post(reverse('offer-list'), data=offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_offer_illegal_member_id(self):
        offer_data = {
            'price': 10,
            'book_id': self.book.isbn,
            'seller_id': self.seller.id,
            'member_id': 9999,  # Assuming member is a User
        }
        response = self.client.post(reverse('offer-list'), data=offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
