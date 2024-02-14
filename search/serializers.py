from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Seller, Offer, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    # todo: foreign key works?
    class Meta:
        model = Offer
        fields = '__all__'  # Adjust fields as necessary'