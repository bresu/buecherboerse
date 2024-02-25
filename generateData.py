import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buecherboerse.settings')
django.setup()

from search.models import Seller, Book, Offer, Exam  # Update 'your_app' to the name of your Django app
from django.contrib.auth import get_user_model

User = get_user_model()

fake = Faker()
Faker.seed(0)  # Set a seed for reproducibility


def create_exams(n):
    exams = []
    for _ in range(n):
        name = fake.word().capitalize()
        exam, created = Exam.objects.get_or_create(name=name)
        exams.append(exam)
    return exams


def create_sellers(n):
    for _ in range(n):
        fullName = fake.name()
        matriculationNumber = str(fake.unique.random_int(min=10000000, max=99999999))
        email = fake.unique.email()
        Seller.objects.create(fullName=fullName, matriculationNumber=matriculationNumber, email=email)


def create_books(n, exams):
    for _ in range(n):
        isbn = fake.isbn13().replace("-", "")
        title = fake.sentence(nb_words=5)
        authors = fake.name()
        maxPrice = round(random.uniform(10, 100), 2)
        edition = fake.random_int(min=1, max=10)
        publisher = fake.company()
        exam = random.choice(exams)
        Book.objects.create(isbn=isbn, title=title, authors=authors, maxPrice=maxPrice, edition=edition,
                            publisher=publisher, exam=exam)


def create_offers(n, books, sellers):
    for _ in range(n):
        book = random.choice(books)
        price = round(random.uniform(5, float(book.maxPrice)), 2)
        seller = random.choice(sellers)
        active = fake.boolean()
        location = fake.postcode()[:4]
        marked = fake.boolean()
        Offer.objects.create(book=book, price=price, seller=seller, marked=marked, active=active, location=location,
                             member=User.objects.first())


def generate_data(books=10, sellers=5, offers=20):
    exams = create_exams(5)  # Create some exams for the books
    create_sellers(sellers)
    create_books(books, exams)
    sellers = Seller.objects.all()
    books = Book.objects.all()
    create_offers(offers, books, sellers)


if __name__ == "__main__":
    # Set the number of Books, Offers, and Sellers you want to create
    generate_data(books=50, sellers=1000, offers=2000)
    print("Fake data generation completed.")
