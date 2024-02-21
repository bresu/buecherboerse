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


    # def test_delete_single_entry(self):
