from rest_framework import serializers
from .models import Seller, Offer, Transaction


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'  # Adjust fields as necessary'