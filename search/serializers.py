from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Seller, Offer, Transaction


# abstract
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    # Use SellerSerializer to represent the seller field for serialization
    seller = SellerSerializer(read_only=True)
    # Add a write-only field to accept the seller ID for create/update operations
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True, source='seller')

    class Meta:
        model = Offer
        fields = '__all__'  # Make sure this includes both 'seller' and 'seller_id'
        extra_kwargs = {
            'seller': {'read_only': True},  # Ensure seller object is read-only
        }



# todo: member same serializiation as seller
#