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
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create seller instances for associating with offers
        cls.seller1 = Seller.objects.create(fullName="John Doe", email="john@example.com",
                                            matriculationNumber="12345678")
        cls.seller2 = Seller.objects.create(fullName="Jane Doe", email="jane@example.com",
                                            matriculationNumber="87654321")

        # Create test offers associated with different sellers
        cls.offer_seller1 = Offer.objects.create(
            isbn="1111111111111",
            price=50.00,
            member=cls.user,
            seller=cls.seller1,
            active=True,
            location="A1"
        )
        cls.offer_seller2 = Offer.objects.create(
            isbn="2222222222222",
            price=75.00,
            member=cls.user,
            seller=cls.seller2,
            active=True,
            location="B2"
        )

    def setUp(self):
        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

    def test_filter_by_seller_exact(self):
        base_url = reverse('offer-list')
        query_params = {'seller': self.seller1.id}  # Filter by the first seller's ID
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assuming there is only one offer from seller1
        self.assertEqual(len(response.data), 1)

        # Check if the response contains offers only from the specified seller
        # Adjust the assertion to match the nested structure
        self.assertEqual(response.data[0]['seller']['id'], self.seller1.id)
        self.assertEqual(response.data[0]['seller']['fullName'], self.seller1.fullName)
        self.assertEqual(response.data[0]['seller']['email'], self.seller1.email)

    def test_filter_by_non_existent_seller(self):
        base_url = reverse('offer-list')
        query_params = {
            'seller': '9999'}  # Ensure the seller ID is sent as a string if your filtering logic expects that
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        print(response.data)  # Debugging: Print response data to see error messages
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=f"Response data: {response.data}")  # Added message for debugging
        self.assertEqual(len(response.data), 0)