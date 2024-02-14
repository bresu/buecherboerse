from django.contrib.auth.models import User
from search.models import Offer, Seller
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
class OfferPriceGTFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authentication
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a seller instance for associating with offers
        cls.seller = Seller.objects.create(full_name="John Doe", email="john@example.com",
                                           matriculation_number="12345678")
        # Create test offers
        cls.offer_active = Offer.objects.create(
            isbn="1111111111111",
            wish_price=50.00,
            member_id=cls.user,
            # seller_id=cls.seller,
            is_active=True,
            location="A1"
        )
        cls.offer_inactive = Offer.objects.create(
            isbn="2222222222222",
            wish_price=75.00,
            member_id=cls.user,
            # seller_id=cls.seller,
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

    def test_filter_wish_price_gt_success_with_results(self):
        """
        Success case: Filtering offers with 'wish_price' greater than a value should return matching offers.
        """
        response = self.client.get(reverse('offer-list'), {'wish_price_gt': '30'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Assuming there are offers with 'wish_price' > 30
        self.assertTrue(all(float(offer['wish_price']) > 30 for offer in response.data))

    def test_filter_wish_price_gt_success_no_results(self):
        """
        Success case: Filtering offers with 'wish_price' greater than a high value should return no offers.
        """
        response = self.client.get(reverse('offer-list'), {'wish_price_gt': '1000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Assuming no offers have 'wish_price' > 1000

    def test_filter_wish_price_gt_error_invalid_value(self):
        """
        Error case: Filtering offers with an invalid 'wish_price' value should be handled gracefully.
        """
        response = self.client.get(reverse('offer-list'), {'wish_price_gt': 'not_a_number'})
        self.assertNotEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Depending on API design, you might expect a 400 Bad Request or simply no results with a 200 OK.
        # This assertion checks that the server does not return a 500 error, indicating some graceful handling of the error.

    def test_filter_wish_price_gt_error_negative_value(self):
        """
        Error case: Filtering offers with a negative 'wish_price' value.
        """
        response = self.client.get(reverse('offer-list'), {'wish_price_gt': '-10'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming the logic treats negative values as valid input but returns no results.
        self.assertEqual(len(response.data), 0)
