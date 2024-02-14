from django.contrib.auth.models import User
from search.models import Offer, Seller
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class OfferFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authentication
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a seller instance for associating with offers
        cls.seller = Seller.objects.create(full_name="John Doe", email="john@example.com", matriculation_number="12345678")
        # Create test offers
        cls.offer_active = Offer.objects.create(
            isbn="1111111111111",
            wish_price=50.00,
            member_id=cls.user,
            #seller_id=cls.seller,
            is_active=True,
            location="A1"
        )
        cls.offer_inactive = Offer.objects.create(
            isbn="2222222222222",
            wish_price=75.00,
            member_id=cls.user,
            #seller_id=cls.seller,
            is_active=False,
            location="B2"
        )
        # Directly modify the 'created_at' field if necessary for specific tests
        # Note: This step is optional and shown here for illustrative purposes
        Offer.objects.filter(pk=cls.offer_active.pk).update(created_at=timezone.now() - timedelta(days=100))
        cls.offer_active.refresh_from_db()

    def setUp(self):
        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

    def test_filter_by_is_active_true(self):
        """
        Test filtering offers where is_active is True.
        """
        response = self.client.get(reverse('offer-list'), {'is_active': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming default pagination, adjust if necessary
        print(response.data)
        self.assertTrue(all(offer['is_active'] for offer in response.data))

    def test_filter_by_is_active_false(self):
        """
        Test filtering offers where is_active is False.
        """
        response = self.client.get(reverse('offer-list'), {'is_active': 'False'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertTrue(all(not offer['is_active'] for offer in response.data))
