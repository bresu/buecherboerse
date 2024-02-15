from django.contrib.auth.models import User
from search.models import Offer, Seller
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from urllib.parse import urlencode, urljoin


class OfferPriceGTFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user1 for authentication
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a seller instance for associating with offers
        cls.seller = Seller.objects.create(fullName="John Doe", email="john@example.com",
                                           matriculationNumber="12345678")
        # Create test offers
        cls.offer_active_50 = Offer.objects.create(
            isbn="1111111111111",
            price=50.00,
            member=cls.user,
            seller=cls.seller,
            active=True,
            location="A1"
        )
        cls.offer_inactive_75 = Offer.objects.create(
            isbn="2222222222222",
            price=75.00,
            member=cls.user,
            seller=cls.seller,
            active=False,
            location="B2"
        )
        cls.offer_active_10 = Offer.objects.create(
            isbn="3333333333333",
            price=10.00,
            member=cls.user,
            seller=cls.seller,
            active=True,
            location="C3"
        )
        # Directly modify the 'created_at' field if necessary for specific tests
        # Note: This step is optional and shown here for illustrative purposes
        Offer.objects.filter(pk=cls.offer_active_50.pk).update(createdAt=timezone.now() - timedelta(days=100))
        cls.offer_active_50.refresh_from_db()

    def setUp(self):
        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

    def test_filter_price_greater_than(self):
        base_url = reverse('offer-list')
        query_params = {'price__gt': '10'}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 offers since there are two offers with price greater than 10
        self.assertEqual(len(response.data), 2)

    def test_filter_price_less_than(self):
        base_url = reverse('offer-list')
        query_params = {'price__lt': '60'}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 offers since there are two offers with price less than 60
        self.assertEqual(len(response.data), 2)

    def test_filter_price_greater_than_or_equal_to(self):
        base_url = reverse('offer-list')
        query_params = {'price__gte': '50'}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 offers since there are two offers with price greater than or equal to 50
        self.assertEqual(len(response.data), 2)

    def test_filter_price_less_than_or_equal_to(self):
        base_url = reverse('offer-list')
        query_params = {'price__lte': '50'}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 offers since there are two offers with price less than or equal to 50
        self.assertEqual(len(response.data), 2)

    def test_filter_price_less_than_0(self):
        base_url = reverse('offer-list')
        query_params = {'price__lt': '0'}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 offers since there are two offers with price less than or equal to 50
        self.assertEqual(len(response.data), 0)

    def test_filter_price_exact(self):
        base_url = reverse('offer-list')
        exact_price = '50.00'  # Assuming you want to test for offers exactly priced at 50.00
        query_params = {'price': exact_price}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 1 offer since there is one offer with price exactly 50.00
        # Adjust the expected number based on your test data setup
        self.assertEqual(len(response.data), 1)
