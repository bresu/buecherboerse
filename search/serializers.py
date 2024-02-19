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

# todo: sellers are all private

# class OfferSerializer(serializers.ModelSerializer):
#     # Use SellerSerializer to represent the seller field for serialization
#     seller = SellerSerializer(read_only=True)
#     # Add a write-only field to accept the seller ID for create/update operations
#     seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True, source='seller')
#
#     class Meta:
#         model = Offer
#         fields = '__all__'  # Make sure this includes both 'seller' and 'seller_id'
#         extra_kwargs = {
#             'seller': {'read_only': True},  # Ensure seller object is read-only
#         }


class OfferSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True, source='seller')

    class Meta:
        model = Offer
        fields = ['id', 'isbn', 'price', 'marked', 'seller', 'seller_id', 'member', 'active', 'createdAt', 'modified', 'location']
        extra_kwargs = {
            'seller': {'read_only': True},  # Ensure seller object is read-only
        }

    def to_representation(self, instance):
        # Start with the public data
        ret = super().to_representation(instance)
        request = self.context.get('request')

        # Remove non-public fields for unauthenticated users
        if not request or not request.user.is_authenticated:
            non_public_fields = ['seller', 'member', 'active', 'createdAt', 'modified', 'location']
            for field in non_public_fields:
                ret.pop(field, None)

        return ret

# todo: member same serializiation as seller
# pagination?