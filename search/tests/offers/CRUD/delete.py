from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from search.models import Exam, Book, Seller, Offer

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
        cls.book = Book.objects.create(isbn="1234567890123", title="Buchtitel", authors="Ich & Du", maxPrice=200, edition=1, publisher="Manz", exam_id=1)
        cls.token = get_tokens_for_user(cls.user)
        cls.offer_url = reverse('offer-bulk-delete')  # Ensure this is the correct URL name for your bulk delete endpoint

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.offer1 = Offer.objects.create(book=self.book, price=100.00, seller=self.seller, member=self.user, active=True)
        self.offer2 = Offer.objects.create(book=self.book, price=150.00, seller=self.seller, member=self.user, active=True)

    def test_errornous_body_sent(self):
        """
        Test sending an erroneous body (not a list) to the bulk deletion endpoint.
        """
        response = self.client.post(self.offer_url, {'offers': 'not a list'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_list_sent(self):
        """
        Test sending a correctly formatted body, but the list is empty.
        """
        response = self.client.post(self.offer_url, {'offers': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correct_list_sent(self):
        """
        Test sending a correct list of offer IDs for deletion.
        """
        response = self.client.post(self.offer_url, {'offers': [self.offer1.id, self.offer2.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer1.refresh_from_db()
        self.offer2.refresh_from_db()
        self.assertFalse(self.offer1.active)
        self.assertFalse(self.offer2.active)

    def test_duplicate_ids_in_list(self):
        """
        Test sending a list containing the same offer ID twice. This should lead to an error due to the
        uniqueness constraint or logic in the view that should handle duplicate IDs.
        """
        # Assuming your logic needs to catch and handle this as an error
        response = self.client.post(self.offer_url, {'offers': [self.offer1.id, self.offer1.id]}, format='json')
        # Adjust the expected response based on how your endpoint handles this case
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.offer1.refresh_from_db()
        self.offer2.refresh_from_db()

        # Additional assertions to verify that both offers remain active
        self.assertTrue(self.offer1.active, "Offer1 should remain active")
        self.assertTrue(self.offer2.active, "Offer2 should remain active")
