from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from search.models import Exam, Book
from django.db import IntegrityError
from django.test import TransactionTestCase

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.exam = Exam.objects.create(name="Test Exam")
        cls.token = get_tokens_for_user(cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_book_with_exam_id(self):
        book_data_with_exam = {
            'isbn': "9781234567897",
            'title': "Test Book With Exam",
            'authors': "Author One, Author Two",
            'maxPrice': "49.99",
            'edition': 1,
            'publisher': "Test Publisher",
            'exam_id': self.exam.id,
        }
        response = self.client.post(reverse('book-list'), data=book_data_with_exam, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('exam' in response.data)

    def test_create_book_without_exam_id(self):
        book_data_without_exam = {
            'isbn': "9781234567896",
            'title': "Test Book Without Exam",
            'authors': "Author One, Author Two",
            'maxPrice': "39.99",
            'edition': 1,
            'publisher': "Test Publisher",
            # No 'exam_id' provided
        }
        response = self.client.post(reverse('book-list'), data=book_data_without_exam, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
        #self.assertFalse('exam' in response.data or 'exam_id' in response.data)

    def test_create_book_non_digit_isbn(self):
        book_data_without_exam = {
            'isbn': "978123456789a", # not allowed
            'title': "Test Book Without Exam",
            'authors': "Author One, Author Two",
            'maxPrice': "39.99",
            'edition': 1,
            'publisher': "Test Publisher",
            # No 'exam_id' provided
        }
        response = self.client.post(reverse('book-list'), data=book_data_without_exam, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertFalse('exam' in response.data or 'exam_id' in response.data)


class BookModelTransactionTests(TransactionTestCase):

    def test_duplicate_isbn_creation_fails(self):
        isbn = "1234567890123"
        Book.objects.create(
            isbn=isbn,
            title="First Book",
            authors="Author One",
            maxPrice=50.00,
            edition=1,
            publisher="Publisher One",
        )

        # Attempt to create another book with the same ISBN
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                isbn=isbn,
                title="Second Book",
                authors="Author Two",
                maxPrice=55.00,
                edition=1,
                publisher="Publisher Two",
            )

        # No further operations after the exception is caught are necessary here
