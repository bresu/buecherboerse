from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from search.validators import validate_isbn_numeric

exam_char_length = 20


class Exam(models.Model):
    name = models.CharField(max_length=exam_char_length, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name


class Seller(models.Model):
    fullName = models.CharField(max_length=255, verbose_name="Vor- und Nachname")
    matriculationNumber = models.CharField(max_length=8, validators=[MinLengthValidator(8)],
                                           verbose_name="Matrikelnummer", unique=True) # todo solve this shit
    email = models.EmailField(verbose_name="E-Mail", unique=True)
    note = models.TextField(verbose_name="Anmerkung", blank=True, null=True)

    def __str__(self):
        return f"{self.fullName} - {self.matriculationNumber}"


class Book(models.Model):
    isbn = models.CharField(max_length=13, verbose_name="ISBN", primary_key=True,validators=[validate_isbn_numeric])
    title = models.CharField(max_length=100, verbose_name="Titel")
    authors = models.CharField(max_length=100, verbose_name="Autoren")
    maxPrice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Maximaler Preis")
    edition = models.IntegerField(verbose_name="Auflage")
    publisher = models.CharField(max_length=30, verbose_name="Verlag")
    exam = models.ForeignKey(Exam, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Prüfung")
    # old

    def __str__(self):
        return f"{self.title} - {self.edition}"


class Offer(models.Model):
    """
    Offer represents the logical link of a seller selling a book. An offer is always created by some member.
    Offers have a price and are either active or inactive.
    """
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="ISBN")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Wunschpreis")
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name="Verkäufer:in")
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="FV-Mitglied")
    active = models.BooleanField(default=True, verbose_name="Aktiv")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    modified = models.DateTimeField(auto_now=True, verbose_name="Zuletzt geändert am")
    marked = models.BooleanField(default=True, verbose_name="Markiert")
    location = models.CharField(max_length=5, null=True, blank=True, verbose_name="Lagerort")
    note = models.TextField(verbose_name="Anmerkung", blank=True, null=True)

    def __str__(self):
        return f"{self.pk} - {self.book_id}: {self.book_id}"


class Transaction(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Betrag")
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name="Verkäufer:in")
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="FV-Mitglied")
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Check if the instance already exists
            raise ValidationError("Transactions cannot be modified once created.")
        super().save(*args, **kwargs)

    def __str__(self):
        out = ""
        if self.value < 0:
            out += f"AUS: {self.value} ID:{self.offer}"
        else:
            out += f"EIN: {self.value} ID:{self.offer}"

        return out

