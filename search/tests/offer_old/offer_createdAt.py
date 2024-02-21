from django.contrib.auth.models import User
from search.models import Offer, Seller
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from urllib.parse import urlencode, urljoin

# todo: maybe we have to change the formating for ease of use

class OfferPriceGTFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user1 for authentication
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a seller instance for associating with offers
        cls.seller = Seller.objects.create(fullName="John Doe", email="john@example.com",
                                           matriculationNumber="12345678")
        # Create test offers
        cls.offer_one_year_old = Offer.objects.create(
            isbn="1111111111111",
            price=50.00,
            member=cls.user,
            seller=cls.seller,
            active=True,
            location="A1"
        )
        cls.offer_now = Offer.objects.create(
            isbn="2222222222222",
            price=75.00,
            member=cls.user,
            seller=cls.seller,
            active=False,
            location="B2"
        )
        cls.offer_one_month_old = Offer.objects.create(
            isbn="3333333333333",
            price=10.00,
            member=cls.user,
            seller=cls.seller,
            active=True,
            location="C3"
        )
        # Directly modify the 'created_at' field if necessary for specific tests
        # Note: This step is optional and shown here for illustrative purposes
        Offer.objects.filter(pk=cls.offer_one_year_old.pk).update(createdAt=timezone.now() - timedelta(days=365))
        cls.offer_one_year_old.refresh_from_db()

        Offer.objects.filter(pk=cls.offer_one_month_old.pk).update(createdAt=timezone.now() - timedelta(days=30))
        cls.offer_one_month_old.refresh_from_db()

    def setUp(self):
        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

    def test_filter_offers_older_than_one_week(self):
        base_url = reverse('offer-list')
        one_week_ago = timezone.now() - timedelta(weeks=1)
        # Format the date string for the query
        one_week_ago_str = one_week_ago.strftime('%Y-%m-%dT%H:%M:%S')
        query_params = {'createdAt__lt': one_week_ago_str}  # Filtering for offers created before one week ago
        url = f"{base_url}?{urlencode(query_params)}"
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that all returned offers have a createdAt date older than one week
        for offer in response.data:
            offer_created_at = timezone.datetime.strptime(offer['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                tzinfo=timezone.utc)
            self.assertTrue(offer_created_at < one_week_ago, "Offer is not older than one week")

        print(response.data)