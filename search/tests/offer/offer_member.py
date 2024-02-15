from django.contrib.auth.models import User
from search.models import Offer, Seller
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from urllib.parse import urlencode


class OfferSellerFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users for authentication
        cls.user1 = User.objects.create_user(username='testuser', password='testpassword')
        cls.user2 = User.objects.create_user(username='testuser2', password='testpassword2')


        # Create seller instances for associating with offers
        cls.seller1 = Seller.objects.create(fullName="John Doe", email="john@example.com",
                                            matriculationNumber="12345678")
        cls.seller2 = Seller.objects.create(fullName="Jane Doe", email="jane@example.com",
                                            matriculationNumber="87654321")

        # Create test offers associated with different sellers
        cls.offer_user1 = Offer.objects.create(
            isbn="1111111111111",
            price=50.00,
            member=cls.user1,
            seller=cls.seller1,
            active=True,
            location="A1"
        )
        cls.offer_user2 = Offer.objects.create(
            isbn="2222222222222",
            price=75.00,
            member=cls.user2,
            seller=cls.seller2,
            active=True,
            location="B2"
        )

    def setUp(self):
        # Authenticate the test client
        self.client.force_authenticate(user=self.user1)

    def test_filter_offers_by_member_positive(self):
        base_url = reverse('offer-list')
        query_params = {'member': self.user1.id}  # Filter by the first user's ID
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting only offers associated with user1
        self.assertEqual(len(response.data), 1)
        # Verify that the returned offer(s) are indeed for the specified member
        self.assertEqual(response.data[0]['member'], self.user1.id)
        print(response.data)

    def test_filter_offers_by_non_existent_member(self):
        base_url = reverse('offer-list')
        non_existent_member_id = 9999  # ID for a non-existent member
        query_params = {'member': non_existent_member_id}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting an empty list since no offers are associated with a non-existent member
        self.assertEqual(len(response.data), 0)
        print(response.data)