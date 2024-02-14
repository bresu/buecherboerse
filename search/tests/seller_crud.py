from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from search.models import Seller


class SellerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authentication
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a seller instance for testing update and delete
        cls.seller = Seller.objects.create(full_name="John Doe", email="john@example.com",
                                           matriculation_number="12345678")

    def test_create_seller_success(self):
        self.url = reverse('seller-list')
        self.client.force_authenticate(user=self.user)
        data = {'full_name': 'Jane Doe', 'email': 'jane@example.com', 'matriculation_number': '87654321'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seller.objects.count(), 2)  # Assuming one seller was already created in setUpTestData

    def test_create_seller_failure(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-list')
        data = {}  # Missing required fields
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_seller_success(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('seller-detail', kwargs={'pk': self.seller.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'John Doe')

    def test_retrieve_seller_failure(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('seller-detail', kwargs={'pk': 999})  # Assuming this ID does not exist
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_seller_success(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('seller-detail', kwargs={'pk': self.seller.pk})
        data = {'full_name': 'John Updated', 'email': 'johnupdated@example.com', 'matriculation_number': '12345678'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.full_name, 'John Updated')

    def test_update_seller_failure(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('seller-detail', kwargs={'pk': self.seller.pk})
        data = {'full_name': ''}  # Invalid data
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_seller_success(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('seller-detail', kwargs={'pk': self.seller.pk})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seller.objects.filter(pk=self.seller.pk).exists(), False)

    def test_delete_seller_failure(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse('seller-detail', kwargs={'pk': 999})  # Assuming this ID does not exist
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
