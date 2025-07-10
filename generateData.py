import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buecherboerse.settings')
django.setup()

from search.models import Seller, Book, Offer, Exam
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


def create_specific_book_offers(n, isbn, min_price, max_price):
    """Create n offers for a specific book with Gaussian price distribution"""
    # Create or get the specific exam for the book
    exam, created = Exam.objects.get_or_create(name="Zivilverfahrensrecht und so weiter")
    if created:
        print(f"Created exam: {exam.name}")
    
    # Create or get the specific book
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': "Österreichisches Strafrecht. Besonderer Teil II (§§ 169 bis 321k StGB)",
            'authors': "Maxima Musterfrau, Max Mustermann, Herr von und zu Name",
            'maxPrice': 123.41,
            'edition': 123,
            'publisher': "FVJus Verlag bester Verlag",
            'exam': exam
        }
    )
    if created:
        print(f"Created book: {book.title}")
    
    # Create or get the specific seller
    seller, created = Seller.objects.get_or_create(
        matriculationNumber="01234567",
        defaults={
            'fullName': "Martha Musterfrau",
            'email': "user@email.com"
        }
    )
    if created:
        print(f"Created seller: {seller.fullName}")
    
    # Calculate mean and std for Gaussian distribution
    mean_price = (min_price + max_price) / 2
    std_price = (max_price - min_price) / 6  # 99.7% of values within range
    
    for _ in range(n):
        # Generate Gaussian price, clamped to min/max bounds
        price = random.gauss(mean_price, std_price)
        price = max(min_price, min(max_price, price))  # Clamp to bounds
        price = round(price, 2)
        
        active = fake.boolean()
        location = fake.postcode()[:4]
        marked = fake.boolean()
        
        Offer.objects.create(
            book=book, 
            price=price, 
            seller=seller,  # Use the specific seller
            marked=marked, 
            active=active, 
            location=location,
            member=User.objects.first()
        )
    
    print(f"Created {n} offers for book '{book.title}' (ISBN: {isbn}) by seller {seller.fullName}")


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
    
    # Create 100 offers for the specific book with Gaussian price distribution
    create_specific_book_offers(200, "1234123412341", 65, 123)
    create_specific_book_offers(200, "1231231231231", 45, 76)
    
    print("Fake data generation completed.")
