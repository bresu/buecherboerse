from django.contrib import admin
from .models import Seller, Transaction, Offer, Book, Exam


admin.site.register(Seller)
admin.site.register(Transaction)
admin.site.register(Offer)
admin.site.register(Book)
admin.site.register(Exam)
