from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from search.models import Seller  # Update 'your_app' with the actual app name

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class SellerAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='admin', password='adminpassword')
        cls.token = get_tokens_for_user(cls.user)
        # Create a seller to test duplicate scenarios
        cls.existing_seller = Seller.objects.create(
            fullName='Existing Seller',
            matriculationNumber='12345678',
            email='existing@example.com',
            note='Existing note'
        )

        cls.existing_seller_no_mrn = Seller.objects.create(
            fullName='Existing Seller',
            #matriculationNumber='12345678',
            email='existing2@example.com',
            note='Existing note'
        )

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_seller_successfully(self):
        seller_data = {
            'fullName': "New Seller",
           'matriculationNumber': "87654321",
            'email': "new@example.com",
            'note': "New seller note",
        }
        response = self.client.post(reverse('seller-list'), data=seller_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Seller.objects.filter(email='new@example.com').exists())

    def test_create_seller_duplicate_email(self):
        seller_data = {
            'fullName': "Another Seller",
            'matriculationNumber': "12345679",
            'email': "existing@example.com",  # Duplicate email
            'note': "Another seller note",
        }
        response = self.client.post(reverse('seller-list'), data=seller_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_seller_duplicate_matriculation_number(self):
        seller_data = {
            'fullName': "Another Seller",
            'matriculationNumber': "12345678",  # Duplicate matriculation number
            'email': "unique@example.com",
            'note': "Another seller note",
        }
        response = self.client.post(reverse('seller-list'), data=seller_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_seller_no_mrn_unique(self):
        seller_data = {
            'fullName': "Another Seller",
            #'matriculationNumber': "12345678",  # Duplicate matriculation number
            'email': "unique2@example.com",
            'note': "Another seller note",
        }
        response = self.client.post(reverse('seller-list'), data=seller_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_seller_no_mrn_duplicate_mail(self):
        seller_data = {
            'fullName': "Another Seller",
            # 'matriculationNumber': "12345678",  # Duplicate matriculation number
            'email': "existing2@example.com",
            'note': "Another seller note",
        }

        response = self.client.post(reverse('seller-list'), data=seller_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
